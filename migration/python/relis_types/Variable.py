from relis_types.FieldClassificationType import FieldClassificationType

class Variable:
    def __init__(self, name: str, title: str, type: FieldClassificationType, multiple: bool):
        self.name = name
        self.title = title
        self.type = type
        self.multiple = multiple