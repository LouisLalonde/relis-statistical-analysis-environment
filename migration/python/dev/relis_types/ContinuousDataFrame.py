import pandas as pd
from typing import Type

from relis_types.ContinuousVariables import ContinuousVariables
from relis_types.DataFrame import DataFrame


class ContinuousDataFrame(DataFrame):
    def __init__(self, data: pd.DataFrame, variable_type: Type[ContinuousVariables]):
        super().__init__(data, variable_type)