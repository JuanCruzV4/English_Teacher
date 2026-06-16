# English Teacher con IA

Aplicación web hecha con Gradio para aprender inglés de forma práctica. Permite ingresar una palabra, frase hecha, phrasal verb o expresión en inglés y recibe una explicación en español con formato Markdown.

## Qué hace

- Analiza expresiones en inglés y devuelve una explicación clara en español.
- Usa Gemini como modelo principal.
- Si Gemini no responde o se agota la cuota, hace fallback automático a Ollama con `llama3.2:1b`.
- Muestra la respuesta en una interfaz web sencilla.

## Requisitos

- Python 3.13 o compatible con la versión de tus dependencias.
- Una API key válida de Gemini en la variable `GOOGLE_API_KEY`.
- Ollama instalado y ejecutándose localmente si quieres usar el fallback.

## Instalación

1. Crea y activa tu entorno virtual.
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con estas variables:

```env
GOOGLE_API_KEY=tu_api_key_de_gemini
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_API_KEY=ollama
```

`OLLAMA_BASE_URL` y `OLLAMA_API_KEY` son opcionales, pero útiles si quieres cambiar la URL o mantener la configuración explícita.

## Uso

Ejecuta la aplicación con:

```bash
python main.py
```

Luego abre la URL local que aparece en la terminal.

## Estructura del proyecto

- `main.py`: lógica de la interfaz y conexión con los modelos.
- `requirements.txt`: dependencias del proyecto.

## Notas

- La interfaz está pensada para escribir una sola expresión por vez.
- Si Gemini no está disponible o supera la cuota, la app intenta usar Ollama automáticamente.
