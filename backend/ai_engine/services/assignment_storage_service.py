
from database.supabase_client import supabase


def save_assignments(assignments):

    if not assignments:
        print("\nNo task assignments generated.")
        return

    records = []

    for assignment in assignments:

        records.append({
            "task_id": assignment["task_id"],
            "task_name": assignment["task_name"],
            "emp_id": assignment["emp_id"],
            "employee_name": assignment["employee_name"],
            "similarity_score": assignment["similarity_score"],
            "workload_score": assignment["workload_score"],
            "final_score": assignment["final_score"],
            "status": "Assigned",
        })

    # Batch upsert instead of checking and writing each record
    supabase.table("task_assignment").upsert(
        records,
        on_conflict="task_id"
    ).execute()

    print("\n" + "=" * 70)
    print("FINAL TASK ASSIGNMENTS")
    print("=" * 70)

    for assignment in records:
        print(
            f"[SUCCESS] {assignment['employee_name']} "
            f"-> {assignment['task_name']} "
            f"(Final Score: {assignment['final_score']})"
        )

    print("\n" + "=" * 70)
    print(f"Assigned Tasks: {len(records)}")
    print("=" * 70)
