import argparse
from pathlib import Path

from storykeeper.agent import ContinuityAgent
from storykeeper.knowledge_base import KnowledgeBase

DATA_FILE = Path(__file__).resolve().parent / "data" / "novel_notes.md"


def run_index():
    knowledge_base = KnowledgeBase()
    total = knowledge_base.index_document(DATA_FILE)
    print(f"\n[OK] Se han indexado {total} fragmentos.")
    print("La base vectorial está preparada para realizar consultas.")


def run_ask(scene: str | None):
    if not scene:
        print("Introduce la escena que quieres revisar.")
        print("Finaliza la entrada escribiendo una línea con SOLO: FIN\n")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "FIN":
                break
            lines.append(line)
        scene = "\n".join(lines).strip()

    if not scene:
        print("No se ha introducido ninguna escena.")
        return

    knowledge_base = KnowledgeBase()
    agent = ContinuityAgent(knowledge_base)

    print("\nBuscando información relacionada en la base de conocimiento...")
    answer, sources = agent.review_scene(scene)

    print("\n" + "=" * 65)
    print("ANÁLISIS DE STORYKEEPER")
    print("=" * 65)
    print(answer)

    print("\n" + "-" * 65)
    print("FRAGMENTOS RECUPERADOS (fuentes utilizadas)")
    print("-" * 65)
    for item in sources:
        print(
            f"\n[Fragmento {item['chunk']}] "
            f"Distancia: {item['distance']:.3f} | Fuente: {item['source']}"
        )
        print(item["text"])


def main():
    parser = argparse.ArgumentParser(
        description="StoryKeeper: revisión de continuidad narrativa con RAG."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("index", help="Indexa las notas de continuidad.")

    ask_parser = subparsers.add_parser("ask", help="Analiza una escena.")
    ask_parser.add_argument(
        "--scene",
        type=str,
        help="Escena que se desea revisar. Si se omite, se solicita por terminal.",
    )

    args = parser.parse_args()

    if args.command == "index":
        run_index()
    elif args.command == "ask":
        run_ask(args.scene)


if __name__ == "__main__":
    main()
