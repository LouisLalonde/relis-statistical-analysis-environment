import json

with open('../../data/relis_classification_CV.json', 'r', encoding='utf8') as f:
   data =  json.loads(f.read())

# Define the attribute type mapping
attribute_type_mapping = {
    "Transformation name": "Text",
    "Domain": "Nominal",
    "Transformation Language": "Nominal",
    "Source language": "Nominal",
    "Target language": "Nominal",
    "Scope": "Nominal",
    "Industrial": "Nominal",
    "Bidirectional": "Nominal",
    "Targeted year": "Continuous",
    "Note": "Text",
    "Publication year": "Continuous",
    "Venue": "Nominal",
    "Search Type": "Nominal"
}

# Define a function to determine if the attribute should be multiple based on the character '|'
def is_multiple(attribute_name, attribute_value):
    if attribute_name in ["Transformation Language", "Scope", "Source language", "Target language"]:
        return "|" in attribute_value
    else:
        return False

# Transform the keys based on the attribute type and multiple attribute
transformed_data = []

for row in data:
    transformed_row = {}
    for key, value in row.items():
        attribute_type = attribute_type_mapping.get(key)
        print(attribute_type)
        if attribute_type is not None and attribute_type != 'Text':
            multiple = is_multiple(key, value)
            transformed_row[key.lower().replace(' ', '_')] = {
                "title": key,
                "value": value,
                "type": attribute_type,
                "multiple": multiple
            }
    transformed_data.append(transformed_row)

# Convert the transformed data to JSON
json_output = json.dumps(transformed_data, indent=2)

with open('../data/relis_classification_rsc_CV.json', 'w', encoding='utf8') as wf:
    wf.write(json_output)
