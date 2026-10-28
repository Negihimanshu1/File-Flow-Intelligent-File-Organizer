from functools import reduce


def functional_analysis(categories):
    """
    Perform file analysis using
    lambda, map, filter and reduce.
    """

    counts = list(categories.values())

    # map() + lambda
    doubled_counts = list(
        map(
            lambda x: x * 2,
            counts
        )
    )

    # filter() + lambda
    non_zero_counts = list(
        filter(
            lambda x: x > 0,
            counts
        )
    )

    # reduce() + lambda
    total_files = reduce(
        lambda x, y: x + y,
        counts,
        0
    )

    # lambda with max()
    highest_category = max(
        categories.items(),
        key=lambda item: item[1]
    )

    return {
        "Doubled Counts": doubled_counts,
        "Non Zero Counts": non_zero_counts,
        "Total Files": total_files,
        "Highest Category": highest_category
    }