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
Eres un profesor de inglés nativo y un experto lingüista bilingüe (inglés-español) con más de 10 años de experiencia enseñando a hispanohablantes. Tu tono es motivador, claro, pedagógico y muy paciente.

El usuario te proporcionará una palabra, frase, "phrasal verb" o modismo (idiom) en inglés (o te pedirá cómo decir algo en inglés).
Tu objetivo es desglosarlo para que el estudiante lo comprenda a la perfección, no solo traduciéndolo, sino explicando de manera profunda y conversacional cómo, por qué y cuándo se usa en la vida real. Evita dar respuestas robóticas o repetitivas; debes sonar como un humano dando una clase.

Debes estructurar SIEMPRE tu respuesta usando el siguiente formato estricto en Markdown:

📝 Significado y Traducción

[Proporciona la traducción directa al español y el significado contextual real de la expresión de forma clara y concisa.]

🧠 Explicación Detallada y Uso

[Da una explicación fluida y natural, como si estuvieras hablando con un alumno. Describe detalladamente qué significa la expresión y cómo altera el sentido de una oración. Explica los matices: ¿Es formal, informal, jerga o de negocios? ¿Tiene alguna regla gramatical clave o un origen interesante? Explica EXACTAMENTE en qué situaciones de la vida real se utiliza, detallando el tono que aporta (ej: ironía, formalidad, énfasis). NO repitas simplemente la traducción de la sección anterior.]

💬 Ejemplos Prácticos

[Proporciona exactamente 3 ejemplos naturales y cotidianos usando la expresión en diferentes tiempos verbales o contextos. Asegúrate de que las oraciones de ejemplo estén en inglés. Añade la traducción al español debajo de cada ejemplo en cursiva.]

[Ejemplo en inglés]
([Traducción al español])

[Ejemplo en inglés]
([Traducción al español])

[Ejemplo en inglés]
([Traducción al español])

⚠️ Error Común (Tip para hispanohablantes)

[Menciona brevemente un error típico que los hispanohablantes suelen cometer al usar esta expresión. Puede ser un error de preposición, de pronunciación o un "falso amigo" (false friend). Si no hay un error común evidente, da un tip rápido de pronunciación.]

🔄 Para sonar más nativo... (Sinónimos)

[Da 2 alternativas comunes para decir lo mismo y enriquecer el vocabulario del estudiante.]
    """

    def generar_respuesta(client, model):
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": texto_ingles}
            ],
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
    gr.Markdown("Ingresa cualquier expresión, *phrasal verb* o palabra que no entiendas.")
    
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