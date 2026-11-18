
from backend.ai_engine.services.similarity_service import (
    calculate_similarity,
)


def generate_recommendations(employee_vectors, task_vectors):

    """
    Generate employee-task recommendations one at a time.

    Uses yield instead of storing the complete recommendation
    matrix in memory.
    """

    total_generated = 0

    for employee in employee_vectors:

        for task in task_vectors:

            score = calculate_similarity(
                employee["embedding"],
                task["embedding"]
            )

            percentage = round(score * 100, 2)

            if percentage >= 90:
                status = "Excellent Match"

            elif percentage >= 75:
                status = "Good Match"

            elif percentage >= 60:
                status = "Average Match"

            elif percentage >= 40:
                status = "Poor Match"

            elif percentage >= 30:
                status = "Bad Match"

            elif percentage <= 20:
                status = "No Match"

            else:
                status = "Low Match"

            recommendation = {
                "emp_id": employee["emp_id"],
                "task_id": task["task_id"],
                "task_name": task["task_title"],
                "similarity_score": percentage,
                "status": status
            }

            total_generated += 1

            yield recommendation

    print(
        f"\nTotal Recommendations Generated: "
        f"{total_generated}"
    )
