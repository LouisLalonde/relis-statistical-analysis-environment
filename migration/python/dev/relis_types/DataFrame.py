import pandas as pd
from typing import Type

from relis_types.NominalVariables import NominalVariables
from relis_types.ContinuousVariables import ContinuousVariables 


class DataFrame:
    def __init__(self, data: pd.DataFrame, variable_type: Type[NominalVariables] | Type[ContinuousVariables]):
        self.data = data
        self.variable_type = variable_type