from collections import defaultdict
import re

def extract_data_from_query(sentence):
    '''Regex pattern to capture the junos, the platform and the section'''
    #print(f"   Received sentence is: {sentence}")
    #Regex must be optimized: stil miss some sentences
    pattern = r"(?:list|show) the (.*?) (for (?P<platform>\w+) (?:platforms)? in (?:junos)? (?P<version>\d+\.\d+r\d)|in (?P<version_alt>\d+\.\d+r\d) for (?P<platform_alt>\w+))"
    # (?: ... ) is a non-capturing group
    # (...)?  makes it optional

    match = re.search(pattern, sentence.lower())
    
    if match:
        feature = match.group(1)
        version = match.group("version") or match.group("version_alt")
        platform = match.group("platform") or match.group("platform_alt")
        print(f"Feature: {feature}, Version: {version}, Platform: {platform}")
        return feature, version, platform
    else:
        return None, None, None

def calculate_intent_score(query):
    '''Gets the intention of the query'''

    # Define a weighted dictionary of words associated with each intent
    intent_weights = {
        "specific_junos": {"show": 1, "list": 1, "between": -1, "among": -1, "junos": 1, "release": 1},
        "compare_junos": {"show": 1, "list": 1, "between": 1, "among": 1, "junos": 1, "release": 1},
        "general_query": {"junos": -1, "release": -1, "features": -1}
    }

    # Tokenize the sentence (simple split by spaces here, you might use a more sophisticated tokenizer if needed)
    words = query.lower().split()

    # Calculate scores for each intent based on the presence and weight of words
    scores = defaultdict(int)
    for intent, keywords in intent_weights.items():
        for word in words:
            if word in keywords:
                scores[intent] += keywords[word]

    # Determine the intent with the highest score
    if scores:
        best_intent = max(scores, key=scores.get)
        return best_intent, scores[best_intent]
    else:
        return None, 0