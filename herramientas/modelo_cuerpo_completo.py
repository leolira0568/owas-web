"""Crea la versión visible del modelo de cuerpo completo de Wilkinson que descarga OWAS Web.

Misma cinemática que el original: solo cambia la visibilidad. El modelo trae ocultos los huesos del tronco y de la
cabeza (vértebras, costillas, esternón, clavículas, escápulas, cervicales, cráneo y mandíbula) y los músculos del
tronco y los brazos; aquí se hacen visibles todas las mallas y todos los músculos.

La carpeta Geometry del modelo resultante debe reunir la geometría del repositorio original y la de los modelos
toracolumbares de ross-wilkinson/moco-cycling-standing (costillas, esternón, clavículas, escápulas, vértebras y
cabeza), que tiene prioridad porque OpenSim incluye archivos con el mismo nombre de otro modelo, más l_pat.vtp de la
geometría de OpenSim.

Uso: python modelo_cuerpo_completo.py cyclistFullBodyMuscle.osim cyclistFullBodyMuscle_OWAS.osim
"""
import sys
import xml.etree.ElementTree as ET


def main():
    entrada, salida = sys.argv[1:3]
    arbol = ET.parse(entrada)
    raiz = arbol.getroot()
    raiz.find('Model').set('name', 'cyclistFullBodyMuscle_OWAS')
    cambios = {'Mesh': 0, 'GeometryPath': 0}
    for etiqueta in cambios:
        for e in raiz.iter(etiqueta):
            v = e.find('Appearance/visible')
            if v is not None and v.text.strip() == 'false':
                v.text = 'true'
                cambios[etiqueta] += 1
    arbol.write(salida, encoding='UTF-8', xml_declaration=True)
    print(f'{salida}: {cambios["Mesh"]} mallas y {cambios["GeometryPath"]} músculos pasan a ser visibles')


if __name__ == '__main__':
    main()
