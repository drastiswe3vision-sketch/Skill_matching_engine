
"""
vector_fetch_service.py

Fetch employee and pending task embeddings
using memory-efficient NumPy arrays.
"""

import ast
import numpy as np

from database.supabase_client import supabase


def convert_embedding(embedding):

    if isinstance(embedding, str):
        embedding = ast.literal_eval(embedding)

    return np.asarray(embedding, dtype=np.float32)


# --------------------------------------------------------
# Fetch Employee Vectors
# --------------------------------------------------------

def get_employee_vectors():

    response = (
        supabase
        .table("employee_vector")
        .select("emp_id, embedding")
        .execute()
    )

    employee_vectors = response.data or []

    for employee in employee_vectors:

        employee["embedding"] = convert_embedding(
            employee["embedding"]
        )

    print(
        f"[SUCCESS] Employee vectors loaded: "
        f"{len(employee_vectors)}"
    )

    return employee_vectors


# --------------------------------------------------------
# Fetch Pending Task Vectors
# --------------------------------------------------------

def get_task_vectors():

    pending_response = (
        supabase
        .table("tasks")
        .select("id")
        .eq("status", "Pending")
        .execute()
    )

    pending_tasks = pending_response.data or []

    if not pending_tasks:
        print("[INFO] No pending tasks found.")
        return []

    pending_ids = [
        task["id"]
        for task in pending_tasks
    ]

    vector_response = (
        supabase
        .table("task_vector")
        .select("task_id, task_title, embedding")
        .in_("task_id", pending_ids)
        .execute()
    )

    task_vectors = vector_response.data or []

    for task in task_vectors:

        task["embedding"] = convert_embedding(
            task["embedding"]
        )

    print(
        f"[SUCCESS] Task vectors loaded: "
        f"{len(task_vectors)}"
    )

    return task_vectors
