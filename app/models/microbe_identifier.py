import random

def simple_microbe_identification(image_name: str) -> str:
    """
    Simulates microbial identification for a given image.
    """
    print(f"Simulating microbial identification for image: {image_name}")
    species_list = [
        "Escherichia coli",
        "Staphylococcus aureus",
        "Pseudomonas aeruginosa",
        "Streptococcus pneumoniae",
        "Candida albicans"
    ]
    return random.choice(species_list)

if __name__ == '__main__':
    # Example usage
    image = "test_image_002.png"
    identified_species = simple_microbe_identification(image)
    print(f"Identified species for {image}: {identified_species}")

    image_2 = "another_sample_B.jpg"
    identified_species_2 = simple_microbe_identification(image_2)
    print(f"Identified species for {image_2}: {identified_species_2}")
