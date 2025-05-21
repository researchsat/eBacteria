import random

def predict_antibiotic_resistance(identified_microbe: str, sensitivity_data: dict) -> dict:
    """
    Simulates antibiotic resistance prediction for a given microbe and sensitivity data.
    """
    print(f"Simulating antibiotic resistance prediction for {identified_microbe} with data: {sensitivity_data}")
    
    antibiotics = ["Ampicillin", "Tetracycline", "Penicillin", "Ciprofloxacin", "Erythromycin"]
    statuses = ["Susceptible", "Resistant", "Intermediate"]
    
    resistance_profile = {}
    for antibiotic in antibiotics:
        resistance_profile[antibiotic] = random.choice(statuses)
        
    return resistance_profile

if __name__ == '__main__':
    # Example usage
    microbe = "Escherichia coli"
    data = {"ampicillin_concentration": 10, "tetracycline_concentration": 5, "zone_diameter_mm": {"penicillin": 12}}
    profile = predict_antibiotic_resistance(microbe, data)
    print(f"Resistance profile for {microbe}: {profile}")

    microbe_2 = "Staphylococcus aureus"
    data_2 = {"zone_diameter_mm": {"ciprofloxacin": 22, "erythromycin": 15}}
    profile_2 = predict_antibiotic_resistance(microbe_2, data_2)
    print(f"Resistance profile for {microbe_2}: {profile_2}")
