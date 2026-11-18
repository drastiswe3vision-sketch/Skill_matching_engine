
from datetime import datetime, date

from database.supabase_client import supabase

from backend.resource_workload.workload_service import (
    generate_employee_workload,
    save_employee_workload,
)

# ==========================================================
# Priority Score
# ==========================================================

def get_priority_score(priority):

    priority_map = {
        "Critical": 100,
        "High": 80,
        "Medium": 60,
        "Low": 40,
        "Very Low": 20
    }

    return priority_map.get(priority, 50)


# ==========================================================
# Complexity Score
# ==========================================================

def get_complexity_score(complexity):

    complexity_map = {
        "Very Easy": 50,
        "Easy": 60,
        "Medium": 75,
        "Hard": 90,
        "Expert": 100
    }

    return complexity_map.get(complexity, 70)


# ==========================================================
# Deadline Urgency Score
# ==========================================================

def get_deadline_score(deadline):

    if not deadline:
        return 50

    if isinstance(deadline, str):
        deadline_date = datetime.strptime(
            deadline,
            "%Y-%m-%d"
        ).date()
    else:
        deadline_date = deadline

    days_left = (deadline_date - date.today()).days

    if days_left <= 2:
        return 100

    elif days_left <= 5:
        return 90

    elif days_left <= 10:
        return 80

    elif days_left <= 15:
        return 70

    elif days_left <= 20:
        return 60

    return 50


# ==========================================================
# Intelligent Task Assignment
# Highest Similarity Selection
# ==========================================================

def assign_tasks():

    # ----------------------------------------
    # Load similarity results
    # ----------------------------------------

    matches_response = (
        supabase
        .table("employee_task_match")
        .select(
            "emp_id, name, task_id, task_name, similarity_score"
        )
        .execute()
    )

    matches = matches_response.data or []

    if not matches:
        print("No employee matches found.")
        return []

    # ----------------------------------------
    # Load Pending Tasks
    # ----------------------------------------

    tasks_response = (
        supabase
        .table("tasks")
        .select(
            "id, task_name, priority, complexity, deadline, starting_date"
        )
        .eq("status", "Pending")
        .execute()
    )

    pending_tasks = tasks_response.data or []

    if not pending_tasks:
        print("No pending tasks.")
        return []

    final_assignments = []

    # Prevent one employee from receiving
    # multiple NEW tasks in this execution.

    assigned_employees = set()

    # ======================================================
    # LOOP TASK BY TASK
    # ======================================================

    for task in pending_tasks:

        task_id = task["id"]
        task_name = task["task_name"]

        # ----------------------------------------
        # Validate Deadline
        # ----------------------------------------

        if not task.get("deadline"):

            print(
                f"[SKIPPED] {task_name}: "
                "Deadline is missing."
            )

            continue

        try:

            urgency_score = get_deadline_score(
                task["deadline"]
            )

        except (ValueError, TypeError) as e:

            print(
                f"[SKIPPED] {task_name}: "
                f"Invalid deadline - {e}"
            )

            continue

        # ----------------------------------------
        # All employee matches for THIS task
        # ----------------------------------------

        task_candidates = []

        for row in matches:

            if str(row["task_id"]) != str(task_id):
                continue

            similarity = float(row["similarity_score"])

            # Ignore similarity below 20%

            if similarity < 20:
                continue

            task_candidates.append(row)

        if not task_candidates:
            print(
                f"No eligible employee found for {task_name}"
            )
            continue

        # ----------------------------------------
        # Highest similarity first
        # ----------------------------------------

        task_candidates.sort(
            key=lambda x: float(x["similarity_score"]),
            reverse=True
        )


        assigned = False

        # ==================================================
        # FIND BEST AVAILABLE EMPLOYEE
        # ==================================================

        for row in task_candidates:

            emp_id = row["emp_id"]
            employee_name = row["name"]

            similarity_score = float(
                row["similarity_score"]
            )

            if emp_id in assigned_employees:
                continue

            # ----------------------------------------
            # Calculate workload
            # ----------------------------------------

            try:
                workload = generate_employee_workload(
                    emp_id=emp_id,
                    task_id=task_id,
                    similarity_score=similarity_score
                )

            except Exception as e:
                print(
                    f"Workload Error ({employee_name}): {e}"
                )
                continue

            # ----------------------------------------
            # Calculate assignment scores
            # ----------------------------------------

            priority_score = get_priority_score(
                task["priority"]
            )

            complexity_score = get_complexity_score(
                task["complexity"]
            )

            final_score = (
                similarity_score * 0.45
                + workload["workload_score"] * 0.25
                + priority_score * 0.15
                + urgency_score * 0.10
                + complexity_score * 0.05
            )

            # ----------------------------------------
            # Update task status
            # ----------------------------------------

            try:
                update_response = (
                    supabase
                    .table("tasks")
                    .update({"status": "Assigned"})
                    .eq("id", task_id)
                    .eq("status", "Pending")
                    .select("id")
                    .execute()
                )

            except Exception as e:
                print(
                    f"[ERROR] Task update failed for "
                    f"{task_name}: {e}"
                )
                continue

            if not update_response.data:
                print(
                    f"[WARNING] Could not assign {task_name}. "
                    "Task may no longer be Pending."
                )
                assigned = True
                break

            # ----------------------------------------
            # Save workload AFTER successful assignment
            # ----------------------------------------

            try:
                save_employee_workload(workload)

            except Exception as e:
                print(
                    f"[WARNING] Task assigned, but workload "
                    f"could not be saved for {employee_name}: {e}"
                )

            # ----------------------------------------
            # Store final assignment
            # ----------------------------------------

            final_assignments.append({
                "emp_id": emp_id,
                "employee_name": employee_name,
                "task_id": task_id,
                "task_name": task_name,
                "similarity_score": similarity_score,
                "workload_score": workload["workload_score"],
                "priority": task["priority"],
                "complexity": task["complexity"],
                "deadline": task["deadline"],
                "priority_score": priority_score,
                "complexity_score": complexity_score,
                "urgency_score": urgency_score,
                "final_score": round(final_score, 2)
            })

            assigned_employees.add(emp_id)

            print(
                f"[SUCCESS] {employee_name} -> {task_name} "
                f"Final Score: {round(final_score, 2)}"
            )

            assigned = True

            # Keep highest-similarity selection.
            break

        if not assigned:
            print(
                f"No available employee for {task_name}"
            )


    # ======================================================
    # FINAL OUTPUT
    # ======================================================

    print("\n" + "=" * 70)
    print("SMART TASK ASSIGNMENT COMPLETED")
    print("=" * 70)

    print(f"Assignments: {len(final_assignments)}")

    print("=" * 70)

    return final_assignments
