# Declaración de privacidad y seguridad de OWAS Web

OWAS Web está diseñada para proteger los datos de los estudios ergonómicos y la identidad de las personas que aparecen en los videos y las fotografías que se analizan.

## Qué datos maneja la aplicación

- Los datos del estudio que escribe el usuario: empresa, departamento, trabajo estudiado, observador, fecha, hora, intervalo y tareas.
- Las observaciones: códigos OWAS, tarea, momento del video y, si se activa, la propuesta y los ángulos de la detección automática.
- Los videos y las fotografías que el usuario abre, y las imágenes de cada observación (fotogramas o fotos). Pueden mostrar rostros y otros rasgos que identifican a una persona.

## Dónde se procesan

- **Todo se procesa en el equipo del usuario**, dentro del navegador. La aplicación no envía datos a ningún servidor, no usa cookies, ni herramientas de analítica, ni servicios externos.
- La detección de posturas usa MediaPipe Pose, que va **incluido dentro del archivo** y se ejecuta localmente.
- Los videos y las fotografías se abren desde el equipo y **nunca se suben a internet**. El video original no se copia en el proyecto.

## Medidas de seguridad

1. **Sin conexiones de red.** La aplicación incluye una política de seguridad de contenido (Content Security Policy) que impide conectarse a servidores externos, enviar formularios y cargar código de otros sitios.
2. **Rostros difuminados.** La opción «Difuminar el rostro en las imágenes guardadas» (activada por defecto) pixela la cabeza de la persona detectada en las imágenes de las observaciones, los informes y los proyectos. Solo funciona cuando la detección encuentra a la persona, por lo que conviene revisar cada imagen antes de compartirla.
3. **Sin metadatos.** Las imágenes guardadas se vuelven a codificar, por lo que no conservan datos como la ubicación GPS o el modelo de la cámara.
4. **Autoguardado opcional.** El trabajo se guarda automáticamente en el navegador del equipo para no perderlo. En equipos compartidos puede desactivarse en *Ayuda → Privacidad y seguridad*.
5. **Borrado de datos locales.** El botón «Borrar los datos guardados en este navegador» elimina el autoguardado y las preferencias de la aplicación y cierra el estudio abierto.
6. **Sin referencias externas.** La aplicación no envía la dirección de la página al abrir enlaces (`no-referrer`).

## Dónde quedan los datos

- En el **autoguardado del navegador** del equipo, hasta que el usuario lo borre o lo desactive.
- En los **archivos que el usuario guarda o exporta**: proyectos `.owsp`, archivos `.OWS`, documentos de Word (`.doc`) y PDF. Los proyectos y los informes con imágenes contienen datos personales.

## Versión en línea

La versión en línea se sirve desde GitHub Pages. GitHub puede registrar datos técnicos de la visita, como la dirección IP, según su [declaración de privacidad](https://docs.github.com/es/site-policy/privacy-policies/github-general-privacy-statement). Los datos del estudio, los videos y las fotografías no se envían. Para la máxima privacidad, descargue `OWASWeb.html` y úselo sin conexión.

## Protocolo recomendado para quien realiza el estudio

1. Informar a las personas observadas del propósito del estudio y obtener su consentimiento antes de grabar o fotografiar.
2. Grabar solo lo necesario para el análisis y, si es posible, encuadrar el cuerpo sin mostrar el rostro.
3. Mantener activado el difuminado de rostros y revisar las imágenes antes de compartir un informe.
4. Evitar nombres de personas en los datos del estudio y en las tareas cuando no sean necesarios.
5. Guardar proyectos, informes y videos en carpetas protegidas o cifradas (por ejemplo, con BitLocker) y compartirlos solo por medios seguros con quien deba verlos.
6. En equipos compartidos, desactivar el autoguardado y borrar los datos del navegador al terminar.
7. Eliminar los videos, fotografías y proyectos cuando ya no sean necesarios, y cumplir la normativa de protección de datos personales del país en que se realiza el estudio.

## Responsabilidad

Quien realiza el estudio es responsable del tratamiento de los datos que recoge. El autor de OWAS Web no recibe ningún dato de la aplicación. Para dudas o sugerencias, abra un *issue* en el [repositorio del proyecto](https://github.com/leolira0568/owas-web/issues).

Esta declaración describe el funcionamiento técnico de la aplicación y no constituye asesoría legal.
