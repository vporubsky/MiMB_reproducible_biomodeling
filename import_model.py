'''
Author: Veronica Porubsky
Description: Script to import BIOMD0000000012 (Elowitz repressilator model, 2000)

See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.'''
import tellurium as te
import tkinter
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
repressilator_mod = te.loadSBMLModel("https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000012?filename=BIOMD0000000012_url.xml")
simulation_result = repressilator_mod.simulate(0, 500, 1000)
repressilator_mod.plot(figsize = (10, 6), xtitle = 'Time', ytitle = 'Concentration')
plt.show()

# Todo:
# Visualize model with SBGN



# Todo:
# Add annotation to antimony



# Todo:
# Show git changelist