"""Convierte un modelo de OpenSim en los datos compactos que usa la aplicación.

Genera en vendor/opensim:
- <nombre>.json, con la cadena cinemática: desplazamientos de cada articulación, ejes y
  funciones. Las curvas (como las de la rodilla) se guardan muestreadas cada grado. Con
  --geometria, también unos puntos del contorno de los pies y las tibias, para apoyar el
  modelo en el suelo.
- Con --osim, el modelo con los 19 marcadores de OWAS Web, para abrirlo en OpenSim.

Uso:
  python generar_modelo_js.py Rajagopal2016.osim rajagopal2016 --osim Rajagopal2016_OWAS.osim --geometria <Geometry de OpenSim>
  python generar_modelo_js.py cyclistFullBodyMuscle.osim wilkinson2021 --geometria <Geometry del modelo> <Geometry de OpenSim>
"""
import argparse
import json
import math
import pathlib
import xml.etree.ElementTree as ET

import opensim as osim

from trc_a_opensim import colocar_marcadores

CARPETA = pathlib.Path(__file__).resolve().parent.parent / 'vendor/opensim'


def r(v):
    return round(v, 7) + 0


def vec(v):
    return [r(v.get(k)) for k in range(3)]


def funcion(f, coordenada):
    """Devuelve [pendiente, ordenada] si es lineal, o la curva muestreada en el rango de la coordenada."""
    tipo = f.getConcreteClassName()
    valor = lambda x: f.calcValue(osim.Vector(1, x))
    if tipo in ('LinearFunction', 'Constant'):
        return [r(valor(1) - valor(0)), r(valor(0))]
    bajo, alto = coordenada.getRangeMin(), coordenada.getRangeMax()
    n = math.ceil((alto - bajo) / math.radians(1))
    return {'x0': r(bajo), 'dx': r((alto - bajo) / n), 'y': [r(valor(bajo + (alto - bajo) * i / n)) for i in range(n + 1)]}


def marco(f):
    """Desplazamiento fijo de un marco respecto a su cuerpo: cuerpo, posición y orientación XYZ."""
    o = osim.PhysicalOffsetFrame.safeDownCast(f)
    if o is None:
        return [f.getName(), [0, 0, 0], [0, 0, 0]]
    return [o.getParentFrame().getName(), vec(o.get_translation()), vec(o.get_orientation())]


def contorno(cuerpo, carpetas, n=48):
    """Puntos repartidos por las mallas de un cuerpo (en su marco), elegidos por muestreo del punto más lejano."""
    pts = []
    for i in range(cuerpo.getPropertyByName('attached_geometry').size()):
        g = cuerpo.get_attached_geometry(i)
        if g.getConcreteClassName() != 'Mesh':
            continue
        nombre, esc = g.getPropertyByName('mesh_file').toString(), g.get_scale_factors()
        ruta = next((c / nombre for c in carpetas if (c / nombre).exists()), None)
        if ruta is None:
            raise SystemExit(f'No se encontró la geometría {nombre}')
        v = [float(x) for x in ET.parse(ruta).getroot().find('.//Points/DataArray').text.split()]
        pts += [(v[k] * esc.get(0), v[k + 1] * esc.get(1), v[k + 2] * esc.get(2)) for k in range(0, len(v), 3)]
    elegidos = [min(pts, key=lambda p: p[1])]
    dist = [math.dist(p, elegidos[0]) for p in pts]
    while len(elegidos) < min(n, len(pts)):
        k = max(range(len(pts)), key=dist.__getitem__)
        elegidos.append(pts[k])
        dist = [min(d, math.dist(p, pts[k])) for d, p in zip(dist, pts)]
    return [[round(x, 4) for x in p] for p in elegidos]


def ejes(j, coordenadas):
    """Ejes de movimiento de una articulación, en el orden en que se aplican."""
    tipo = j.getConcreteClassName()
    if tipo == 'CustomJoint':
        st = osim.CustomJoint.safeDownCast(j).getSpatialTransform()
        lista = []
        for i in range(6):
            t = st.getTransformAxis(i)
            nombres = t.getCoordinateNamesInArray()
            if nombres.getSize() == 0:
                continue
            c = nombres.get(0)
            lista.append({'rot': i < 3, 'eje': vec(t.getAxis()), 'c': c, 'f': funcion(t.getFunction(), coordenadas[c])})
        return lista
    if tipo == 'PinJoint':
        return [{'rot': True, 'eje': [0, 0, 1], 'c': j.get_coordinates(0).getName(), 'f': [1, 0]}]
    if tipo == 'UniversalJoint':   # gira sobre X y luego sobre Y
        return [{'rot': True, 'eje': [1, 0, 0], 'c': j.get_coordinates(0).getName(), 'f': [1, 0]},
                {'rot': True, 'eje': [0, 1, 0], 'c': j.get_coordinates(1).getName(), 'f': [1, 0]}]
    if tipo == 'WeldJoint':
        return []
    raise SystemExit(f'Tipo de articulación no admitido: {tipo} ({j.getName()})')


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('modelo', type=pathlib.Path)
    ap.add_argument('nombre')
    ap.add_argument('--osim')
    ap.add_argument('--geometria', nargs='*', type=pathlib.Path, default=[])
    args = ap.parse_args()

    modelo = osim.Model(str(args.modelo))
    modelo.initSystem()
    coordenadas = {c.getName(): c for c in modelo.getCoordinateSet()}
    articulaciones = []
    for j in modelo.getJointSet():
        if j.getName().startswith('patellofemoral'):   # la rótula no lleva marcadores y su coordenada sigue a la rodilla
            continue
        articulaciones.append({'nombre': j.getName(), 'padre': marco(j.getParentFrame()), 'hijo': marco(j.getChildFrame()), 'ejes': ejes(j, coordenadas)})
    # Cada cuerpo se calcula después de su padre
    ordenadas, hechos = [], {'ground'}
    while articulaciones:
        listas = [a for a in articulaciones if a['padre'][0] in hechos]
        if not listas:
            raise SystemExit('La cadena cinemática tiene cuerpos sin padre: ' + ', '.join(a['nombre'] for a in articulaciones))
        for a in listas:
            ordenadas.append(a); hechos.add(a['hijo'][0]); articulaciones.remove(a)

    datos = {
        'coordenadas': [{'n': n, 'rot': c.getMotionType() == 1, 'd': r(c.getDefaultValue()), 'min': r(c.getRangeMin()), 'max': r(c.getRangeMax()),
                         'lim': c.get_clamped(), 'fija': c.get_locked()} for n, c in coordenadas.items()],
        'articulaciones': ordenadas,
    }
    if args.geometria:
        # Pies y tibias: el punto más bajo del modelo estándar se apoya en el suelo (la planta o, de rodillas, la rodilla)
        datos['suelo'] = {b: contorno(modelo.getBodySet().get(b), args.geometria) for b in ('calcn_r', 'toes_r', 'tibia_r', 'calcn_l', 'toes_l', 'tibia_l')}
    salida = CARPETA / f'{args.nombre}.json'
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(datos, separators=(',', ':'), ensure_ascii=False), encoding='utf-8')
    print(salida, salida.stat().st_size, 'bytes,', len(ordenadas), 'articulaciones,', len(coordenadas), 'coordenadas')

    if args.osim:
        archivo = CARPETA / args.osim
        colocar_marcadores(modelo)
        modelo.printToXML(str(archivo))
        # La licencia MIT pide conservar el aviso en las copias
        aviso = '<!-- ' + (CARPETA / 'LICENSE').read_text(encoding='utf-8').replace('--', '-') + '-->\n'
        texto = archivo.read_text(encoding='utf-8')
        fin = texto.index('?>') + 3
        archivo.write_text(texto[:fin] + aviso + texto[fin:], encoding='utf-8', newline='')
        print(archivo, archivo.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
