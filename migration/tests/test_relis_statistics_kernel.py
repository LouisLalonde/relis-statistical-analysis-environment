import re
import os
import numpy as np
import pandas as pd
import pytest
import seaborn as sns
import matplotlib.pyplot as plt
from enum import Enum
from typing import Type
from matplotlib import ticker
from matplotlib.text import Text
from statsmodels.robust.scale import mad
from scipy.stats import kurtosis, skew, shapiro, spearmanr, pearsonr, chi2_contingency
from python.relis_statistics_kernel import (
    NominalVariables, ContinuousVariables, _aggregate_variables_by_data_type
)

### Testing

CURRENT_FILE_PATH = os.path.abspath(__file__)

TEST_ROOT_DIRECTORY = os.path.dirname(CURRENT_FILE_PATH)

AGGREGATED_NOMINAL_VARIABLES = {'Venue': 'venue',
                                'Search Type': 'search_type',
                                'Domain': 'domain',
                                'Transformation Language': 'transformation_language',
                                'Source language': 'source_language',
                                'Target language': 'target_language',
                                'Scope': 'scope',
                                'Industrial': 'industrial',
                                'Bidirectional': 'bidirectional'}

AGGREGATED_CONTINUOUS_VARIABLES = {'Publication year': 'publication_year',
                                    'Targeted year': 'targeted_year'}

@pytest.fixture
def project_classification_data():
    return pd.read_csv(f'{TEST_ROOT_DIRECTORY}/data/relis_classification_CV.csv', encoding='utf8')

@pytest.fixture
def project_classification_nominal_data():
    return pd.read_csv(f'{TEST_ROOT_DIRECTORY}/data/project_classification_nominal_data.csv', encoding='utf8')

@pytest.fixture
def project_classification_continuous_data():
    return pd.read_csv(f'{TEST_ROOT_DIRECTORY}/data/project_classification_continuous_data.csv', encoding='utf8')

@pytest.fixture
def nominal_variables():
    return NominalVariables

@pytest.fixture
def continuous_variables():
    return ContinuousVariables

@pytest.fixture
def aggregated_nominal_variables():
    return AGGREGATED_NOMINAL_VARIABLES

@pytest.fixture
def aggregated_continuous_variables():
    return AGGREGATED_CONTINUOUS_VARIABLES

### Data

## Parsing

def test_load_classification_data(project_classification_data: pd.DataFrame):
    # Assert that classification file isn't empty
    assert(project_classification_data.size) > 0
    # Assert that classification file contains a header
    assert(len(project_classification_data.columns)) > 0
    # Assert that classification file contains papers
    assert(len(project_classification_data.index)) > 0
    # Assert that classification header contains the publication year
    assert(hasattr(project_classification_data, 'Publication year'))

def test_aggregate_nominal_variables(nominal_variables, aggregated_nominal_variables):
    assert _aggregate_variables_by_data_type(nominal_variables) == aggregated_nominal_variables

def test_aggregate_continuous_variables(continuous_variables, aggregated_continuous_variables):
    assert _aggregate_variables_by_data_type(continuous_variables) == aggregated_continuous_variables

## Preprocessing

def create_test_processing_classification_data(project_classification_data: pd.DataFrame, aggregated_variables: dict[str, str]):
    return project_classification_data[aggregated_variables.keys()].rename(columns=aggregated_variables)

def test_processing_classification_nominal_data(project_classification_data, aggregated_nominal_variables,
                                         project_classification_nominal_data):
    data = create_test_processing_classification_data(project_classification_data, aggregated_nominal_variables)
    assert project_classification_nominal_data.equals(data)


def test_processing_classification_continuous_data(project_classification_data, aggregated_continuous_variables,
                                         project_classification_continuous_data):
    data = create_test_processing_classification_data(project_classification_data, aggregated_continuous_variables)
    assert project_classification_continuous_data.equals(data)
    

def substitute_nan(df: pd.DataFrame):
    df.replace(np.nan, '', inplace=True)

def create_test_substitute_nan(df: pd.DataFrame):

    # Apply the function
    substitute_nan(df)

    # Assert that there are no NaN values in the DataFrame
    assert not df.isnull().values.any(), "DataFrame still contains NaN values"

def test_substitute_nan_nominal_variables(project_classification_nominal_data):
    create_test_substitute_nan(project_classification_nominal_data)

def test_substitute_nan_continuous_variables(project_classification_continuous_data):
    create_test_substitute_nan(project_classification_continuous_data)

