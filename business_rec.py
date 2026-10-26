import json
from dataclasses import dataclass, field
from collections import Counter
import math

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
    file_path = "yelp_datasets/yelp_academic_dataset_business.json"
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

def build_vectors(businesses, frequency):
    n = len(businesses)
    for business in businesses:
        vector = {}
        for category in business.categories:
            if category in frequency:
                #tf is always 1 because each category appears only once per business
                vector[category] = 1 * math.log(n / frequency[category])
        business.vector = vector
        business.norm = sum(value ** 2 for value in vector.values()) ** 0.5

vectors = build_vectors(businesses, frequency)
#print(f"Example - {businesses[2].name} vector: {businesses[2].vector}")


def compute_cosine_similarity(business1, business2):
    if business1.norm == 0 or business2.norm == 0:
        return 0.0

    if len(business1.vector) <= len(business2.vector):
        smallvector, largevector = business1.vector, business2.vector
    else:
        smallvector, largevector = business2.vector, business1.vector

    dot_product = sum(smallvector[cat] * largevector.get(cat, 0) for cat in smallvector)
    return dot_product / (business1.norm * business2.norm)

cosine = compute_cosine_similarity(businesses[24], businesses[18])
print(f"Cosine similarity between: {businesses[24].name} and {businesses[18].name}: {cosine:.4f}")