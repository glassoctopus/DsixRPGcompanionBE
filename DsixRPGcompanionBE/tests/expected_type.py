
def not_json(expected_type, json):
    if isinstance(expected_type, float):
        return float(json)
    elif isinstance(expected_type, int):
        return int(json)
    elif isinstance(expected_type, bool):
        return 'true'
    elif isinstance(expected_type, str):
        return json