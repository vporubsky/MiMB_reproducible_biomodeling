"""
Author: Veronica Porubsky
Description: Query KEGG database for example identifier using the bioservices package.
            Tet repressor protein KEGG Orthology term: http://identifiers.org/kegg.orthology/K18476
"""
from bioservices import *
import pandas as pd
# Todo: clean up
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
print(tetR_dict['DEFINITION'])


# Store data
df = pd.DataFrame()
df.to_excel('BIOMD0000000012_metadata.xlsx')