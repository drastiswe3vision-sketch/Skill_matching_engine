
from datetime import datetime

from database.supabase_client import supabase

from backend.resource_workload.workload_cal import (
    calculate_employee_scores,
)


# ==========================================================
# CALCULATE EMPLOYEE WORKLOAD
# Does NOT save to Supabase.
# ==========================================================

def generate_employee_workload(
    emp_id,
    task_id,
    similarity_score
):

    # ----------------------------------------
    # Fetch Employee Name
    # ----------------------------------------

    employee_response = (
        supabase
        .table("employee_profiles")
        .select("name")
        .eq("emp_id", emp_id)
        .single()
        .execute()
    )

    if not employee_response.data:
        raise ValueError(
            f"Employee not found: {emp_id}"
        )

    employee_name = employee_response.data["name"]

    # ----------------------------------------
    # Fetch Task Details
    # ----------------------------------------

    task_response = (
        supabase
        .table("tasks")
        .select(
            "starting_date, deadline, priority, complexity"
        )
        .eq("id", task_id)
        .single()
        .execute()
    )

    if not task_response.data:
        raise ValueError(
            f"Task not found: {task_id}"
        )

    task = task_response.data

    starting_date = task["starting_date"]
    deadline = task["deadline"]
    priority = task["priority"]
    complexity = task["complexity"]

    if not deadline:
        raise ValueError(
            f"Deadline is missing for task: {task_id}"
        )

    # ----------------------------------------
    # Calculate Workload
    # ----------------------------------------

    result = calculate_employee_scores(
        starting_date,
        deadline,
        similarity_score,
        emp_id,
        task_id
    )

    # ----------------------------------------
    # Attach Information Needed for Storage
    # ----------------------------------------

    result["emp_id"] = emp_id
    result["task_id"] = task_id
    result["employee_name"] = employee_name
    result["starting_date"] = starting_date
    result["deadline"] = deadline
    result["priority"] = priority
    result["complexity"] = complexity
    result["similarity_score"] = similarity_score

    return result


# ==========================================================
# SAVE WORKLOAD
# Call ONLY after the task is successfully assigned.
# ==========================================================

def save_employee_workload(workload):

    workload_data = {

        "emp_id": workload["emp_id"],

        "task_id": workload["task_id"],

        "employee_name": workload["employee_name"],

        "starting_date": workload["starting_date"],

        "deadline": workload["deadline"],

        "priority": workload["priority"],

        "complexity": workload["complexity"],

        "similarity_score": workload["similarity_score"],

        "total_days": workload["total_days"],

        "total_task_hours": workload["total_task_hours"],

        "total_weekly_available_hours":
            workload["total_weekly_available_hours"],

        "free_hour_before_deadline":
            workload["free_hour_before_deadline"],

        "availability_score":
            workload["availability_score"],

        "active_tasks": workload["active_tasks"],

        "task_load": workload["task_load"],

        "hours_utilization": workload["hours_utilization"],

        "workload_score": workload["workload_score"],

        "resource_balancing_score":
            workload["resource_balancing_score"],

        # Keep the workload-calculation score.
        # Do not overwrite it with the assignment final_score.

        "final_workload_score":
            workload["final_workload_score"],

        "updated_at": datetime.utcnow().isoformat()

    }

    response = (
        supabase
        .table("employee_workload")
        .upsert(
            workload_data,
            on_conflict="emp_id"
        )
        .execute()
    )

    print(
        f"[SUCCESS] Workload saved for "
        f"{workload['employee_name']}"
    )

    return response
