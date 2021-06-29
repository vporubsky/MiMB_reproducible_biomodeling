"""
Author: Veronica Porubsky
Description: Program to test BIOMD0000000012.
(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
import tellurium as te
import unittest
from SBMLLint.tools.sbmllint import lint
import numpy as np


# %% Build model-specific unit testing suite using unittest

# Implement class of helper functions for unit test suite
class BIOMD0000000012TestSuiteHelper:
    """
    Test suite helper functions for BIOMD0000000012.
    """

    def __init__(self, model):
        self.model = model

    def has_mass_balance_errors(self):
        """
        Use sbmllint to check if model has static mass-balance errors.

        :return: bool
        """
        return lint(self.model.getCurrentAntimony(), mass_balance_check="games")

    # Check for complex eigen values
    def has_complex_eigen_vals(self):
        """
        Function to check if model (RoadRunner object instance) has complex eigenvalues.

        :return: bool
        """
        eigen_vals = self.model.getFullEigenValues()
        return any(np.iscomplex(eigen_vals))

    # Add more helper functions to class as needed


# Implement unit test suite
class BIOMD0000000012TestSuite(unittest.TestCase):
    """
    Test suite for BIOMD0000000012.

    To set up the test suite, the user must supply an RoadRunner Object instance called MODEL.
    """

    def setUp(self):
        self.model = MODEL
        self.data = self.model.simulate(0, 500, 50)

    def test_BIOMD0000000012_mass_balance(self):
        """
        Check if model system has mass balance errors.
        """
        self.assertFalse(BIOMD0000000012TestSuiteHelper(model=self.model).has_mass_balance_errors())

    def test_BIOMD0000000012_eigen_vals(self):
        """
        Check if model system has complex eigenvalues after timecourse simulation.
        """
        self.assertTrue(BIOMD0000000012TestSuiteHelper(model=self.model).has_complex_eigen_vals())


if __name__ == "__main__":
    # Load model from BioModels Database and store Antimony string
    BIOMD0000000012 = te.loadSBMLModel(
        "https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000012?filename=BIOMD0000000012_url.xml")
    BIOMD0000000012_ANTIMONY = BIOMD0000000012.getAntimony()

    # Declare test suite input MODEL, a RoadRunner Object instance
    MODEL = BIOMD0000000012

    # Run unit test suite on error-free model
    test_suite = unittest.TestLoader().loadTestsFromTestCase(BIOMD0000000012TestSuite)
    _ = unittest.TextTestRunner().run(test_suite)

    # Run unit test suite on model with error:
    # Set the Hill coefficient parameter 'n' to 0 to remove oscillatory dynamics.
    # This results in the failure of the test for complex eigenvalues.
    MODEL.resetAll()
    MODEL.n = 0
    MODEL.simulate(0, 10, 10)
    MODEL.plot()

    suite = unittest.TestLoader().loadTestsFromTestCase(BIOMD0000000012TestSuite)
    _ = unittest.TextTestRunner().run(suite)
