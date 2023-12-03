# relis-statistical-analysis-environment

## 🔍 Overview

This repository defines the *Relis* statistical analysis environment artifacts for the Python GPL.

The environment artifacts are seamlessly created using the TWIG template engine's versatile templating system.

Three artifacts are generated:

1. relis_statistics_kernel.py
2. relis_statistics_playground.py
3. requirements.txt

The `relis_statistics_kernel` executable artifact defines the analysis configuration, data types, utility functions and statistical functions which are used to perform the statistical analysis of a *ReLiS* project.  

The `relis_statistics_playground` executable artifact is the entry point for experimenters to retreive the results of their project's statistical analysis. Every combination of statistic analysis is pre-evaluated based on the ReLiS project classification configuration.

The `requirements.txt` contains the Python librairies which the environment depends on.

**Primary authors:** Louis Lalonde [@louislalonde](https://github.com/LouisLalonde) and Hanz Schepens [@Wickkawizz](https://github.com/Wickkawizz)

## 🚀 Execution

1. Download the Python enviroment from your *ReLiS* project
2. Extract it
3. Install the required python libraries with: `pip install -r requirements.txt`
4. Open the relis_statistics_playground.py file with your editor of choice
5. Modulate the visibility of the different statistical analysis results by changing the attribrute `False` to `True`
6. Save the file
7. Execute the file : `python3 relis_statistics_playground.py`

## 📊 Results
- Statistical analysis returning data in tabular format will be displayed in the console.
- Statistical analysis returning figures will be displayed with the maplotlib user interface.
