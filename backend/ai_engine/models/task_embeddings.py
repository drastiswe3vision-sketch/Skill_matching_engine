
"""
task_embeddings.py

Generate task embeddings and save them to Supabase.
"""

from backend.ai_engine.data.tasks import get_pending_tasks
from backend.ai_engine.utils.text_builder import build_task_text
from backend.ai_engine.services.embedding_service import generate_embedding
from backend.ai_engine.services.vector_storage_service import save_task_vector


def generate_task_embeddings():

    # Fetch latest pending tasks
    tasks = get_pending_tasks()

    print("\nGenerating Task Embeddings...\n")

    for task in tasks:

        # Convert task into text
        text = build_task_text(task)

        # Generate embedding
        embedding = generate_embedding(text)

        # Get task ID
        task_id = task["id"]

        # Save embedding to Supabase
        save_task_vector(
            task_id,
            task["title"],
            embedding
        )

        print(f"[SUCCESS] {task.get('title')}")

        # Release local references
        del embedding
        del text

    # Release fetched task list
    del tasks
