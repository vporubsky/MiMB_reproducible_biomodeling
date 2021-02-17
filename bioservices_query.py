'''
Author: Veronica Porubsky
Description: Update KEGG identifiers - first, programmatically check KEGG Orthology term for Tet repressor protein.
Then add "http://identifiers.org/kegg.orthology/K18476" identifier annotation to Antimony.'''

from bioservices import *
database = KEGG()

# Retrieve a KEGG entry
tetR_query = database.get("K18476")

# Build a dictionary to parse query
tetR_dict = database.parse(tetR_query)
print(tetR_dict['DEFINITION'])