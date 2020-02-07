goal: plot substrate and products over time in microbial cultures

run:
    "python scripts/plot.py"

required input:
    data/data.xlsx

output:
    data/regression.csv
    results/{culture_name}.pdf

scripts/plot.py is the main script that should be run. This takes raw data from
data/data.xlsx. This raw data can always be updated with new measurements.
The raw data contains values like ppm and uM that are converted to umol/bottle.
Regression lines are then calculated, and this data is plotted and exported to
results/regression.csv. Each culture will have a graph exported like
results/{culture_name}.pdf.

The requirements.yml file expects you are using anaconda.

![control plot](/results/control.png "control")
![culture 1 plot](/results/culture 1.png "culture 1")
![culture 2 plot](/results/culture 2.png "culture 2")