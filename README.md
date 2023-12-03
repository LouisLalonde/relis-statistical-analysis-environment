# relis-statistical-classification-environment

## 🔍 Overview

This repository defines the *Relis* statistical classification executable artifacts for the Python environment of the [relis-statistical-classification](https://github.com/LouisLalonde/relis-statistical-classification) (*RSC*) DSL.

The executable artifacts are automatically generated by executing a template code generation with the PHP TWIG library.

Two executable artifacts are generated:

1. relis_statistics_kernel.py
2. relis_statistics_playground.py

The `relis_statistics_kernel` executable artifact defines the analysis configuration, data types (which conforms to the (*RSC*) metamodel), utility functions and statistical functions which are used to perform the statistical classification analysis.  

The `relis_statistics_playground` executable artifact provides a direct access to the various combinations of statistical functions that can be used by the user based on its project specification.

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
