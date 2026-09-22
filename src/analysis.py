import statistics


def calculate_statistics(values):
    if not values:
        return {
            "error": "No values provided."
        }

    return {
        "count": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "minimum": min(values),
        "maximum": max(values),
        "standard_deviation": 
        statistics.stdev(values) if len(values) > 1 else 0
    }