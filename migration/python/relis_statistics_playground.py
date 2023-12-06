from relis_statistics_kernel import (
    NominalVariables, ContinuousVariables,
    desc_frequency_table, desc_statistics, desc_bar_plot, desc_box_plot, desc_violin_plot, 
    evo_plot, evo_frequency_table, comp_stacked_bar_plot, comp_grouped_bar_plot,
    comp_chi_squared_test, comp_spearman_cor_test, comp_frequency_table, comp_bubble_chart,
    comp_shapiro_wilk_test, comp_pearson_cor_test
)


desc_frequency_table(NominalVariables.industrial, True)

desc_frequency_table(NominalVariables.bidirectional, False)

comp_frequency_table(NominalVariables.industrial, NominalVariables.domain, True)

comp_stacked_bar_plot(NominalVariables.industrial, NominalVariables.domain, True)

desc_bar_plot(NominalVariables.domain, True)

comp_chi_squared_test(NominalVariables.scope, NominalVariables.domain, True)

comp_spearman_cor_test(ContinuousVariables.publication_year, ContinuousVariables.targeted_year, True)

comp_shapiro_wilk_test(ContinuousVariables.publication_year, True)

comp_pearson_cor_test(ContinuousVariables.publication_year, ContinuousVariables.targeted_year, True)

# display_data(desc_frequency_tables[NominalVariables.industrial], True)

# display_data(desc_statistics[ContinuousVariables.publication_year], True)

# display_figure(desc_bar_plots[NominalVariables.bidirectional], True)

# display_figure(desc_bar_plots[NominalVariables.industrial], True)

# display_figure(desc_box_plots[ContinuousVariables.publication_year], False)

# display_figure(desc_violin_plots[ContinuousVariables.publication_year], True)

# display_data(evo_frequency_tables[NominalVariables.bidirectional], True)

# display_figure(evo_plots[NominalVariables.bidirectional], True)

# display_figure(comp_stacked_bar_plots[NominalVariables.bidirectional][NominalVariables.domain], False)

# display_figure(comp_grouped_bar_plots[NominalVariables.bidirectional][NominalVariables.target_language], True)

# display_data(comp_chi_squared_tests[NominalVariables.venue][NominalVariables.industrial], True)

# display_data(comp_shapiro_wilk_tests[ContinuousVariables.targeted_year], True)

# display_data(comp_pearson_cor_tests[ContinuousVariables.publication_year][ContinuousVariables.targeted_year], True)

# display_data(comp_spearman_cor_tests[ContinuousVariables.publication_year][ContinuousVariables.targeted_year], True)

input("Press enter to close...")