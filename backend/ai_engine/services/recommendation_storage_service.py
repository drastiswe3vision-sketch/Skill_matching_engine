
from database.supabase_client import supabase


def save_recommendations(recommendations):

    # Fetch employee names once
    employee_response = (
        supabase
        .table("employee_profiles")
        .select("emp_id, name")
        .execute()
    )

    employee_names = {
        employee["emp_id"]: employee["name"]
        for employee in (employee_response.data or [])
    }

    batch_size = 100
    batch = []

    total_saved = 0

    print("\nSaving Recommendations...\n")

    for recommendation in recommendations:

        emp_id = recommendation["emp_id"]

        employee_name = employee_names.get(emp_id)

        if employee_name is None:
            print(
                f"[WARNING] Employee name not found: {emp_id}"
            )
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

            total_saved += len(batch)

            print(
                f"[SUCCESS] Total saved: {total_saved}"
            )

            batch.clear()

    # Save remaining recommendations
    if batch:

        supabase.table("employee_task_match").upsert(
            batch,
            on_conflict="emp_id,task_id"
        ).execute()

        total_saved += len(batch)

        batch.clear()

    print(
        f"\n[SUCCESS] Total recommendations saved: "
        f"{total_saved}"
    )
