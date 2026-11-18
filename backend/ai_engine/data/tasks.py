
from database.supabase_client import supabase


def get_pending_tasks():

    response = (
        supabase
        .table("tasks")
        .select(
            "id,task_name,description,technologies,"
            "tools_and_ide,required_skills,status"
        )
        .eq("status", "Pending")
        .execute()
    )

    tasks = []

    for row in response.data:

        tasks.append({
            "id": row["id"],
            "title": row["task_name"],
            "description": row.get("description") or "",
            "technologies": row.get("technologies") or [],
            "tools": row.get("tools_and_ide") or [],
            "required_skills": row.get("required_skills") or [],
            "status": row.get("status")
        })

    return tasks
