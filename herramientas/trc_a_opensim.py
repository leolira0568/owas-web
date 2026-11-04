"""Vincula un .trc exportado por OWAS Web a un modelo de OpenSim y calcula los ángulos articulares.

Escala el modelo con las longitudes medidas en el .trc, coloca los 19 marcadores en sus
articulaciones, ejecuta Inverse Kinematics y señala en _calidad.csv los fotogramas poco
fiables. Requiere el módulo opensim (pip install opensim).

Uso: python trc_a_opensim.py archivo.trc [--modelo Rajagopal_2015.osim] [--salida carpeta]
"""
import argparse
import csv
import math
import os
import pathlib
import statistics

import opensim as osim

MODELO = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs/OpenSim-4.6/opensim-core-4.6/Resources/Code/Matlab/OpenSenseExample/Rajagopal_2015.osim'

# Límites para señalar un fotograma como poco fiable. Son valores de partida, no están validados
ERROR_RMS = 5        # cm, error medio de los marcadores
ERROR_MAX = 10       # cm, error del peor marcador
TRONCO_MAX = 100     # grados respecto a la vertical: más allá, hombros por debajo de las caderas
DIF_TRONCO = 5       # grados de diferencia entre el modelo y los marcadores
LUMBAR_LATERAL = 30  # grados, flexión lateral lumbar
LUMBAR_GIRO = 40     # grados, rotación lumbar

# marcador: (cuerpo al que se fija, cuerpo cuyo origen marca la articulación, desplazamiento, peso en IK)
LADOS = {'L': 'l', 'R': 'r'}
MARCADORES = {'Nose': ('torso', 'torso', (.10, .58, 0), 0), 'LEar': ('torso', 'torso', (0, .58, -.07), 0), 'REar': ('torso', 'torso', (0, .58, .07), 0)}
for M, s in LADOS.items():
    MARCADORES |= {
        M + 'Shoulder': ('torso', f'humerus_{s}', (0, 0, 0), 5),
        M + 'Elbow': (f'ulna_{s}', f'ulna_{s}', (0, 0, 0), 1),
        M + 'Wrist': (f'hand_{s}', f'hand_{s}', (0, 0, 0), 1),
        M + 'Hip': ('pelvis', f'femur_{s}', (0, 0, 0), 5),
        M + 'Knee': (f'tibia_{s}', f'tibia_{s}', (0, 0, 0), 1),
        M + 'Ankle': (f'talus_{s}', f'talus_{s}', (0, 0, 0), 1),
        M + 'Heel': (f'calcn_{s}', f'calcn_{s}', (0, 0, 0), 1),
        M + 'Toe': (f'toes_{s}', f'toes_{s}', (.05, 0, 0), 1),
    }

# segmento: (cuerpos que escala, par de marcadores en el .trc, par de cuerpos en el modelo)
SEGMENTOS = [(f'{c}_{s}', (M + a, M + b), (f'{p}_{s}', f'{q}_{s}'))
             for M, s in LADOS.items()
             for grupo, a, b, p, q in (
                 (('femur', 'patella'), 'Hip', 'Knee', 'femur', 'tibia'),
                 (('tibia', 'talus', 'calcn', 'toes'), 'Knee', 'Ankle', 'tibia', 'talus'),
                 (('humerus',), 'Shoulder', 'Elbow', 'humerus', 'ulna'),
                 (('ulna', 'radius', 'hand'), 'Elbow', 'Wrist', 'ulna', 'hand'))
             for c in grupo]


def alinear(trc, destino):
    """Copia el .trc girando cada fotograma alrededor de la vertical para que las caderas miren hacia +X.

    Las posturas son independientes y la persona puede estar orientada de cualquier forma
    respecto a la cámara. Sin este giro, los ángulos de la pelvis son globales y pelvis_tilt
    deja de medir la inclinación del tronco.
    """
    lineas = trc.read_text(encoding='ascii').split('\n')
    nombres = [c for c in lineas[3].split('\t')[2:] if c]
    i, d = 2 + 3 * nombres.index('LHip'), 2 + 3 * nombres.index('RHip')
    salida = lineas[:6]
    for fila in lineas[6:]:
        c = fila.split('\t')
        if len(c) < 3:
            continue
        v = [float(x) for x in c[2:]]
        cx, cz = (v[i - 2] + v[d - 2]) / 2, (v[i] + v[d]) / 2
        giro = math.atan2(v[d - 2] - v[i - 2], v[d] - v[i])   # ángulo de la línea de caderas respecto a +Z
        co, se = math.cos(giro), math.sin(giro)
        for k in range(0, len(v), 3):
            x, z = v[k] - cx, v[k + 2] - cz
            v[k], v[k + 2] = co * x - se * z, se * x + co * z
        salida.append('\t'.join(c[:2] + [f'{x:.5f}' for x in v]))
    destino.write_text('\n'.join(salida) + '\n', encoding='ascii', newline='')


def leer_puntos(tabla):
    """Devuelve {marcador: [(x, y, z) por fotograma]}."""
    nombres = list(tabla.getColumnLabels())
    faltan = [m for m in MARCADORES if m not in nombres]
    if faltan:
        raise SystemExit(f'Al .trc le faltan marcadores: {faltan}')
    puntos = {m: [] for m in nombres}
    for i in range(tabla.getNumRows()):
        fila = tabla.getRowAtIndex(i)
        for j, m in enumerate(nombres):
            puntos[m].append((fila[j].get(0), fila[j].get(1), fila[j].get(2)))
    return puntos


def longitud(puntos, a, b):
    """Mediana de la distancia entre dos marcadores: resiste los fotogramas mal detectados."""
    return statistics.median(math.dist(p, q) for p, q in zip(puntos[a], puntos[b]))


def medio(p, q):
    return tuple((u + v) / 2 for u, v in zip(p, q))


def escalar(modelo, puntos):
    """Escala cada segmento según la relación entre lo medido y el modelo."""
    estado = modelo.initSystem()
    pos = {b.getName(): tuple(b.getPositionInGround(estado).get(k) for k in range(3)) for b in modelo.getBodySet()}
    factores = {}
    for cuerpo, (a, b), (p, q) in SEGMENTOS:
        factores[cuerpo] = longitud(puntos, a, b) / math.dist(pos[p], pos[q])
    factores['pelvis'] = longitud(puntos, 'LHip', 'RHip') / math.dist(pos['femur_l'], pos['femur_r'])
    tronco = statistics.median(math.dist(medio(a, b), medio(c, d)) for a, b, c, d in zip(puntos['LShoulder'], puntos['RShoulder'], puntos['LHip'], puntos['RHip']))
    factores['torso'] = tronco / math.dist(medio(pos['humerus_l'], pos['humerus_r']), medio(pos['femur_l'], pos['femur_r']))

    escalas = osim.ScaleSet()
    for cuerpo, f in factores.items():
        f = min(max(f, .5), 1.5)
        e = osim.Scale()
        e.setSegmentName(cuerpo)
        e.setScaleFactors(osim.Vec3(f, f, f))
        e.setApply(True)
        escalas.cloneAndAppend(e)
    modelo.scale(estado, escalas, True, -1.0)
    return factores


def colocar_marcadores(modelo):
    """Añade los marcadores en las articulaciones del modelo ya escalado."""
    estado = modelo.initSystem()
    cuerpos = modelo.getBodySet()
    lugares = {nombre: cuerpos.get(referencia).findStationLocationInAnotherFrame(estado, osim.Vec3(*desplazamiento), cuerpos.get(cuerpo))
               for nombre, (cuerpo, referencia, desplazamiento, _) in MARCADORES.items()}
    for nombre, lugar in lugares.items():   # añadir un marcador invalida el sistema: primero se calculan todos
        modelo.addMarker(osim.Marker(nombre, cuerpos.get(MARCADORES[nombre][0]), lugar))
    modelo.finalizeConnections()


def fijar_lumbar(modelo):
    """Bloquea la extensión lumbar con los hombros sobre las caderas.

    Sin marcadores en la pelvis, su inclinación y la flexión lumbar se compensan entre sí y
    IK las reparte de forma arbitraria. Bloqueada, pelvis_tilt mide toda la inclinación del
    tronco respecto a la vertical (negativo hacia delante).
    """
    estado = modelo.initSystem()
    cuerpos = modelo.getBodySet()
    pos = lambda n: tuple(cuerpos.get(n).getPositionInGround(estado).get(k) for k in range(3))
    lumbar = pos('torso')
    hombros, caderas = medio(pos('humerus_l'), pos('humerus_r')), medio(pos('femur_l'), pos('femur_r'))
    radio = math.hypot(hombros[0] - lumbar[0], hombros[1] - lumbar[1])
    delante = math.asin((caderas[0] - lumbar[0]) / radio) - math.atan2(hombros[0] - lumbar[0], hombros[1] - lumbar[1])
    coordenada = modelo.getCoordinateSet().get('lumbar_extension')
    coordenada.setDefaultValue(-delante)
    coordenada.setDefaultLocked(True)


def cinematica_inversa(modelo, trc, tabla, mot, carpeta):
    tiempos = tabla.getIndependentColumn()
    ik = osim.InverseKinematicsTool()
    ik.setModel(modelo)
    ik.setMarkerDataFileName(str(trc))
    ik.setStartTime(tiempos[0])
    ik.setEndTime(tiempos[-1])
    ik.setOutputMotionFileName(str(mot))
    ik.setResultsDir(str(carpeta))
    ik.set_report_errors(True)
    for nombre, (*_, peso) in MARCADORES.items():
        tarea = osim.IKMarkerTask()
        tarea.setName(nombre)
        tarea.setApply(peso > 0)
        tarea.setWeight(peso)
        ik.getIKTaskSet().cloneAndAppend(tarea)
    ik.run()


def revisar(puntos, mot, errores, destino):
    """Escribe la calidad de cada fotograma en un .csv y devuelve los poco fiables."""
    angulos, fallos = osim.TimeSeriesTable(str(mot)), osim.TimeSeriesTable(str(errores))
    columnas, columnas_error = list(angulos.getColumnLabels()), list(fallos.getColumnLabels())
    tiempos = angulos.getIndependentColumn()
    filas, dudosos = [], []
    for i in range(angulos.getNumRows()):
        fila, error = angulos.getRowAtIndex(i), fallos.getRowAtIndex(i)
        q = lambda c: fila[columnas.index(c)]
        rms, peor = (error[columnas_error.index(c)] * 100 for c in ('marker_error_RMS', 'marker_error_max'))
        hombros, caderas = medio(puntos['LShoulder'][i], puntos['RShoulder'][i]), medio(puntos['LHip'][i], puntos['RHip'][i])
        x, y, z = (a - b for a, b in zip(hombros, caderas))
        vertical = math.degrees(math.acos(y / math.hypot(x, y, z)))
        tronco, medido = -q('pelvis_tilt'), math.degrees(math.atan2(x, y))
        motivos = []
        if rms > ERROR_RMS:
            motivos.append(f'error medio {rms:.1f} cm')
        if peor > ERROR_MAX:
            motivos.append(f'peor marcador {peor:.1f} cm')
        if vertical > TRONCO_MAX:
            motivos.append(f'tronco a {vertical:.0f}° de la vertical')
        if abs(tronco - medido) > DIF_TRONCO:
            motivos.append(f'modelo y marcadores difieren {abs(tronco - medido):.0f}°')
        if abs(q('lumbar_bending')) > LUMBAR_LATERAL:
            motivos.append(f"flexión lateral {abs(q('lumbar_bending')):.0f}°")
        if abs(q('lumbar_rotation')) > LUMBAR_GIRO:
            motivos.append(f"rotación lumbar {abs(q('lumbar_rotation')):.0f}°")
        filas.append([f'{tiempos[i]:.3f}', f'{tronco:.1f}', f'{rms:.1f}', f'{peor:.1f}', 'no' if motivos else 'si', '; '.join(motivos)])
        if motivos:
            dudosos.append((tiempos[i], motivos))
    with destino.open('w', encoding='utf-8-sig', newline='') as f:
        escritor = csv.writer(f)
        escritor.writerow(['tiempo_s', 'tronco_grados', 'error_rms_cm', 'error_max_cm', 'fiable', 'motivos'])
        escritor.writerows(filas)
    return dudosos


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('trc', type=pathlib.Path)
    ap.add_argument('--modelo', type=pathlib.Path, default=MODELO)
    ap.add_argument('--salida', type=pathlib.Path)
    args = ap.parse_args()

    if not args.modelo.is_file():
        raise SystemExit(f'No se encontró el modelo {args.modelo}. Indíquelo con --modelo; pip install opensim no incluye modelos.')
    trc = args.trc.resolve()
    carpeta = (args.salida or trc.parent).resolve()
    carpeta.mkdir(parents=True, exist_ok=True)
    alineado = carpeta / f'{trc.stem}_alineado.trc'
    alinear(trc, alineado)
    tabla = osim.TimeSeriesTableVec3(str(alineado))
    puntos = leer_puntos(tabla)

    modelo = osim.Model(str(args.modelo))
    factores = escalar(modelo, puntos)
    colocar_marcadores(modelo)
    fijar_lumbar(modelo)
    osim_salida = carpeta / f'{trc.stem}_modelo.osim'
    modelo.printToXML(str(osim_salida))

    mot = carpeta / f'{trc.stem}_ik.mot'
    cinematica_inversa(osim.Model(str(osim_salida)), alineado, tabla, mot, carpeta)
    errores = carpeta / f'{trc.stem}_ik_errores.sto'
    os.replace(carpeta / '_ik_marker_errors.sto', errores)
    calidad = carpeta / f'{trc.stem}_calidad.csv'
    dudosos = revisar(puntos, mot, errores, calidad)

    print('Factores de escala:', {k: round(v, 2) for k, v in sorted(factores.items())})
    print('Modelo:', osim_salida)
    print('Ángulos:', mot)
    print('Calidad:', calidad)
    print(f'Fotogramas poco fiables: {len(dudosos)} de {tabla.getNumRows()}')
    for tiempo, motivos in dudosos:
        print(f'  {tiempo:.2f} s: ' + '; '.join(motivos))


if __name__ == '__main__':
    main()
