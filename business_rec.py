import json
from dataclasses import dataclass, field
from collections import Counter

@dataclass
class Business:
    business_id: str
    name: str
    city: str
    state: str
    latitude: float
    longitude: float
    stars: float
    categories: list[str] = field(default_factory=list)
    vector: dict[str, float] = field(default_factory=dict, repr=False)
    norm: float = 0.0
    attributes: dict[str, str] = field(default_factory=dict, repr=False)


def tokenize_categories(categories: str) -> list[str]:
    if categories:
        return [category.strip() for category in categories.split(",")]
    return []



def get_business_data(limit=None, state=None):
    businesses = []
    file_path = "yelp_datasets\\yelp_academic_dataset_business.json"
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if limit is not None and len(businesses) >= limit:
                break
            data = json.loads(line)
            if state is not None and data.get("state") != state:
                continue

            business = Business(
                business_id=data.get("business_id", ""),
                name=data.get("name", ""),
                city=data.get("city", ""),
                state=data.get("state", ""),
                latitude=data.get("latitude", 0.0),
                longitude=data.get("longitude", 0.0),
                stars=data.get("stars", 0.0),
                categories=tokenize_categories(data.get("categories", "")),
                attributes=data.get("attributes") or {}
            )
            businesses.append(business)
    return businesses

businesses = get_business_data(limit=10000)  # Example usage


def build_frequency(businesses):
    freq = Counter()
    for business in businesses:
        business_categories = set(business.categories)
        freq.update(business_categories)
    return freq

frequency = build_frequency(businesses)
#print(frequency.most_common(10))  # Print the 10 most common categories