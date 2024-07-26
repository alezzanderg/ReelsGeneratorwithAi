### README

# Generador de Videos Motivacionales para Shorts/Reels/TikToks con AI

Este proyecto genera videos motivacionales dirigidos a personas que quieren ser millonarios. Utiliza las APIs de OpenAI, ElevenLabs y Pexels para generar mensajes motivacionales, convertirlos a audio, descargar videos de fondo y añadir subtítulos sincronizados.

## Requisitos

- Python 3.7 o superior
- Claves API de OpenAI, ElevenLabs y Pexels
- Librerías de Python necesarias (ver Instalación)
- [ImageMagick-7.1.1-Q16-HDRI](https://imagemagick.org/script/download.php) instalado y configurado

## Instalación

1. **Clonar el repositorio:**

```bash
git clone <URL del repositorio>
cd <nombre del repositorio>
```

2. **Crear un entorno virtual:**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar las dependencias:**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**

Copiar el archivo `.env.example` a `.env` y agregar tus claves API:

```bash
cp .env.example .env
```

Editar el archivo `.env` y añadir tus claves API:

```env
OPENAI_API_KEY=tu-api-key-openai
ELEVENLABS_API_KEY=tu-api-key-elevenlabs
PEXELS_API_KEY=tu-api-key-pexels
```

5. **Instalar y configurar ImageMagick**

Descargar e instalar [ImageMagick-7.1.1-Q16-HDRI](https://imagemagick.org/script/download.php). Asegúrate de añadir ImageMagick al PATH durante la instalación.

6. **Desinstalar Pillow 10 e instalar Pillow 9.5.0**

Pillow 10 tiene un problema con `ANTIALIAS`, por lo que se recomienda desinstalarlo e instalar la versión 9.5.0:

```bash
pip uninstall Pillow
pip install Pillow==9.5.0
```

7. **Crear las carpetas necesarias:**

```bash
mkdir contenido
```

## Ejecución

Ejecutar el script para generar un video motivacional:

```bash
python generate_video.py
```

## Funcionalidades

1. **Generar Mensaje Motivacional:**
   - Utiliza la API de OpenAI para generar un mensaje motivacional dirigido a personas que quieren ser millonarios.
   - Guarda el mensaje en un archivo de texto en una carpeta con la fecha y hora actual.

2. **Convertir Texto a Voz:**
   - Utiliza la API de ElevenLabs para convertir el mensaje de texto a un archivo de audio.
   - Nota: Actualmente el script usa el ID de voz "eleven_multilingual_v2". Para usar otras voces, puedes utilizar los siguientes IDs de voz:
     - **George**: `"voice_id": "JBFqnCBsd6RMkjVDRZzb"`
     - **Callum**: `"voice_id": "N2lVS1w4EtoT3dr4eOWO"`
   - Se recomienda usar las siguientes configuraciones de variables para una voz más fluida y menos robótica:
     ```json
     {
         "text": text,
         "model_id": "eleven_multilingual_v2", 
         "voice_settings": {
             "stability": 0.50,
             "similarity_boost": 0.75,
             "style": 0.00,
             "use_speaker_boost": True
         }
     }
     ```

3. **Descargar Videos de Pexels:**
   - Utiliza la API de Pexels para descargar videos de fondo.

4. **Obtener Duración del Audio:**
   - Obtiene la duración del archivo de audio generado.

5. **Verificar Duración de los Videos:**
   - Selecciona videos de fondo hasta que la duración total sea al menos 4 segundos mayor que la duración del audio.

6. **Aplicar Opacidad y Aspecto:**
   - Ajusta cada video seleccionado a una opacidad del 50% y una resolución de 9:16 (608x1080).

7. **Combinar Videos y Añadir Audio:**
   - Combina los videos y añade el audio, asegurando que comience en el segundo 2 del video.

8. **Transcribir el Audio:**
   - Transcribe el audio utilizando `SpeechRecognition` y genera subtítulos sincronizados.
   - Nota: Esta funcionalidad no está completamente finalizada. Se recomienda buscar o implementar una librería que capture el texto y lo adapte al audio de manera más precisa.

9. **Añadir Subtítulos al Video:**
   - Añade los subtítulos generados al video combinado.

10. **Renderizar el Video Combinado:**
    - Renderiza el video combinado y lo guarda en una carpeta con la fecha y hora actual.

11. **Simulación de la Duración del Audio en el Video:**
    - Imprime la duración del audio desde el segundo 2 hasta el segundo correspondiente, asegurando que termine 2 segundos antes del final del video.

## Mejoras Futuras

Este proyecto no está completamente finalizado y puede mejorarse. Algunas ideas de mejoras incluyen:

- Optimizar la sincronización de subtítulos.
- Mejorar la selección de videos de fondo.
- Añadir más configuraciones personalizables.
- Asegurar una mayor estabilidad y manejo de errores.

Si deseas mejorar este proyecto, siéntete libre de clonar el repositorio y hacer tus modificaciones. Por favor, comparte tus mejoras para que otros también puedan beneficiarse.

## Contribuciones

Si haces mejoras al proyecto, te animamos a compartir tus cambios. Puedes hacerlo a través de un pull request o compartiendo tu repositorio modificado.

## Documentación de APIs Utilizadas

- [OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
- [ElevenLabs API](https://elevenlabs.io/docs/introduction)
- [Pexels API](https://www.pexels.com/api/documentation/)

---

### `.env.example`

```env
# Reemplaza los valores de abajo con tus claves API
OPENAI_API_KEY=tu-api-key-openai
ELEVENLABS_API_KEY=tu-api-key-elevenlabs
PEXELS_API_KEY=tu-api-key-pexels
```

