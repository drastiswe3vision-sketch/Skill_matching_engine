
"""
employee_embeddings.py

Generate employee embeddings and save them to Supabase.
"""

import gc

from backend.ai_engine.data.employees import employees
from backend.ai_engine.utils.text_builder import build_employee_text
from backend.ai_engine.services.embedding_service import generate_embedding
from backend.ai_engine.services.vector_storage_service import save_employee_vector


def generate_employee_embeddings():

    print("\nGenerating Employee Embeddings...\n")

    for idx, employee in enumerate(employees, start=1):

        text = None
        embedding = None

        try:

            # Build employee text
            text = build_employee_text(employee)

            # Generate embedding
            embedding = generate_embedding(text)

            # emp_id fallback safety
            emp_id = employee.get("emp_id")

            if emp_id is None:
                emp_id = idx

                print(
                    f"⚠ Missing emp_id for "
                    f"{employee.get('employee_name')} "
                    f"→ using fallback {emp_id}"
                )

            # Save embedding to Supabase
            save_employee_vector(emp_id, embedding)

            print(
                f"✓ {employee.get('employee_name')}"
            )

        except Exception as e:

            print(
                f"[ERROR] Error for "
                f"{employee.get('employee_name')}: {e}"
            )

        finally:

            del embedding
            del text

            gc.collect()
