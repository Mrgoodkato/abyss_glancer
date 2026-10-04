import logging
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def parse_db_records(db_records: list[tuple], columns: dict):

    extracted_data = []

    for record in db_records:
        extracted_element = {}
        for col_name, index in columns.items():
            extracted_element[col_name] = record[index]
        extracted_data.append(extracted_element)

    return extracted_data

def parse_scores_response(comment_id: str, scores: list[dict])-> dict:

    parsed_scores = {}

    for score in scores:

        for k, v in score.items():
            if k == "label":
                label = v
            if k == "score":
                score_val = v
        if label and score_val:
            parsed_scores[label] = score_val
            continue
        logging.error(f"Error parsing score for {comment_id}")

    parsed_scores["id"] = str(uuid.uuid4())

    return parsed_scores

def parse_roberta_scores(scores: tuple)-> dict:

    roberta_scores_range = range(len(scores))
    if roberta_scores_range != 3:
        logging.error(f"Scores failed to parse, iterator for this scores is different than 3 -> {roberta_scores_range}")
        return None

    roberta_scores ={
        "negative": scores[0],
        "neutral": scores[1],
        "positive": scores[2]
    }

    return roberta_scores