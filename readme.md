### plot substrate and products over time in microbial cultures

**run:**  
"python scripts/plot.py"

**required input:**  
data/data.xlsx

**output:**    
data/regression.csv  
results/{culture_name}.png
 
scripts/plot.py is the main script that should be run. This takes raw data from
data/data.xlsx. This raw data can always be updated with new measurements.
The raw data contains values like ppm and uM that are converted to umol/bottle.
Regression lines are then calculated, and this data is plotted and exported to
results/regression.csv. Each culture will have a graph exported like
results/{culture_name}.png.

The requirements.yml file expects you are using anaconda.

culture 1
<img src="/results/culture_1.png" alt="culture 1 plot" width="500"/>

culture 2
<img src="/results/culture_2.png" alt="culture 2 plot" width="500"/>   
      
control
<img src="/results/control.png" alt="control plot" width="500"/>
