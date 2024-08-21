"""needed this for testing, there was no conversion from json mechanisim in my test code, there maybe a django feature, and i ashould read the docs, but this was quicker
Takes the type it should be , and the field, and casts it to that type on return"""
def not_json(expected_type, json):
    if isinstance(expected_type, float):
        return float(json)
    elif isinstance(expected_type, int):
        return int(json)
    elif isinstance(expected_type, bool):
        return 'true'
    elif isinstance(expected_type, str):
        return json