from relis_statistics_lib import (
    display_data, display_figure, NominalVariables, ContinuousVariables,
    desc_frequency_tables, desc_bar_plots, desc_box_plots, desc_violin_plots,
    evo_plots, comp_stacked_bar_plots, comp_grouped_bar_plots
)

display_data(desc_frequency_tables[NominalVariables.industrial], True)

display_figure(desc_bar_plots[NominalVariables.bidirectional], False)

display_figure(desc_bar_plots[NominalVariables.industrial], False)

display_figure(desc_box_plots[ContinuousVariables.publication_year], False)

display_figure(desc_violin_plots[ContinuousVariables.publication_year], True)

display_figure(evo_plots[NominalVariables.bidirectional], False)

display_figure(comp_stacked_bar_plots[NominalVariables.bidirectional][NominalVariables.domain], True)

display_figure(comp_grouped_bar_plots[NominalVariables.bidirectional][NominalVariables.domain], True)

input("Press enter to close...")