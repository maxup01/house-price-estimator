from dataclasses import dataclass
from typing import Optional

@dataclass
class PropertyDetails:
    url: str
    price_eur: float
    property_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    built_area_m2: Optional[int] = None
    plot_area_m2: Optional[int] = None

    def __init__(
            self, url, price_eur, property_type=None, bedrooms=None, bathrooms=None,
            built_area_m2=None, plot_area_m2=None
    ):
        self.url = url
        self.price_eur = price_eur
        self.property_type = property_type
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.built_area_m2 = built_area_m2
        self.plot_area_m2 = plot_area_m2

def numeric_features():
    return ["bedrooms", "bathrooms", "built_area_m2", "plot_area_m2"]

@dataclass
class PropertyInput:
    property_type: str
    bedrooms: int
    bathrooms: int
    built_area_m2: int
    plot_area_m2: int

    def __init__(
            self, property_type, bedrooms, bathrooms,
            built_area_m2, plot_area_m2
    ):
        self.property_type = property_type
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.built_area_m2 = built_area_m2
        self.plot_area_m2 = plot_area_m2