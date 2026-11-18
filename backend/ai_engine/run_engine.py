
from backend.BAAI.fine_tuning.flow.inference.model_loader import ModelLoader

from backend.ai_engine.models.employee_embeddings import (
    generate_employee_embeddings,
)

from backend.ai_engine.models.task_embeddings import (
    generate_task_embeddings,
)

from backend.ai_engine.services.vector_fetch_service import (
    get_employee_vectors,
    get_task_vectors,
)

from backend.ai_engine.services.recommendation_service import (
    generate_recommendations,
)

from backend.ai_engine.services.recommendation_storage_service import (
    save_recommendations,
)

from backend.ai_engine.services.task_assignment_service import (
    assign_tasks,
)

from backend.ai_engine.services.assignment_storage_service import (
    save_assignments,
)

from backend.ai_engine.services.task_completed_service import (
    move_completed_tasks,
)


def log_step(message):
    print("\n" + "=" * 60, flush=True)
    print(message, flush=True)
    print("=" * 60, flush=True)


# =====================================================
# STEP 0: COMPLETED TASKS
# =====================================================

log_step("STEP 0: CHECKING COMPLETED TASKS")

move_completed_tasks()

print("Completed-task processing finished.", flush=True)


# =====================================================
# STEP 1: EMPLOYEE EMBEDDINGS
# =====================================================

log_step("STEP 1: GENERATING EMPLOYEE EMBEDDINGS")

generate_employee_embeddings()

print("Employee embeddings generated.", flush=True)


# =====================================================
# STEP 2: TASK EMBEDDINGS
# =====================================================

log_step("STEP 2: GENERATING TASK EMBEDDINGS")

generate_task_embeddings()

print("Task embeddings generated.", flush=True)


# =====================================================
# STEP 3: UNLOAD BGE MODEL
# =====================================================

log_step("STEP 3: UNLOADING BGE MODEL")

ModelLoader.unload()

print("BGE model unloaded.", flush=True)


# =====================================================
# STEP 4: FETCH VECTORS
# =====================================================

log_step("STEP 4: FETCHING STORED VECTORS")

employee_vectors = get_employee_vectors()

print(
    f"Employee vectors fetched: {len(employee_vectors)}",
    flush=True,
)

task_vectors = get_task_vectors()

print(
    f"Task vectors fetched: {len(task_vectors)}",
    flush=True,
)


# =====================================================
# STEP 5: GENERATE RECOMMENDATIONS
# =====================================================

log_step("STEP 5: GENERATING RECOMMENDATIONS")

recommendations = generate_recommendations(
    employee_vectors,
    task_vectors,
)

print("Recommendation generation completed.", flush=True)


# =====================================================
# STEP 6: SAVE RECOMMENDATIONS
# =====================================================

log_step("STEP 6: SAVING RECOMMENDATIONS")

save_recommendations(recommendations)

print("Recommendations saved.", flush=True)


# =====================================================
# STEP 7: ASSIGN TASKS
# =====================================================

log_step("STEP 7: ASSIGNING TASKS")

assignments = assign_tasks()

print(
    f"Assignments generated: {len(assignments)}",
    flush=True,
)


# =====================================================
# STEP 8: SAVE ASSIGNMENTS
# =====================================================

log_step("STEP 8: SAVING ASSIGNMENTS")

save_assignments(assignments)

print("Assignments saved.", flush=True)


# =====================================================
# COMPLETED
# =====================================================

log_step("AI PIPELINE COMPLETED SUCCESSFULLY")
