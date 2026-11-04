# Modelo Rajagopal 2015

Archivos derivados del modelo de cuerpo completo de Rajagopal et al. (2016), que `OWASWeb.html` incluye para calcular los ángulos articulares sin instalar OpenSim:

- `rajagopal2015.json`: cadena cinemática del modelo (articulaciones, ejes y curvas de la rodilla).
- `Rajagopal2015_OWAS.osim`: el modelo con los 19 marcadores de OWAS Web, para abrirlo en OpenSim.

Ambos se generan con [`herramientas/generar_modelo_js.py`](../../herramientas/generar_modelo_js.py) a partir de `Rajagopal_2015.osim`, incluido en las descargas de OpenSim 4.6.

Proyecto original: https://simtk.org/projects/full_body. Licencia: [MIT](LICENSE), © 2015 Stanford University.

Rajagopal, A., Dembia, C. L., DeMers, M. S., Delp, D. D., Hicks, J. L., & Delp, S. L. (2016). Full-body musculoskeletal model for muscle-driven simulation of human gait. *IEEE Transactions on Biomedical Engineering, 63*(10), 2068–2079.
