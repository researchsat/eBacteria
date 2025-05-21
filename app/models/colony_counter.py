import random

def simple_colony_count(image_name: str) -> int:
    """
    Simulates colony counting for a given image.
    """
    print(f"Simulating colony count for image: {image_name}")
    # Return a random integer between 10 and 100 to simulate a count
    return random.randint(10, 100)

if __name__ == '__main__':
    # Example usage
    image = "test_image_001.png"
    count = simple_colony_count(image)
    print(f"Simulated count for {image}: {count}")

    image_2 = "another_sample.jpg"
    count_2 = simple_colony_count(image_2)
    print(f"Simulated count for {image_2}: {count_2}")
