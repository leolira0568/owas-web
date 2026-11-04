# OWAS Web

Herramienta libre y de código abierto para analizar posturas de trabajo con el método **OWAS** (*Ovako Working posture Analysing System*). Hasta la versión 3.4 se llamaba *WinOWAS Web*.

El WinOWAS original era un programa de Windows 3.x de 16 bits (Visual Basic 3) que deja de funcionar a partir de Windows de 64 bits. Este proyecto lo reemplaza con **un solo archivo HTML**:

- Funciona sin instalación ni conexión a internet: se abre con doble clic en cualquier navegador moderno.
- Abre y guarda archivos **`.OWS` compatibles con el WinOWAS original**, así que los estudios existentes siguen sirviendo.
- Funciona en Windows, macOS, Linux, tabletas y celulares.
- Desde la versión 3.0 detecta posturas en fotos y videos con MediaPipe, incluido dentro del mismo archivo (pesa unos 28 MB).

**▶ Usar en línea:** https://leolira0568.github.io/owas-web/

## Funciones

Desde la versión 4.0 la interfaz es **una sola página, sin pestañas**: 1 · Proyecto, 2 · Observación, 3 · Resultados y 4 · Observaciones, una tras otra, con la ayuda al final. En la sección de observación, el video va primero, debajo el código de postura y «Aceptar postura», y debajo los códigos y la tarea. Los resultados se actualizan solos al guardar cada postura.


- **1 · Proyecto**: empresa, departamento, trabajo estudiado, observador, fecha, hora, intervalo de observación y tareas.
- **2 · Observación**, en tres modos. En todos, la postura se elige con pictogramas o con el teclado (`2341` + Enter) y la categoría de acción se ve al instante.
  - **En vivo**: reloj con aviso sonoro en cada intervalo.
  - **Video** *(nuevo en 2.0)*: carga un video MP4 o WebM y lo revisa fotograma a fotograma, segundo a segundo o saltando a cada instante de muestreo según el intervalo. Al aceptar, el fotograma se guarda como imagen de la observación y queda marcado con su color de categoría en la barra de tiempo.
  - **Fotografías** *(nuevo en 2.0)*: carga varias fotos y registra una observación por foto, con su imagen.
- **Detección automática de posturas** *(nuevo en 3.0)*: en los modos Video y Fotografías, **Detectar postura** (tecla `D`) localiza a la persona con [MediaPipe Pose](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker), dibuja su esqueleto y propone los dígitos de espalda, brazos y piernas, con los ángulos medidos. La carga se elige siempre a mano. Puede detectar automáticamente al llegar a cada muestra o foto. La lista marca cada código como «auto» (aceptado) o «corregido», y los resultados muestran la concordancia por parte del cuerpo. Los umbrales se pueden ajustar.
- **Imágenes** *(nuevo en 2.0)*: miniaturas en la lista de observaciones, galería ordenada por riesgo en los resultados, visor ampliado con salto al momento del video, e impresión de las imágenes en el informe.
- **Categorías de acción**: distribución en las categorías 1–4 con sus recomendaciones, desglose por tarea y posturas agrupadas por categoría.
- **Por parte del cuerpo**: porcentaje del tiempo en cada postura de espalda, brazos y piernas, comparado con los límites de cada categoría.
- **Tablas y figuras en formato APA (7.ª edición)** *(nuevo en 3.1)*: número en negrita, título en cursiva, tablas solo con líneas horizontales, «Nota.» con el tamaño de la muestra y referencia a Karhu et al. (1977). Numeración correlativa en todo el informe:
  - *Categorías de acción*: distribución por categoría (tabla y figura), distribución por tarea (tabla y figura, si hay varias tareas) y frecuencia de los códigos de postura.
  - *Por parte del cuerpo*: frecuencia de cada postura con su categoría (tabla y figura). Las tablas de concordancia y de mediciones de la detección automática se muestran solo si se activa «Mostrar tablas de la detección automática».
  - Se incluyen en la impresión con la casilla «Incluir tablas y figuras APA al imprimir».
- **Archivos**: abrir, guardar, guardar como y unir archivos `.OWS` (solo datos, compatibles con el original) y proyectos `.owsp` (datos más imágenes).
- **Imprimir o guardar en PDF**, y copiar los resultados al portapapeles (se pegan como tabla en Excel o Word).
- **Exportar resultados** *(nuevo en 3.14)*: a **Word** (`.doc`, con la información general, las tablas y figuras APA y las imágenes de las observaciones; desde Word puede guardarse como `.docx`) o a **PDF** (mediante «Guardar como PDF» en el diálogo de impresión).
- **Exportar a OpenSim** *(nuevo en 4.6)*: guarda las posturas detectadas como marcadores 3D en un archivo `.trc` y, desde la versión 4.7, calcula en la propia aplicación los ángulos articulares en un archivo `.mot`, sin instalar OpenSim ni Python. Ver [Análisis en OpenSim](#análisis-en-opensim).
- **Autoguardado** en el navegador para no perder trabajo.
- **Tema claro u oscuro** *(nuevo en 3.9)*: botón en la barra superior; la elección se recuerda en el navegador. Por defecto se usa el tema claro.

## Privacidad y seguridad

Todo se procesa en el equipo: la aplicación no envía datos a ningún servidor y una política de seguridad de contenido bloquea las conexiones de red. Los rostros se difuminan en las imágenes guardadas, el autoguardado puede desactivarse y los datos locales pueden borrarse desde la ayuda. Ver la [declaración de privacidad y seguridad](PRIVACIDAD.md).

## Cómo usarlo sin internet

1. Descarga [`OWASWeb.html`](OWASWeb.html) (botón *Download raw file* en GitHub) o el archivo de la [última versión publicada](https://github.com/leolira0568/owas-web/releases/latest).
2. Ábrelo con doble clic. Con Edge o Chrome, *Guardar* sobrescribe directamente el archivo `.OWS` abierto. En otros navegadores, el archivo se descarga.

En la carpeta [`ejemplos/`](ejemplos/) hay un estudio de muestra para probar.

## Método OWAS

Cada observación se codifica con cuatro dígitos:

| Dígito | Parte | Códigos |
|---|---|---|
| 1 | Espalda | 1 recta · 2 inclinada · 3 girada · 4 inclinada y girada |
| 2 | Brazos | 1 ambos bajo el hombro · 2 uno sobre el hombro · 3 ambos sobre el hombro |
| 3 | Piernas | 1 sentado · 2 de pie, piernas rectas · 3 de pie, una pierna recta · 4 de pie, rodillas flexionadas · 5 de pie, una rodilla flexionada · 6 arrodillado · 7 caminando |
| 4 | Carga | 1 < 10 kg · 2 10–20 kg · 3 > 20 kg |

| Categoría | Significado |
|---|---|
| 1 | Postura normal. No se requieren acciones. |
| 2 | Se requieren acciones correctivas en un futuro cercano. |
| 3 | Se requieren acciones correctivas lo antes posible. |
| 4 | Se requieren acciones correctivas inmediatamente. |

## Cómo se calcula la propuesta automática

Se usan los 33 puntos 3D que estima MediaPipe Pose (en metros, con origen entre las caderas). Los umbrales por defecto se pueden cambiar en *Ajustes de detección*:

| Parte | Regla |
|---|---|
| Espalda | **Inclinada** si el tronco (de caderas a hombros) forma 20° o más con la vertical en el plano sagital. **Girada** si la línea de hombros y la de caderas difieren 20° o más en el plano horizontal, o si el tronco se inclina de lado 20° o más. |
| Brazos | Número de brazos con el codo o la muñeca por encima del hombro, más uno. |
| Piernas | **Arrodillado** si una rodilla está cerca del suelo. **Sentado** si ambos muslos están casi horizontales y la cadera está baja. **Una pierna** si un pie está levantado al menos un 10 % de la longitud de la pierna; con la rodilla de apoyo por debajo de 150°, flexionada. **Ambas piernas** con alguna rodilla por debajo de 150°: flexionadas. **Caminando** (solo video) si la cadera se desplaza al menos un 25 % del tronco en 0,5 s. |

En video, los puntos del cuerpo se promedian entre el fotograma elegido y sus vecinos a ±0,1 s (se puede desactivar). Las partes que el usuario elige a mano en un fotograma no se cambian con la detección.

La detección es una ayuda y no reemplaza el criterio de quien observa. Funciona mejor con una sola persona de cuerpo entero, vista de lado o en diagonal. El giro de la espalda es la medida menos fiable desde una sola cámara.

## Análisis en OpenSim

*Exportar resultados → OpenSim (.trc)* guarda las posturas aceptadas que tienen detección automática: 19 marcadores en metros, con los ejes de OpenSim (X adelante, Y arriba, Z derecha) y los pies en el suelo. Cada fila es una postura independiente, no un movimiento continuo.

### Ángulos en la aplicación

*Exportar resultados → OpenSim (.mot)* calcula los ángulos articulares en el navegador, sin instalar nada, con la cinemática del modelo Rajagopal 2015 incluida en el archivo. Antes de descargar, muestra qué posturas son poco fiables y por qué, y por defecto las excluye del archivo. También permite descargar la revisión de calidad (`.csv`) y el modelo con los 19 marcadores (`.osim`).

Para verlo en OpenSim: *File → Open Model* con `Rajagopal2015_OWAS.osim` y *File → Load Motion* con el `.mot`. El cálculo usa un modelo escalado a la persona, pero el `.osim` descargado tiene el tamaño estándar, por lo que el cuerpo no coincide exactamente con los marcadores. Para obtener un modelo escalado, usa el script.

La aplicación no ejecuta OpenSim: resuelve el mismo problema con su propio código. Se comparó con Inverse Kinematics de OpenSim 4.6 en un video real y en una persona simulada: las dos vías señalaron las mismas posturas y, en las posturas fiables del video, los ángulos difirieron como máximo 0,1° en el tronco, 1,4° en la cadera y 1,1° en la rodilla. En los brazos llegaron a 3,7°, porque la aplicación mantiene cerca de la posición neutra los giros que los marcadores no pueden medir (`arm_rot` y `pro_sup`). Esos giros no tienen valor de medición en ninguna de las dos vías.

### Script para OpenSim

El script [`herramientas/trc_a_opensim.py`](herramientas/trc_a_opensim.py) usa OpenSim para vincular el `.trc` a un modelo y calcular los ángulos articulares:

```
pip install opensim
python herramientas/trc_a_opensim.py "estudio - posturas.trc" --modelo Rajagopal_2015.osim
```

El script gira cada fotograma para que las caderas miren hacia delante, escala el modelo, coloca los marcadores en sus articulaciones y ejecuta Inverse Kinematics. El modelo debe tener los cuerpos de Rajagopal 2015, incluido en las descargas de OpenSim (en Windows lo busca en la instalación de `opensim-core` 4.6). Genera estos archivos:

| Archivo | Contenido |
|---|---|
| `*_modelo.osim` | Modelo escalado con los 19 marcadores |
| `*_ik.mot` | Ángulos articulares de cada postura |
| `*_calidad.csv` | Inclinación del tronco, error de los marcadores y fotogramas poco fiables, con el motivo |
| `*_alineado.trc` | Marcadores girados, usados por Inverse Kinematics |
| `*_ik_errores.sto` | Error de los marcadores en cada fotograma |

La inclinación del tronco es `tronco_grados` en `*_calidad.csv` (positiva hacia delante) y equivale a `pelvis_tilt` con el signo cambiado. La extensión lumbar queda bloqueada porque, sin marcadores en la pelvis, no se puede distinguir de la inclinación de la pelvis.

### Límites

Las dos vías son **experimentales**. Se probaron con una persona simulada y con un solo video real de 22 segundos, sin compararla con un sistema de captura de movimiento:

- En ese video, la inclinación del tronco coincidió con los marcadores en la mayoría de los fotogramas, pero **los ángulos de rodilla no fueron fiables** y la revisión de calidad no los comprueba. Que la aplicación y OpenSim coincidan no significa que los ángulos sean correctos: ambas parten de los mismos puntos.
- Los puntos vienen de una sola cámara y la profundidad es la medida menos fiable. Las proporciones del cuerpo son aproximadas y no sirven como medidas antropométricas.
- Una detección errónea que parezca una postura creíble puede pasar la revisión de calidad. El script no elimina del archivo `.mot` los fotogramas señalados.
- Los límites de la revisión son valores de partida.

## Formato de archivo `.OWS`

Texto plano con codificación Windows-1252 y finales de línea CRLF:

```
!OWAS!
"Empresa"
"Departamento"
"Trabajo estudiado"
"Observador"
"dd/mm/aaaa"
"hh:mm"
 N                ← número de tareas (con un espacio antes y otro después)
"Tarea 1"         ← N nombres de tarea
...
30                ← intervalo en segundos
M                 ← número de observaciones
23330             ← M códigos: espalda, brazos, piernas, carga e índice de tarea (desde 0)
...
```

## Formato de proyecto `.owsp`

Los estudios con imágenes se guardan como JSON (UTF-8):

```json
{ "format": "winowas-proyecto", "version": 2,
  "S": { "bg": [...], "phases": [...], "interval": 30,
         "obs": [ { "b": 2, "a": 1, "l": 3, "w": 1, "p": 0,
                    "img": "data:image/jpeg;base64,...", "t": 12.5, "src": "video.mp4",
                    "det": "213" } ] } }
```

`img` es el fotograma o la foto (JPEG de 800 px como máximo), `t` el segundo del video, `src` el nombre del archivo de origen y `det` la propuesta automática de espalda, brazos y piernas, si la hubo (`0` en piernas significa que no se pudo detectar), y `dm` los ángulos medidos en grados: `trunk` (tronco), `twist` (giro), `side` (lateral), `armsUp` (brazos sobre el hombro), `kneeL` y `kneeR` (rodillas) y `walk` (desplazamiento en %). `w3` guarda los 33 puntos 3D de la detección en metros, para exportarlos a OpenSim. El video no se incluye en el proyecto. El identificador `winowas-proyecto` se conserva del nombre anterior para que los proyectos sigan siendo compatibles entre versiones.

## Desarrollo

El código editable está en [`src/OWASWeb.html`](src/OWASWeb.html). El archivo publicado `OWASWeb.html` se genera con:

```
python build.py
```

El script incrusta en base64 los archivos de [`vendor/mediapipe/`](vendor/mediapipe/) (MediaPipe Tasks Vision 0.10.35 y el modelo Pose Landmarker *full*) y de [`vendor/opensim/`](vendor/opensim/) (modelo Rajagopal 2015, generado con [`herramientas/generar_modelo_js.py`](herramientas/generar_modelo_js.py)). Para probar `src/OWASWeb.html` sin compilar, sírvelo con un servidor local (por ejemplo `python -m http.server`): en ese caso lee los archivos de `vendor/`.

## Versiones

- **4.7**: cálculo de los ángulos articulares en la propia aplicación y descarga del `.mot`, sin instalar OpenSim ni Python, con revisión de calidad antes de exportar y descarga del modelo con los marcadores; los códigos de espalda, brazos, piernas y carga se muestran en columnas.
- **[4.6](https://github.com/leolira0568/owas-web/releases/tag/v4.6)**: exportación de las posturas detectadas a OpenSim (`.trc`) y script experimental para calcular ángulos articulares con revisión de calidad de cada fotograma.
- **[4.5](https://github.com/leolira0568/owas-web/releases/tag/v4.5)**: declaración de privacidad y seguridad (ayuda, pie de página y [PRIVACIDAD.md](PRIVACIDAD.md)); política de seguridad de contenido sin conexiones de red; rostros difuminados en las imágenes guardadas; autoguardado desactivable y borrado de datos locales; estilo plano sin bordes inspirado en Windows 11.
- **[4.4](https://github.com/leolira0568/owas-web/releases/tag/v4.4)**: el aviso de «Aceptar postura» indica que la detección debe ser revisada por un profesional en Ergonomía.
- **[4.3](https://github.com/leolira0568/owas-web/releases/tag/v4.3)**: los códigos de espalda, brazos, piernas, carga y tarea se muestran debajo de «Aceptar postura», en una sola columna (nunca al lado del video).
- **[4.2](https://github.com/leolira0568/owas-web/releases/tag/v4.2)**: el código de postura y «Aceptar postura» se muestran debajo del video; a la derecha quedan solo los códigos.
- **[4.1](https://github.com/leolira0568/owas-web/releases/tag/v4.1)**: botón flotante para subir al inicio de la página; área de códigos y tareas más compacta.
- **[4.0](https://github.com/leolira0568/owas-web/releases/tag/v4.0)**: interfaz en una sola página, sin pestañas; video y códigos lado a lado en pantallas anchas; resultados y lista de observaciones actualizados al momento.
- **[3.18](https://github.com/leolira0568/owas-web/releases/tag/v3.18)**: los avisos de la detección (espalda, brazos, piernas) desaparecen al elegir el código de esa parte; la carga nunca queda preseleccionada y se avisa «Seleccione la carga» hasta elegirla.
- **[3.17](https://github.com/leolira0568/owas-web/releases/tag/v3.17)**: se quita el texto «Propuesta» con los ángulos bajo «Aceptar postura»; solo se muestran los avisos de la detección.
- **[3.16](https://github.com/leolira0568/owas-web/releases/tag/v3.16)**: observaciones en una sola fila bajo la línea de tiempo (número y riesgo en vertical); el aviso sobre la detección automática aparece al pasar el puntero sobre «Aceptar postura»; «Aceptar postura» destella con un aro amarillo aunque Windows tenga las animaciones desactivadas; «Postura guardada» en azul; botones de archivo y de tema solo con icono.
- **[3.15](https://github.com/leolira0568/owas-web/releases/tag/v3.15)**: detección promediada de 3 fotogramas cercanos; la detección ya no cambia las partes elegidas a mano; códigos y tareas en filas; las observaciones aparecen en la línea de tiempo bajo su fotograma; aviso de fotograma repetido y de revisión profesional; «Aceptar postura» parpadea cuando todo está elegido; «Nuevo proyecto» y «Abrir proyecto».
- **[3.14](https://github.com/leolira0568/owas-web/releases/tag/v3.14)**: la detección se activa al pausar el video o al elegir un fotograma; botón «Exportar resultados» (Word y PDF); la lista de posturas aceptadas muestra el número y el riesgo y lleva a su fotograma; mensaje «Postura guardada» al aceptar.
- **[3.13](https://github.com/leolira0568/owas-web/releases/tag/v3.13)**: todas las imágenes aparecen al imprimir; «Cargar video» y «Cargar fotografías» en gris oscuro hasta cargar; las advertencias se muestran junto a «Aceptar postura»; ninguna tarea elegida al empezar, con el aviso «Seleccione la tarea».
- **[3.12](https://github.com/leolira0568/owas-web/releases/tag/v3.12)**: las casillas de detección (detectar al llegar, subtítulos y grabar en la imagen) quedan dentro de «Ajustes de detección», ocultas por defecto y activadas.
- **[3.11](https://github.com/leolira0568/owas-web/releases/tag/v3.11)**: las fases de trabajo pasan a llamarse tareas; botón «Detectar postura»; la detección y sus ajustes se muestran encima del video o la foto.
- **[3.10](https://github.com/leolira0568/owas-web/releases/tag/v3.10)**: tema claro por defecto; encabezado gris neutro con «Imprimir resultados» en azul; las tablas de la detección automática (concordancia y mediciones) quedan ocultas por defecto.
- **[3.9](https://github.com/leolira0568/owas-web/releases/tag/v3.9)**: tema oscuro y claro a elección; archivo `OWASWeb.html`; concordancia con la detección automática oculta por defecto; botones «Aceptar postura» e «Imprimir resultados»; advertencias en rojo.
- **[3.8](https://github.com/leolira0568/owas-web/releases/tag/v3.8)**: botón «Aceptar» en verde; pie de página con el enlace a GitHub y las licencias; autor Leonardo Lira.
- **[3.7](https://github.com/leolira0568/owas-web/releases/tag/v3.7)**: el modo Video es el que aparece seleccionado al abrir la aplicación.
- **[3.6](https://github.com/leolira0568/owas-web/releases/tag/v3.6)**: en Observar, los modos aparecen en el orden Video, Fotografías y En vivo.
- **[3.5](https://github.com/leolira0568/owas-web/releases/tag/v3.5)**: el proyecto pasa a llamarse **OWAS Web** (archivo `OWASWeb.html`, repositorio `owas-web`).
- **[3.4](https://github.com/leolira0568/owas-web/releases/tag/v3.4)**: la tecla de atajo de los botones azules ya no parece una casilla vacía; las casillas de detección no recuperan un estado anterior al recargar.
- **[3.3](https://github.com/leolira0568/owas-web/releases/tag/v3.3)**: subtítulos con los datos de la detección debajo del video o la foto, grabados también en la imagen guardada; los datos aparecen en la galería, el visor y una nueva tabla APA de mediciones.
- **[3.2](https://github.com/leolira0568/owas-web/releases/tag/v3.2)**: «Detectar al llegar a cada muestra o fotografía» activado por defecto; también detecta al cargar un video.
- **[3.1](https://github.com/leolira0568/owas-web/releases/tag/v3.1)**: tablas y figuras en formato APA 7 en pantalla y en la impresión; botón «Detección automática de postura» destacado en azul.
- **[3.0](https://github.com/leolira0568/owas-web/releases/tag/v3.0)**: detección automática de posturas con MediaPipe, incluida en el archivo para funcionar sin internet.
- **[2.0](https://github.com/leolira0568/owas-web/releases/tag/v2.0)**: análisis por video fotograma a fotograma y por fotografías, con una imagen por observación y el formato `.owsp`.
- **[1.0](https://github.com/leolira0568/owas-web/releases/tag/v1.0)**: observación en vivo, compatible con `.OWS`.

## Aviso

Este proyecto es una reimplementación independiente. No está afiliado a la Universidad Tecnológica de Tampere ni a los autores del WinOWAS original, y no incluye ninguna parte de su programa. Las tablas de clasificación corresponden al método OWAS publicado, tal como las usaba el WinOWAS original.

Los resultados son una ayuda para la evaluación ergonómica y no sustituyen el criterio de un profesional.

## Licencia

[MIT](LICENSE) © 2026 Leonardo Lira

Los iconos de la interfaz están basados en [Lucide](https://lucide.dev) (licencia ISC, © Lucide Contributors). Los pictogramas de postura son propios del proyecto.

`OWASWeb.html` incluye MediaPipe Tasks Vision y el modelo Pose Landmarker, © Google LLC, bajo la [licencia Apache 2.0](vendor/mediapipe/LICENSE). Ver [`vendor/mediapipe/README.md`](vendor/mediapipe/README.md).

También incluye datos derivados del modelo Rajagopal 2015, © 2015 Stanford University, bajo [licencia MIT](vendor/opensim/LICENSE). Ver [`vendor/opensim/README.md`](vendor/opensim/README.md).
