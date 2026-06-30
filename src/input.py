from typing import Optional
from src.property import PropertyInput


# the property types your model was trained on — keep in sync with training data.
# ideally pass these in from the trained model's known categories instead of hardcoding.
KNOWN_TYPES = ["Chalet", "Apartamento", "Casa", "Piso", "Ático", "Bungalow"]


def ask_int(prompt: str) -> int:
    while True:
        answer = input(prompt + ": ").strip()
        try:
            value = int(answer)
            if value <= 0:
                print("  Please enter a positive number.")
                continue
            return value
        except ValueError:
            print(f"  '{answer}' is not a whole number, try again.")


def ask_int_optional(prompt: str) -> Optional[int]:
    while True:
        answer = input(prompt + " (leave blank if none): ").strip()
        if not answer:
            return None
        try:
            value = int(answer)
            if value <= 0:
                print("  Please enter a positive number, or leave blank.")
                continue
            return value
        except ValueError:
            print(f"  '{answer}' is not a whole number, try again.")


def ask_choice(prompt: str, choices: list[str]) -> str:
    lookup = {c.lower(): c for c in choices}
    while True:
        answer = input(f"{prompt} {choices}: ").strip().lower()
        if answer in lookup:
            return lookup[answer]          # return canonical casing
        print(f"  Pick one of: {', '.join(choices)}")


def prompt_property_input() -> PropertyInput:
    print("Enter the property details:\n")

    return PropertyInput(
        property_type=ask_choice("Property type", KNOWN_TYPES),
        bedrooms=ask_int("Bedrooms"),
        bathrooms=ask_int("Bathrooms"),
        built_area_m2=ask_int("Built area (m²)"),
        plot_area_m2=ask_int_optional("Plot area (m²)"),
    )