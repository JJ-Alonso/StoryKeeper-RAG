import ollama

from storykeeper.config import GENERATION_MODEL
from storykeeper.knowledge_base import KnowledgeBase


class ContinuityAgent:
    """Agente que analiza una escena usando únicamente el contexto recuperado."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    def review_scene(self, scene: str) -> tuple[str, list[dict]]:
        retrieved = self.knowledge_base.retrieve(scene)

        context = "\n\n".join(
            f"[Fragmento {item['chunk']} | distancia {item['distance']:.3f}]\n"
            f"{item['text']}"
            for item in retrieved
        )

        prompt = f"""
Eres StoryKeeper, un asistente especializado en revisar la continuidad
de novelas y relatos extensos.

Tu tarea es analizar la escena y contrastarla con los hechos establecidos
en la documentación recuperada.

Reglas:
- Utiliza únicamente los datos del contexto recuperado.
- No inventes hechos, relaciones, lesiones ni acontecimientos.
- Distingue entre una contradicción confirmada y una posible incoherencia.
- Si los fragmentos no permiten llegar a una conclusión, dilo expresamente.
- No consideres que la ausencia de información demuestra una contradicción.
- No reescribas la escena; céntrate en el análisis.

DOCUMENTACIÓN RECUPERADA:
{context}

ESCENA QUE SE QUIERE REVISAR:
{scene}

Responde con estos apartados:
1. Resultado general: coherente, posible incoherencia o contradicción.
2. Información de la documentación relacionada con la escena.
3. Problemas detectados y explicación.
4. Información que sería necesario consultar para confirmar dudas.
"""

        response = ollama.chat(
            model=GENERATION_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0,
                "num_predict": 350,
            },
        )

        return response["message"]["content"], retrieved
