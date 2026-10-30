# StoryKeeper — RAG para continuidad narrativa

Prototipo académico que utiliza embeddings, una base vectorial y un modelo generativo local para recuperar información de una novela y analizar posibles errores de continuidad.

## Tecnologías

- Python 3.13
- Ollama
- `gemma3:4b` para generar respuestas
- `nomic-embed-text` para crear embeddings
- ChromaDB para almacenar y recuperar fragmentos

## 1. Requisitos

Instala Ollama y descarga los dos modelos:

```powershell
ollama pull gemma3:4b
ollama pull nomic-embed-text
```

Comprueba que Ollama está funcionando:

```powershell
ollama list
```

## 2. Preparar el entorno

Desde la carpeta del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si PowerShell bloquea la activación del entorno, puedes ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## 3. Indexar la documentación

```powershell
python main.py index
```

El programa lee `data/novel_notes.md`, divide el contenido en fragmentos, genera sus embeddings y los almacena en ChromaDB dentro de `.chroma/`.

Cada vez que modifiques las notas de la novela, vuelve a ejecutar el comando `index`.

## 4. Consultar la continuidad

```powershell
python main.py ask
```

La aplicación solicitará una escena. También puedes pasarla directamente:

```powershell
python main.py ask --scene "Larrubia dejó el bastón y salió corriendo detrás de Chupete."
```

El agente:
1. Genera un embedding de la consulta.
2. Recupera los fragmentos semánticamente más relacionados.
3. Construye un prompt con la escena y los fragmentos recuperados.
4. Pide a Gemma que analice la continuidad sin inventar información.
5. Muestra los fragmentos utilizados como fuentes.

## 5. Estructura

```text
storykeeper-rag/
├── data/
│   └── novel_notes.md
├── storykeeper/
│   ├── __init__.py
│   ├── config.py
│   ├── knowledge_base.py
│   └── agent.py
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Alcance y limitaciones

Este prototipo demuestra el flujo RAG, pero no garantiza que el modelo detecte todas las contradicciones. La recuperación semántica puede no encontrar un dato relevante o puede recuperar fragmentos que no sean suficientes. El modelo también puede interpretar mal la escena.

Para evaluar el sistema, conviene preparar escenas con contradicciones conocidas y comprobar si recupera la información correcta y si su análisis coincide con una revisión humana. La decisión narrativa final corresponde al escritor.

## Subirlo a GitHub

Crea un repositorio vacío en GitHub y, desde esta carpeta, ejecuta:

```powershell
git init
git add .
git commit -m "Primera versión de StoryKeeper con RAG y embeddings"
git branch -M main
git remote add origin https://github.com/USUARIO/storykeeper-rag.git
git push -u origin main
```

Sustituye la URL por la de tu repositorio.
