import json


def print_professors(professors: dict, n: int = 10, reviews_n: int = 0):
    """Print the first n professors, their metadata, and the first reviews_n reviews each."""
    for i, (name, data) in enumerate(professors.items()):
        if i >= n:
            break
        print(f"\n{'='*50}")
        print(f"Professor: {name}")
        print(f"Metadata: {json.dumps(data['metadata'], indent=2)}")
        print(f"Number of reviews: {len(data['reviews'])}")

        for j, review in enumerate(data["reviews"][:reviews_n]):
            print(f"\n--- Review {j+1} ---")
            for key, value in review.items():
                print(f"  {key}: {value}")


def print_professor_reviews(professors: dict, professor_name: str, n: int = 10):
    """Print the first n reviews for a given professor."""
    if professor_name not in professors:
        print(f"Professor '{professor_name}' not found.")
        return

    reviews = professors[professor_name]["reviews"]
    print(f"\n{'='*50}")
    print(f"Reviews for: {professor_name} ({len(reviews)} total)")
    print(f"{'='*50}")

    for i, review in enumerate(reviews[:n]):
        print(f"\n--- Review {i+1} ---")
        for key, value in review.items():
            print(f"  {key}: {value}")
