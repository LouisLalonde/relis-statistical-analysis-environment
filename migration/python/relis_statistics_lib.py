import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from enum import Enum
from typing import Type
from matplotlib import ticker
from statsmodels.robust.scale import mad
from scipy.stats import kurtosis, skew, shapiro, spearmanr, pearsonr, chi2_contingency

### Config

plt.rcParams['figure.max_open_warning'] = 0

custom = {"axes.edgecolor": "black", "grid.linestyle": "dashed", "grid.color": "grey"}

sns.set_style("darkgrid", rc = custom)

class Multivalue(Enum):
    SEPARATOR = '|'

class Policies(Enum):
    DROP_NA = False

### Types

class FieldClassificationType(Enum):
    NOMINAL = 'Nominal'
    CONTINUOUS = 'Continuous'

class Variable:
    def __init__(self, name: str, title: str, type: FieldClassificationType, multiple: bool):
        self.name = name
        self.title = title
        self.type = type
        self.multiple = multiple

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

class ContinuousVariables(Enum):
    publication_year = Variable("publication_year", "Publication year", FieldClassificationType.CONTINUOUS, False)
    targeted_year = Variable("targeted_year", "Targeted year", FieldClassificationType.CONTINUOUS, False)

class DataFrame:
    def __init__(self, data: pd.DataFrame, variable_type: Type[NominalVariables] | Type[ContinuousVariables]):
        self.data = data
        self.variable_type = variable_type

class NominalDataFrame(DataFrame):
    def __init__(self, data: pd.DataFrame, variable_type: Type[NominalVariables]):
        super().__init__(data, variable_type)

class ContinuousDataFrame(DataFrame):
    def __init__(self, data: pd.DataFrame, variable_type: Type[ContinuousVariables]):
        super().__init__(data, variable_type)

### Shared

def substituteNan(df: pd.DataFrame) -> None:
    df.replace(np.nan, '', inplace=True)

def get_variable(field_name: str, variables) -> Variable:
    return variables[field_name].value

def split_multiple_values(value):
    if not pd.isna(value):
        return [item.strip() for item in re.split(rf'\{Multivalue.SEPARATOR.value}', value)] 
    return [value]

def process_multiple_values(values: pd.Series, multiple: bool):
    if (multiple):
        return values.apply(lambda x: split_multiple_values(x))

    return values.apply(lambda x: [x])

def dataFrameGetTitle(statistic_type: str, statistic_name: str,
                          field_name: str, dependency_field_name = None):
    
    base_str =  f"{statistic_type} | {statistic_name} : {field_name}"

    if dependency_field_name: base_str += f"->{dependency_field_name}"

    return {'title': base_str}

def dataFrameUpdateTitle(dataFrame: pd.DataFrame, object: dict):
    dataFrame.attrs.update(object)

def display_data(dataFrame: pd.DataFrame | None, bool: bool):
    if type(dataFrame) != pd.DataFrame:
        print("No data... Nothing to show")
    elif bool:
        if dataFrame.attrs.get('title'): print(dataFrame.attrs.get('title'))
        print(dataFrame.to_markdown())
        print("\n")

def display_figure(plt, bool: bool):
    if bool: plt.show()

### Data

## Parsing

project_classification_data = pd.read_csv('../data/relis_classification_CV.csv', encoding='utf8')

nominal_variables = {nominal_variable.value.title: nominal_variable.name for nominal_variable in NominalVariables}
continuous_variables = {continuous_variable.value.title: continuous_variable.name for continuous_variable in ContinuousVariables}

## Preprocessing

nominal_data = project_classification_data[nominal_variables.keys()].rename(columns=nominal_variables)
continuous_data = project_classification_data[continuous_variables.keys()].rename(columns=continuous_variables)

if (not Policies.DROP_NA.value):
    substituteNan(nominal_data)
    substituteNan(continuous_data)

nominal = NominalDataFrame(nominal_data, NominalVariables)
continuous = ContinuousDataFrame(continuous_data, ContinuousVariables)

### DESCRIPTIVE STATS

## Util

def beautify_data_desc(field_name: str, data: pd.DataFrame):
    # Get metadata
    variable = get_variable(field_name, NominalVariables)

    # Split the values by the multivalue character and flatten the result
    split_values = process_multiple_values(data[field_name], variable.multiple)
    flattened_values = np.concatenate(split_values)

    # Generate the frequency table
    freq_table = pd.Series(flattened_values, dtype=str).value_counts().reset_index()
    freq_table.columns = ['value', 'n']

    # Calculate the percentage
    freq_table['percentage'] = (freq_table['n'] / freq_table['n'].sum()) * 100

    return freq_table

## Frequency tables

def generate_desc_frequency_table(field_name: str, data: pd.DataFrame):
    subset_data = beautify_data_desc(field_name, data)

    dataFrameUpdateTitle(subset_data, dataFrameGetTitle('Descriptive', 'Frequency tables', field_name))

    return subset_data

desc_frequency_tables = {NominalVariables[field_name]:  generate_desc_frequency_table(field_name, nominal.data)
                      for field_name in nominal.data.columns}

## Bar plots

def generate_desc_bar_plot(field_name: str, data: pd.DataFrame):
    df = beautify_data_desc(field_name, data)
    
    if (len(df) == 0): return

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    hue = "n"
    sns.barplot(data=df, x="value", y="percentage", hue=hue, dodge=False)

    # Get metadata
    variable = get_variable(field_name, NominalVariables)

    # Set labels and title
    title = f"{variable.title} ~ Bar plot"
    plt.title(title)
    plt.xlabel(variable.title)
    plt.ylabel("Percentage")
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', title=hue)
    plt.gca().get_legend().get_frame().set_edgecolor('black')

    return fig

desc_bar_plots = {NominalVariables[field_name]: generate_desc_bar_plot(field_name, nominal.data)
                    for field_name in nominal.data.columns}

## Statistics

def generate_desc_statistics(field_name: str, data: pd.DataFrame):
    series =  data[field_name]
    
    series.replace('', np.nan, inplace=True)
    
    if (len(data) == 0): return

    nan_policy = 'omit' if Policies.DROP_NA.value else 'propagate'
    results = {
    "vars": 1,
    "n": series.count(),
    "mean": series.mean(),
    "sd": series.std(),
    "median": series.median(),
    "trimmed": series[series.between(series.quantile(0.25), series.quantile(0.75))].mean(),
    "mad": mad(series),
    "min": series.min(),
    "max": series.max(),
    "range": series.max() - series.min(),
    "skew": skew(series, nan_policy=nan_policy),
    "kurtosis": kurtosis(series, nan_policy=nan_policy, fisher=True),
    "se": series.std() / np.sqrt(series.count())  
    }

    subset_data = pd.DataFrame(results, index=[0])

    dataFrameUpdateTitle(subset_data, dataFrameGetTitle('Descriptive', 'Statistics', field_name))

    return subset_data

desc_statistics = {ContinuousVariables[field_name]: generate_desc_statistics(field_name, continuous.data)
                      for field_name in continuous.data.columns}

## Box Plots

def generate_desc_box_plot(field_name: str, data: pd.DataFrame):
    series = data[field_name]

    variable = get_variable(field_name, ContinuousVariables)

    # Create the box plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=series, color='lightblue')

    # Overlay the mean point
    mean_value = series.mean()
    plt.scatter(x=0, y=mean_value, color='red', s=50, zorder=3)  # s is the size of the point

    # Set the title and labels
    title = f"{variable.title} ~ Box plot"
    plt.title(title)
    plt.ylabel(variable.title)
    plt.xlabel('')
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

    return fig

desc_box_plots = {ContinuousVariables[field_name]: generate_desc_box_plot(field_name, continuous.data)
                    for field_name in continuous.data.columns}

## Violin Plots

def generate_desc_violin_plot(field_name: str, data: pd.DataFrame):
    series = data[field_name]
    
    variable = get_variable(field_name, ContinuousVariables)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(data=series, color="lightgray")

    plt.title(f"{variable.title} ~ Violin plot")
    plt.ylabel(variable.title)
    plt.xlabel("Density")
    plt.xticks([])

    return fig

desc_violin_plots = {ContinuousVariables[field_name]: generate_desc_violin_plot(field_name, continuous.data)
                       for field_name in continuous.data.columns}

### EVOLUTIVE STATS

## Util

def beautify_data_evo(field_name: str, publication_year: pd.Series, variable: Variable, data: pd.DataFrame):
    series = data[field_name]
    
    # Create new DataFrame with specified columns
    subset_data = pd.DataFrame({
        'Year': publication_year,
        'Value': process_multiple_values(series, variable.multiple)
    })
    
    subset_data = subset_data.explode('Value')

    # Remove rows with empty values
    subset_data = subset_data[(subset_data['Value'] != '')]

    subset_data = subset_data.groupby(['Year', 'Value']).size().reset_index(name='Frequency')

    return subset_data

## Frequency tables

def generate_evo_frequency_table(field_name: str, publication_year: pd.Series, data: pd.DataFrame):
    variable = get_variable(field_name, NominalVariables)

    subset_data = beautify_data_evo(field_name, publication_year, variable, data)

    # Pivoting the data
    subset_data = subset_data.pivot(index='Year', columns='Value', values='Frequency').fillna(0)

    subset_data.columns.name = None
    subset_data.reset_index(inplace=True)

    dataFrameUpdateTitle(subset_data, dataFrameGetTitle('Evolutive', 'Frequency tables', field_name))

    return subset_data 

evo_frequency_tables = {NominalVariables[field_name]: generate_evo_frequency_table(field_name, continuous.data["publication_year"], nominal.data)
                       for field_name in nominal.data.columns}

## Evolution Plots

def generate_evo_plot(field_name: str, publication_year: pd.Series, data: pd.DataFrame):
    variable = get_variable(field_name, NominalVariables)
    
    subset_data = beautify_data_evo(field_name, publication_year, variable, data)

    # Create a plot
    fig, ax = plt.subplots(figsize=(10, 6))
    hue = 'Value'
    sns.lineplot(data=subset_data, x='Year', y='Frequency', hue=hue, style='Value', markers=True)

    # Setting title, labels, and theme
    plt.title(f"{variable.title} ~ Evolution plot")
    plt.xlabel('Year')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', title=hue)
    plt.gca().get_legend().get_frame().set_edgecolor('black')

    return fig

evo_plots = {NominalVariables[field_name]: generate_evo_plot(field_name, continuous.data["publication_year"], nominal.data)
                          for field_name in nominal.data.columns}

### COMPARATIVE STATS

## Util

def beautify_data_comp(field_name: str, dependency_field_name: str,
                        variable: Variable, dependency_variable: Variable, data: pd.DataFrame):    
    subset_data = pd.DataFrame({
        field_name: data[field_name],
        dependency_field_name: data[dependency_field_name]
    })
    
    # Filtering out rows where any of the variables is empty
    subset_data = subset_data[(subset_data[field_name] != "") & (subset_data[dependency_field_name] != "")]

    # Splitting the strings and expanding into separate rows
    subset_data[field_name] = process_multiple_values(subset_data[field_name], variable.multiple)
    subset_data = subset_data.explode(field_name)

    subset_data[dependency_field_name] = process_multiple_values(subset_data[dependency_field_name],
                                                                  dependency_variable.multiple)
    subset_data = subset_data.explode(dependency_field_name)

    # Counting occurrences
    subset_data = subset_data.groupby([field_name, dependency_field_name]).size().reset_index(name='Frequency')

    return subset_data

def evaluate_comparative_dependency_field(field_name: str, dataFrame: DataFrame, strategy):
    """
    Perform a statistical analysis strategy for each 
    dependency field of a given classification field.
    Act as a wrapper for the comparative statistical
    functions
    """
    field_names = list(dataFrame.data.columns)

    return {dataFrame.variable_type[dependency_field_name]: strategy(field_name, dependency_field_name, dataFrame.data)
             for dependency_field_name in field_names if dependency_field_name != field_name}

## Frequency Tables

def generate_comp_frequency_table(field_name: str, dependency_field_name: str, data: pd.DataFrame):
    variable = get_variable(field_name, NominalVariables)
    dependency_variable = get_variable(dependency_field_name, NominalVariables)

    subset_data = beautify_data_comp(field_name, dependency_field_name,
                                      variable, dependency_variable, data)
    
    dataFrameUpdateTitle(subset_data, dataFrameGetTitle('Comparative', 'Frequency tables', field_name, dependency_field_name))

    return subset_data

comp_frequency_tables = {NominalVariables[field_name]: evaluate_comparative_dependency_field(field_name, nominal, generate_comp_frequency_table)
                       for field_name in nominal.data.columns}

## Bar Plots

def generate_comp_stacked_bar_plot(field_name: str, dependency_field_name: str, data: pd.DataFrame):
    variable = get_variable(field_name, NominalVariables)
    dependency_variable = get_variable(dependency_field_name, NominalVariables)

    subset_data = beautify_data_comp(field_name, dependency_field_name,
                                      variable, dependency_variable, data)

    if subset_data.empty: return

    # Pivot the data to get a matrix form
    pivoted_data = subset_data.pivot(index=field_name, columns=dependency_field_name, values='Frequency')

    # Replace NaN values with 0
    pivoted_data = pivoted_data.fillna(0)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Bottom value for stacking
    bottom_value = pd.Series([0] * pivoted_data.shape[0], index=pivoted_data.index)

    for col in pivoted_data.columns:
        plt.bar(pivoted_data.index, pivoted_data[col], bottom=bottom_value, label=col)
        bottom_value += pivoted_data[col]

    plt.title(f"{variable.title} and {dependency_variable.title} ~ Stacked bar plot")
    plt.xlabel(variable.title)
    plt.ylabel('Frequency')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', title=dependency_field_name)
    plt.gca().get_legend().get_frame().set_edgecolor('black')

    return fig

comp_stacked_bar_plots = {NominalVariables[field_name]: evaluate_comparative_dependency_field(field_name, nominal, generate_comp_stacked_bar_plot)
                       for field_name in nominal.data.columns}

## Grouped Bar Plots

def generate_comp_grouped_bar_plot(field_name: str, dependency_field_name: str, data: pd.DataFrame):
    variable = get_variable(field_name, NominalVariables)
    dependency_variable = get_variable(dependency_field_name, NominalVariables)

    subset_data = beautify_data_comp(field_name, dependency_field_name,
                                      variable, dependency_variable, data)

    if subset_data.empty: return

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=field_name, y='Frequency', hue=dependency_field_name, data=subset_data, dodge=True)

    plt.title(f"{variable.title} and {dependency_variable.title} ~ Grouped bar plot")
    plt.gca().set_xlabel('')
    plt.ylabel('Frequency')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', title=dependency_field_name)
    plt.gca().get_legend().get_frame().set_edgecolor('black')

    return fig

comp_grouped_bar_plots = {NominalVariables[field_name]: evaluate_comparative_dependency_field(field_name, nominal, generate_comp_grouped_bar_plot)
                       for field_name in nominal.data.columns}

## Bubble Charts

def generate_comp_bubble_chart(field_name: str, dependency_field_name: str, data: pd.DataFrame):
    variable = get_variable(field_name, NominalVariables)
    dependency_variable = get_variable(dependency_field_name, NominalVariables)

    subset_data = beautify_data_comp(field_name, dependency_field_name,
                                      variable, dependency_variable, data)

    if subset_data.empty: return

    # Creating the bubble chart
    fig, ax = plt.subplots(figsize=(10, 6))
    size = 'Frequency'
    sns.scatterplot(data=subset_data, x=field_name, y=dependency_field_name, size=size, color='black')

    # Adding labels and title
    plt.title(f"{variable.title} and {dependency_variable.title} ~ Bubble Chart")
    plt.gca().set_xlabel('')
    plt.gca().set_ylabel('')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', title=size)
    plt.gca().get_legend().get_frame().set_edgecolor('black')

    return fig

comp_bubble_charts = {NominalVariables[field_name]: evaluate_comparative_dependency_field(field_name, nominal, generate_comp_bubble_chart)
                       for field_name in nominal.data.columns}

## Fisher's Exact Test

def generate_comp_chi_squared_test(field_name: str, dependency_field_name: str, data: pd.DataFrame):
    variable = get_variable(field_name, NominalVariables)
    dependency_variable = get_variable(dependency_field_name, NominalVariables)

    subset_data = beautify_data_comp(field_name, dependency_field_name,
                                      variable, dependency_variable, data)

    if subset_data.empty: return

    # Check for the condition where both variables are NaN
    if len(subset_data) == 1 and pd.isna(subset_data[field_name]).all() and pd.isna(subset_data[dependency_field_name]).all():
        return

    # Create contingency table
    contingency_table = pd.crosstab(subset_data[field_name], subset_data[dependency_field_name],
                                     values=subset_data['Frequency'], aggfunc='sum', dropna=False).fillna(0)
   
    # Calculating the Chi-squared statistic
    chi2_result = chi2_contingency(contingency_table)

    subset_data = pd.DataFrame({
        'p-value': chi2_result.pvalue # type: ignore
    }, index=[0])

    return subset_data

chi2_exact_test_vector = {NominalVariables[field_name]: evaluate_comparative_dependency_field(field_name, nominal, generate_comp_chi_squared_test)
                       for field_name in nominal.data.columns}

## Shapiro Wilk's Correlation Test

def generate_comp_shapiro_wilk_test(field_name: str, continuous_df: pd.DataFrame):
    subset_data = continuous_df[field_name].fillna(0)

    shapiro_result = shapiro(subset_data)

    statistics, pvalue =  shapiro_result

    subset_data = pd.DataFrame({
        'statistics': statistics,
        'p-value': pvalue
    }, index=[0])

    dataFrameUpdateTitle(subset_data, dataFrameGetTitle('Comparative', "Shapiro Wilk's Correlation Test", field_name))

    return subset_data

comp_shapiro_wilk_tests = {ContinuousVariables[field_name]: generate_comp_shapiro_wilk_test(field_name, continuous.data)
                          for field_name in continuous.data.columns}

## Pearson's Correlation Test

def generate_comp_pearson_cor_test(field_name: str, dependency_field_name: str, data: pd.DataFrame):
    p_value = comp_shapiro_wilk_tests[ContinuousVariables[field_name]]['p-value'][0]
    dp_value = comp_shapiro_wilk_tests[ContinuousVariables[dependency_field_name]]['p-value'][0]

    if not (p_value > 0.05 and dp_value > 0.05): return
    
    # Perform Pearson's correlation test
    pearson_coefficient, p_value = pearsonr(data[field_name].fillna(0), data[dependency_field_name].fillna(0))

    subset_data = pd.DataFrame({
        'pearson coefficient': pearson_coefficient,
        'p-value': p_value
    }, index=[0])

    dataFrameUpdateTitle(subset_data, dataFrameGetTitle('Comparative', "Pearson's Correlation Test", field_name))

    return subset_data

comp_pearson_cor_tests = {ContinuousVariables[field_name]: evaluate_comparative_dependency_field(field_name, continuous, generate_comp_pearson_cor_test)
                       for field_name in continuous.data.columns}

## Spearman's Correlation Test

def generate_comp_spearman_cor_test(field_name: str, dependency_field_name: str, data: pd.DataFrame):
    p_value = comp_shapiro_wilk_tests[ContinuousVariables[field_name]]['p-value'][0]
    dp_value = comp_shapiro_wilk_tests[ContinuousVariables[dependency_field_name]]['p-value'][0]
    
    if  p_value > 0.05 and dp_value > 0.05: return
  
    # Perform Spearman's correlation test
    spearman_result = spearmanr(data[field_name].fillna(0), data[dependency_field_name].fillna(0))

    subset_data = pd.DataFrame({
        'statistic': spearman_result.statistic, # type: ignore
        'p-value': spearman_result.pvalue # type: ignore
    }, index=[0])

    dataFrameUpdateTitle(subset_data, dataFrameGetTitle('Comparative', "Spearman's Correlation Test", field_name))
   
    return subset_data

comp_spearman_cor_tests = {ContinuousVariables[field_name]: evaluate_comparative_dependency_field(field_name, continuous, generate_comp_spearman_cor_test)
                       for field_name in continuous.data.columns}