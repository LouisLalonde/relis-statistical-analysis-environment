import os
import numpy as np
import pandas as pd
import pytest
from python.relis_statistics_kernel import (
    NominalVariables, ContinuousVariables, Policies,
    NominalDataFrame, ContinuousDataFrame,
    _aggregate_variables_by_data_type, _transform_classification_data,
    _substitute_nan
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
    df = pd.read_csv(f'{TEST_ROOT_DIRECTORY}/data/project_classification_nominal_data.csv', encoding='utf8')
    if not Policies.DROP_NA.value:
        df.replace(np.nan, '', inplace=True)
    return df

@pytest.fixture
def project_classification_continuous_data():
    df = pd.read_csv(f'{TEST_ROOT_DIRECTORY}/data/project_classification_continuous_data.csv', encoding='utf8')
    if not Policies.DROP_NA.value:
        df.replace(np.nan, '', inplace=True)
    return df

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

@pytest.fixture
def nominal_dataframe(project_classification_data):
    aggregated_variables = _aggregate_variables_by_data_type(NominalVariables)
    nominal_data = _transform_classification_data(project_classification_data, aggregated_variables)
    return NominalDataFrame(nominal_data, NominalVariables)

@pytest.fixture
def continuous_dataframe(project_classification_data):
    aggregated_variables = _aggregate_variables_by_data_type(ContinuousVariables)
    continuous_data = _transform_classification_data(project_classification_data, aggregated_variables)
    return ContinuousDataFrame(continuous_data, ContinuousVariables)

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

def test_processing_classification_nominal_data(project_classification_data, aggregated_nominal_variables,
                                         project_classification_nominal_data):
    data = _transform_classification_data(project_classification_data, aggregated_nominal_variables)
    assert project_classification_nominal_data.equals(data)


def test_processing_classification_continuous_data(project_classification_data, aggregated_continuous_variables,
                                         project_classification_continuous_data):
    data = _transform_classification_data(project_classification_data, aggregated_continuous_variables)
    assert project_classification_continuous_data.equals(data)
    

def create_test_substitute_nan(df: pd.DataFrame):

    # Apply the function
    _substitute_nan(df)

    # Assert that there are no NaN values in the DataFrame
    assert not df.isnull().values.any(), "DataFrame still contains NaN values"

def test_substitute_nan_nominal_variables(project_classification_nominal_data):
    create_test_substitute_nan(project_classification_nominal_data)

def test_substitute_nan_continuous_variables(project_classification_continuous_data):
    create_test_substitute_nan(project_classification_continuous_data)

def test_nominal_dataframe(nominal_dataframe, nominal_variables):
    assert nominal_dataframe.data.columns.size == len(nominal_variables)
    for variable in nominal_variables:
        assert variable.name in nominal_dataframe.data.columns

def test_continuous_dataframe(continuous_dataframe, continuous_variables):
    assert continuous_dataframe.data.columns.size == len(continuous_variables)
    for variable in continuous_variables:
        assert variable.name in continuous_dataframe.data.columns