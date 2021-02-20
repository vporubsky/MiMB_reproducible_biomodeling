"""
Author: Veronica Porubsky
Description: Script to import and visualize BIOMD0000000012
(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
import tellurium as te
import matplotlib.pyplot as plt
import matplotlib
from IPython.display import Image
import tempfile
from libsbgnpy import render, utils
matplotlib.use('TkAgg')

# Load model from BioModels Database
repressilator_mod = te.loadSBMLModel("https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000012?filename=BIOMD0000000012_url.xml")

# Simulate model and visualize output
simulation_result = repressilator_mod.simulate(0, 500, 1000)
repressilator_mod.plot(figsize = (10, 6), xtitle = 'Time', ytitle = 'Concentration')
plt.show()


# %% Visualize model network with SBGN
# BIOMD0000000012.sbgn generated using CellDesigner Export SBGN-ML.

repressilator_sbgn = utils.read_from_file("BIOMD0000000012.sbgn")
repressilator_png = tempfile.NamedTemporaryFile(suffix=".png")
render.render_sbgn(repressilator_sbgn,
                   image_file=repressilator_png.name,
                   file_format="png")
Image(repressilator_png.name, width=500)


# Todo:
# Add annotation to antimony
