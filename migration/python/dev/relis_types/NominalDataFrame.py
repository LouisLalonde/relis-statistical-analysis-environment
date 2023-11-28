import pandas as pd
from typing import Type

from relis_types.NominalVariables import NominalVariables
from relis_types.DataFrame import DataFrame


class NominalDataFrame(DataFrame):
    def __init__(self, data: pd.DataFrame, variable_type: Type[NominalVariables]):
        super().__init__(data, variable_type)