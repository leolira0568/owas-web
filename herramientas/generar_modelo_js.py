"""Convierte el modelo Rajagopal 2016 de OpenSim en los datos compactos que usa la aplicación.

Genera en vendor/opensim:
- rajagopal2016.json, con la cadena cinemática: desplazamientos de cada articulación, ejes y
  funciones. Las curvas de la rodilla se guardan muestreadas cada grado.
- Rajagopal2016_OWAS.osim, el modelo con los 19 marcadores, para abrirlo en OpenSim.

Uso: python generar_modelo_js.py Rajagopal2016.osim   (carpeta Models/Rajagopal de OpenSim 4.6)
"""
import json
import math
import pathlib
import sys

import opensim as osim

from trc_a_opensim import colocar_marcadores

CARPETA = pathlib.Path(__file__).resolve().parent.parent / 'vendor/opensim'
SALIDA = CARPETA / 'rajagopal2016.json'
MODELO = CARPETA / 'Rajagopal2016_OWAS.osim'


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


def main():
    modelo = osim.Model(sys.argv[1])
    modelo.initSystem()
    coordenadas = {c.getName(): c for c in modelo.getCoordinateSet()}
    articulaciones = []
    for j in modelo.getJointSet():
        if j.getName().startswith('patellofemoral'):   # la rótula no lleva marcadores y su coordenada sigue a la rodilla
            continue
        padre, hijo = marco(j.getParentFrame()), marco(j.getChildFrame())
        a = {'nombre': j.getName(), 'padre': padre, 'hijo': hijo, 'ejes': []}
        cj = osim.CustomJoint.safeDownCast(j)
        if cj is not None:
            st = cj.getSpatialTransform()
            for i in range(6):
                t = st.getTransformAxis(i)
                nombres = t.getCoordinateNamesInArray()
                if nombres.getSize() == 0:
                    continue
                c = nombres.get(0)
                a['ejes'].append({'rot': i < 3, 'eje': vec(t.getAxis()), 'c': c, 'f': funcion(t.getFunction(), coordenadas[c])})
        elif j.getConcreteClassName() == 'PinJoint':
            a['ejes'].append({'rot': True, 'eje': [0, 0, 1], 'c': j.get_coordinates(0).getName(), 'f': [1, 0]})
        articulaciones.append(a)

    datos = {
        'coordenadas': [{'n': n, 'rot': c.getMotionType() == 1, 'd': r(c.getDefaultValue()), 'min': r(c.getRangeMin()), 'max': r(c.getRangeMax()),
                         'lim': c.get_clamped(), 'fija': c.get_locked()} for n, c in coordenadas.items()],
        'articulaciones': articulaciones,
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(datos, separators=(',', ':'), ensure_ascii=False), encoding='utf-8')
    print(SALIDA, SALIDA.stat().st_size, 'bytes,', len(articulaciones), 'articulaciones,', len(coordenadas), 'coordenadas')

    colocar_marcadores(modelo)
    modelo.printToXML(str(MODELO))
    # La licencia MIT pide conservar el aviso en las copias
    aviso = '<!-- ' + (CARPETA / 'LICENSE').read_text(encoding='utf-8').replace('--', '-') + '-->\n'
    texto = MODELO.read_text(encoding='utf-8')
    fin = texto.index('?>') + 3
    MODELO.write_text(texto[:fin] + aviso + texto[fin:], encoding='utf-8', newline='')
    print(MODELO, MODELO.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
