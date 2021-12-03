"""
Author: Veronica Porubsky
Description: Query KEGG database for example identifier using the bioservices package.
            Tet repressor protein KEGG Orthology term: http://identifiers.org/kegg.orthology/K18476
"""
from bioservices import *
import pandas as pd
# Todo: clean up
# Todo: add seed value to monte carlo/ parameter estimation optimization
# Todo: clean up imports - not working in the jupyter notebook
# Todo: Add additional imports
# Todo: Use os.path.join instead of current paths
# Todo: Add annotations to the parameter estimation HDF5 files and other saved datasets
# Todo: Store imported dataset in .xlsx file for annotation
# Todo: Update README
# Todo: update requirements.txt
# %% Store annotation information
# Select database
database = KEGG()

# Retrieve a KEGG entry
tetR_query = database.get("K18476")

# Build a dictionary to parse query
tetR_dict = database.parse(tetR_query)

# Show information about the query
print(tetR_dict['NAME'])
print(tetR_dict['BRITE'])

# Store collected metadata or experimental measurements
BIOMD0000000012_metadata = pd.DataFrame([[tetR_dict['NAME']],[tetR_dict['BRITE']]],
                                        ['BIOCHEMICAL SPECIES NAME','BRITE'])
BIOMD0000000012_metadata.to_excel('BIOMD0000000012_metadata.xlsx')