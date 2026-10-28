import numpy as np


def analyze_with_numpy(categories):
    """Analyze file category counts using NumPy."""

    # Convert category counts into a NumPy array
    counts = np.array(list(categories.values()))

    # Basic NumPy calculations
    total_files = np.sum(counts)
    average_files = np.mean(counts)
    maximum_files = np.max(counts)
    minimum_files = np.min(counts)

    return {
        "Total Files": total_files,
        "Average Files per Category": average_files,
        "Maximum Files in a Category": maximum_files,
        "Minimum Files in a Category": minimum_files
    }