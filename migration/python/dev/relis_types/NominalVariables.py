from enum import Enum
from relis_types.FieldClassificationType import FieldClassificationType
from relis_types.Variable import Variable


class NominalVariables(Enum):
    venue = Variable("venue", "Venue", FieldClassificationType.NOMINAL, False)
    search_type = Variable("search_type", "Search Type", FieldClassificationType.NOMINAL, False)
    domain = Variable("domain", "Domain", FieldClassificationType.NOMINAL, False)
    transformation_language = Variable("transformation_language", "Transformation Language", FieldClassificationType.NOMINAL, True)
    source_language = Variable("source_language", "Source language", FieldClassificationType.NOMINAL, False)
    target_language = Variable("target_language", "Target language", FieldClassificationType.NOMINAL, False)
    scope = Variable("scope", "Scope", FieldClassificationType.NOMINAL, True)
    industrial = Variable("industrial", "Industrial", FieldClassificationType.NOMINAL, False)
    bidirectional = Variable("bidirectional", "Bidirectional", FieldClassificationType.NOMINAL, False)