from enum import Enum

from relis_types.FieldClassificationType import FieldClassificationType
from relis_types.Variable import Variable


class ContinuousVariables(Enum):
    publication_year = Variable("publication_year", "Publication year", FieldClassificationType.CONTINUOUS, False)
    targeted_year = Variable("targeted_year", "Targeted year", FieldClassificationType.CONTINUOUS, False)