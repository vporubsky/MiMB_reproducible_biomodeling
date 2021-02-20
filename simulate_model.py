"""
Author: Veronica Porubsky
Description: Script to simulate BIOMD0000000012
(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
import tellurium as te
import phrasedml
import matplotlib.pyplot as plt
import matplotlib
import os
import h5py
matplotlib.use('TkAgg')

# Load model from BioModels Database
repressilator_mod = te.loadSBMLModel(
    "https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000012?filename=BIOMD0000000012_url.xml")

# Export SBML model file to current working directory
repressilator_mod.exportToSBML('BIOMD0000000012.xml')


# %% Write and export SED-ML using phraSED-ML

# Write phraSED-ML string specifying the simulation study
phrasedml_str = '''
  // Set model
  BIOMD0000000012 = model "BIOMD0000000012.xml" 

  // Deterministic simulation
  det_sim = simulate uniform(0, 500, 1000)
  run_det_sim = run det_sim on BIOMD0000000012
  plot "Repressilator dynamics" run_det_sim.time vs run_det_sim.PX
'''

# Generate SED-ML string from the phraSED-ML string
repressilator_mod.resetAll()
sbml_str = repressilator_mod.getSBML()
phrasedml.setReferencedSBML("BIOMD0000000012.xml", sbml_str)
sedml_str = phrasedml.convertString(phrasedml_str)

# Save the SED-ML simulation experiment to your current working directory
te.saveToFile('BIOMD0000000012_sedml.xml', sedml_str)

# Load and run SED-ML script
te.executeSEDML('BIOMD0000000012_sedml.xml')


# %% Generate COMBINE archive

# get Antimony string of BIOMD0000000012
from store_antimony_model import repressilator_antimony

# create an inline OMEX string
inline_omex = '\n'.join([repressilator_antimony, phrasedml_str])

# export to a COMBINE archive
archive_name = os.path.join(os.getcwd(), 'BIOMD0000000012.omex')
te.exportInlineOmex(inline_omex, archive_name)

# execute COMBINE archive
te.convertAndExecuteCombineArchive('BIOMD0000000012.omex')


# %% Simulate with Tellurium and libroadrunner and export model to SBML

# Run simulation from time 0 to 500, collecting 1000 timepoints
simulation_result = repressilator_mod.simulate(0, 500, 1000)

# Plot simulation results for visualization
repressilator_mod.plot(figsize=(10, 6),
                       xtitle='Time',
                       ytitle='Concentration')
plt.show()

#%% Store simulation results in HDF5

# write HDF5 file for simulation results
h5f = h5py.File('BIOMD0000000012_simulation_results.h5', 'w')
dset = h5f.create_dataset('BIOMD0000000012_tellurium_simulation', data=simulation_result)
dset.attrs['Version information'] = te.getVersionInfo()
dset.attrs['BioModels Database ID'] = 'BIOMD0000000012'
dset.attrs['Model system'] = 'repressilator'
h5f.close()

# Load and plot HDF5 dataset
data_h5f = h5py.File('BIOMD0000000012_simulation_results.h5', 'r')
data = data_h5f['BIOMD0000000012_tellurium_simulation'][:]

# Visualize simulation results
plt.plot(data[:,0], data[:,1:])

# View dataset attributes
for key in list(data_h5f['BIOMD0000000012_tellurium_simulation'].attrs.keys()):
    print(f"{key}: {data_h5f['BIOMD0000000012_tellurium_simulation'].attrs[key]}")

data_h5f.close()
