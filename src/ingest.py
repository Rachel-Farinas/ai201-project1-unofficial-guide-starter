import os
import csv
from config import REVIEWS_PATH
from config import DOCS_PATH
from config import MAX_CHARS
from config import OVERLAP_CHARS
from print import print_professors, print_professor_reviews

def load_documents():
    """Load all reviews from the docs folder."""
    professors = {}

    # only read files that end with .csv
    for filename in sorted(os.listdir(REVIEWS_PATH)):
        if not filename.endswith("_reviews.csv"):
            continue

        # join file name and path and also strip filename to get professor name
        filepath = os.path.join(REVIEWS_PATH, filename)
        professor_name = filename.replace("_reviews.csv", "").replace("_", " ")


        # only create key in dictionary if professor isn't already in it
        if professor_name not in professors:
            professors[professor_name] = {"metadata": {}, "reviews": []}

        # read CSV and create rows as dictionary entries and add to professors dictionary
        with open(filepath, "r", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                professors[professor_name]["reviews"].append(row)

    return attach_metadata(professors)

def attach_metadata(professors):
    # create file path for professors_list.csv
    filepath = os.path.join(DOCS_PATH, "professors_list.csv")

    # open CSV file
    with open(filepath, "r", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            name = row["Name"]
            if name in professors:

                # add dictionary entry to metadata information
                professors[name]["metadata"] = row

    return professors


def split_text(comment):
    """Split a long comment into overlapping, chunk-sized pieces.

    Short comments come back as a single-element list; long ones are broken on
    sentence boundaries and packed up to MAX_CHARS, carrying OVERLAP_CHARS of
    the previous piece into the next so context isn't lost at the seams.
    """
    # short comment -> one piece, nothing to split
    if len(comment) <= MAX_CHARS:
        return [comment]

    sentences = comment.split(". ")
    pieces = []
    current = ""

    for sentence in sentences:
        # if adding this sentence would overflow the current piece, close it off
        if len(current + sentence) >= MAX_CHARS and current != "":
            pieces.append(current)
            # seed the next piece with the tail of the one we just closed (the overlap)
            current = current[-OVERLAP_CHARS:]
        # always add the sentence (runs once per sentence)
        current += sentence

    # flush whatever is left in the last piece
    if current != "":
        pieces.append(current)

    return pieces


def chunk_data(professors):
    """Turn the professors dict into a flat list of chunks ready for embedding."""

    chunks = []

    for name, data in professors.items():
        metadata = data["metadata"]
        reviews = data["reviews"]

        for review_index, review in enumerate(reviews):
            comment = review["Comment"]

            # skip reviews with no usable comment (empty string or None)
            if comment is None or comment == "":
                continue

            # turn the comment into one or more chunk-sized pieces
            pieces = split_text(comment)

            # one chunk record per piece
            for piece_index, piece in enumerate(pieces):
                chunks.append({
                    "id": f"{name}-{review_index}-{piece_index}",
                    "Professor": {
                        "Name": name,
                        "Metadata": metadata,
                    },
                    "Review": {
                        "Comment": piece,
                        # every review field except the comment itself
                        "Metadata": {
                            key: value
                            for key, value in review.items()
                            if key != "Comment"
                        },
                    },
                })

    return chunks
