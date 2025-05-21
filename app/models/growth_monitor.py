import random

def simple_growth_monitoring(image_series: list[str], duration_hours: int) -> str:
    """
    Simulates growth monitoring for a given image series over a duration.
    """
    print(f"Simulating growth monitoring for image series: {image_series} over {duration_hours} hours.")
    growth_statuses = [
        "No Significant Growth",
        "Low Growth",
        "Moderate Growth",
        "High Growth",
        "Contamination Detected"
    ]
    return random.choice(growth_statuses)

if __name__ == '__main__':
    # Example usage
    series_1 = ["img_t0.png", "img_t1.png", "img_t2.png"]
    duration_1 = 24
    status_1 = simple_growth_monitoring(series_1, duration_1)
    print(f"Monitoring status for {series_1} over {duration_1}h: {status_1}")

    series_2 = ["cultureA_0h.jpg", "cultureA_12h.jpg", "cultureA_24h.jpg", "cultureA_36h.jpg"]
    duration_2 = 36
    status_2 = simple_growth_monitoring(series_2, duration_2)
    print(f"Monitoring status for {series_2} over {duration_2}h: {status_2}")
