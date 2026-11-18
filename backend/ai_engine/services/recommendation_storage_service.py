
"""
recommendation_storage_service.py

Save employee-task recommendations to Supabase
using batched upsert operations.
"""

from database.supabase_client import supabase


def save_recommendations(recommendations):

    if not recommendations:
        print("\n[INFO] No recommendations to save.")
        return

    # Fetch employee names only once
    employee_response = (
        supabase
        .table("employee_profiles")
        .select("emp_id, name")
        .execute()
    )

    employee_names = {
        employee["emp_id"]: employee["name"]
        for employee in employee_response.data
    }

    batch_size = 100
    batch = []

    print("\nSaving Recommendations...\n")

    for recommendation in recommendations:

        emp_id = recommendation["emp_id"]

        employee_name = employee_names.get(emp_id)

        if employee_name is None:
            print(f"[WARNING] Employee name not found for ID: {emp_id}")
            continue

        batch.append({
            "emp_id": emp_id,
            "name": employee_name,
            "task_id": recommendation["task_id"],
            "task_name": recommendation["task_name"],
            "similarity_score": recommendation["similarity_score"],
            "status": recommendation["status"]
        })

        if len(batch) >= batch_size:

            supabase.table("employee_task_match").upsert(
                batch,
                on_conflict="emp_id,task_id"
            ).execute()

            print(f"[SUCCESS] Saved {len(batch)} recommendations")

            batch.clear()

    # Save remaining records
    if batch:

        supabase.table("employee_task_match").upsert(
            batch,
            on_conflict="emp_id,task_id"
        ).execute()

        print(f"[SUCCESS] Saved {len(batch)} recommendations")

    print("\n[SUCCESS] Recommendations saved successfully.")
