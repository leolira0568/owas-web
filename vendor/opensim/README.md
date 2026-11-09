# Modelos de OpenSim

Datos derivados de dos modelos de OpenSim, que `OWASWeb.html` incluye para calcular los ángulos articulares sin instalar OpenSim. Se generan con [`herramientas/generar_modelo_js.py`](../../herramientas/generar_modelo_js.py).

## Rajagopal 2016

- `rajagopal2016.json`: cadena cinemática del modelo (articulaciones, ejes, límites y curvas de la rodilla).
- `Rajagopal2016_OWAS.osim`: el modelo con los 19 marcadores de OWAS Web añadidos a los suyos, para abrirlo en OpenSim.

Se generan a partir de `Rajagopal2016.osim`, que OpenSim 4.6 instala en la carpeta `Models/Rajagopal`. Su cinemática es la misma que la del modelo Rajagopal 2015 de OpenSense, por lo que los `.mot` sirven para ambos.

Proyecto original: https://simtk.org/projects/full_body. Licencia: [MIT](LICENSE), © 2015 Stanford University.

Rajagopal, A., Dembia, C. L., DeMers, M. S., Delp, D. D., Hicks, J. L., & Delp, S. L. (2016). Full-body musculoskeletal model for muscle-driven simulation of human gait. *IEEE Transactions on Biomedical Engineering, 63*(10), 2068–2079.

## Cuerpo completo de Wilkinson

- `wilkinson2021.json`: cadena cinemática del modelo de cuerpo completo (piernas, 17 niveles vertebrales, cuello, costillas, esternón, cintura escapular y brazos).

Se genera a partir de `cyclistFullBodyMuscle.osim`, del repositorio https://github.com/ross-wilkinson/opensim-model-fullBodyMuscleActuated. El modelo y su geometría no se incluyen: se descargan de ese repositorio.

El modelo, adaptado por Ross Wilkinson, combina Rajagopal et al. (2016), Lai et al. (2017), el tronco de Allaire et al. (2020) y los brazos de Saul et al. (2015) actualizados por McFarland et al. (2019). Licencia: [MIT](LICENSE-wilkinson), © 2021 Ross Wilkinson.
