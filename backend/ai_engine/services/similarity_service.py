
import numpy as np


def calculate_similarity(employee_vector, task_vector):

    employee_vector = np.asarray(
        employee_vector,
        dtype=np.float32
    ).reshape(-1)

    task_vector = np.asarray(
        task_vector,
        dtype=np.float32
    ).reshape(-1)

    if employee_vector.shape != task_vector.shape:
        raise ValueError("Employee and task embedding dimensions do not match.")

    # Embeddings are L2-normalized during generation.
    score = np.dot(employee_vector, task_vector)

    return float(np.clip(score, -1.0, 1.0))
