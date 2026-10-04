import math
import logging
import traceback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def calculate_roberta_weight_result(fechted_roberta_scores: list, post_index: int, total_posts: int):

    #TODO Create a way to define the weight_source value, it's gonna be defaulted to 1 for now

    weighted_source = 1.0


    # Check highest roberta score for raw confidence peak
    weighted_confidence = max(fechted_roberta_scores)

    entropy = 0

    # Shannon entropy - measures distribution spread/uncertainty.
    # High concentration (e.g., [0.90, 0.07, 0.03]) -> Low value (~0).
    # Uniform distribution (e.g., [0.33, 0.33, 0.34]) -> High value (~1.098).
    for score in fechted_roberta_scores:
        if score > 0:
            entropy -= score * math.log(score)

    # Divide by log(3) to scale entropy onto a clean 0.0 to 1.0 range.
    # 0.0 = total certainty, 1.0 = total confusion/uncertainty.
    normalized_entropy = entropy / math.log(3)

    # Invert normalized_entropy to certainty and scale with a 0.7 floor.
    # Guarantees the output weight factor stays between 0.7 (min influence) and 1.0 (max influence).
    floor_influence = 0.7
    weighted_entropy = floor_influence + (1 - floor_influence) * (1 - normalized_entropy)

    if total_posts > 1:
        relative_time = post_index / (total_posts - 1)
    else:
        relative_time = 1.0

    floor_time = 0.7
    weighted_time = floor_time + (1-floor_time) * relative_time

    weighted_final = weighted_source + weighted_confidence + weighted_entropy + weighted_time

    return weighted_final