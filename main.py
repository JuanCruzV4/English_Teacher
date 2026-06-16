import os
import gradio as gr
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv

load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')

cliente = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=google_api_key
)

cliente_ollama = OpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("OLLAMA_API_KEY", "ollama")
)


def analizar_ingles(texto_ingles):
    accion = "Explicar significado"
   
    if not texto_ingles.strip():
        yield "Por favor, ingresa una palabra o frase primero."
        return

    system_prompt = f"""
    Eres un profesor de inglés nativo y experto lingüista bilingüe (inglés-español).
    El usuario te va a proporcionar una palabra, frase hecha (idiom), phrasal verb o expresión en inglés.
    
    Tu tarea estricta es realizar la siguiente acción solicitada por el usuario: "{accion}".
    
    Reglas:
    - Responde siempre en español (salvo los ejemplos en inglés).
    - Usa formato Markdown para que la respuesta sea fácil de leer (usa negritas, viñetas, etc.).
    - Sé claro, directo y educativo.
    """

    def generar_respuesta(client, model):
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": texto_ingles}
            ],
            temperature=0.5,
            stream=True
        )

        resultado_completo = ""

        for chunk in stream:
            if chunk.choices[0].delta.content:
                resultado_completo += chunk.choices[0].delta.content
                yield resultado_completo

    try:
        yield from generar_respuesta(cliente, "gemini-2.5-flash")
    except RateLimitError:
        try:
            yield from generar_respuesta(cliente_ollama, "llama3.2:1b")
        except Exception as error:
            yield f"Gemini agotó la cuota y Ollama no respondió correctamente: {error}"
    except Exception:
        try:
            yield from generar_respuesta(cliente_ollama, "llama3.2:1b")
        except Exception as error:
            yield f"No se pudo consultar Gemini ni Ollama: {error}"

with gr.Blocks() as aplicacion:
    
    gr.Markdown("# Tu Profesor de Inglés con IA")
    gr.Markdown("Ingresa cualquier expresión, *phrasal verb* o palabra que no entiendas y elige qué necesitas saber.")
    
    with gr.Row():
        
        with gr.Column(scale=1):
            input_texto = gr.Textbox(
                label="Palabra o Expresión en Inglés", 
                placeholder="Ej: piece of cake, get along, nevertheless...",
                lines=2
            )
            
            boton_analizar = gr.Button("Analizar", variant="primary")
            
        with gr.Column(scale=2):
            salida_resultado = gr.Markdown(label="Respuesta del Profesor")
            
    boton_analizar.click(
        fn=analizar_ingles, 
        inputs=[input_texto], 
        outputs=salida_resultado
    )

if __name__ == "__main__":
    aplicacion.launch(theme=gr.themes.Soft())