import statistics


def calculate_statistics(values):
    if not values:
        return {
            "error": "No values provided."
        }

    