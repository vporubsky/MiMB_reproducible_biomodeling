import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import h5py

#%% Write class of parameter estimation helper functions
class ParameterEstimation:
    def __init__(self, model, data, params):
        """
        :param model: RoadRunner object instance
        :param data: numpy.ndarry
        :param params: dict
        """
        self.model = model
        self.data = data
        self.params_ids = list(params.keys())
        self.params_ranges = list(params.values())

    def get_residuals(self):
        """Returns a matrix of residuals."""


    def rmse_obj_function():
        """Returns the RMSE."""
        # generate matrix of residuals between predicted and ground truth values
        residuals = get_residuals()
        least_sq
        return least_sq

    def estimate_parameters(self, experimental_data):

        return

    def monte_carlo(self, num_itr):
        """Excute multiple iterations of parameter estimation.

        num_itr : int
        """
        parameter_sets = np.zeros((self.params, num_itr))
        set_num = []
        for i in range(num_itr):
            # add optimized parameters to array
            set_num += [f'set_{i + 1}']

        monte_carlo = pd.DataFrame(parameter_sets, columns=self.params)
        monte_carlo.insert(0, "Group", set_num, True)

        return

    def plot_confidence_interval(self):



        return


    def plot_radar(self, parameter_sets, save_to_file = True):
        """ Plots a radar plot with

        :param parameter_sets: dict
        :return:
        """
        # number of variable
        categories = list(df)[1:]
        N = len(categories)

        # We are going to plot the first line of the data frame.
        # But we need to repeat the first value to close the circular graph:
        values = df.loc[0].drop('group').values.flatten().tolist()
        values += values[:1]
        values

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        # Initialise the spider plot
        ax = plt.subplot(111, polar=True)

        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], categories, color='grey', size=8)

        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([10, 20, 30], ["10", "20", "30"], color="grey", size=7)
        plt.ylim(0, 40)

        # Plot data
        ax.plot(angles, values, linewidth=1, linestyle='solid')

        # Fill area
        ax.fill(angles, values, 'b', alpha=0.1)

        if save_to_file:
            # save figure


#%% Set up parameter estimation routine

# Load synthetic dataset
data_h5f = h5py.File('repressilator_data.h5', 'r')
data = data_h5f['repressilator_synthetic_dataset'][:]
data_h5f.close()

# Load model and specify parameters and parameter ranges for optimization
biomodels_file_url = 'https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000012?filename=BIOMD0000000012_url.xml'
repressilator_mod = te.loadSBMLModel(biomodels_file_url)

# Choose parameters to estimate
all_parameters = repressilator_mod.getGlobalParameterIds()
parameters_to_fit = ['KM', 'tau_mRNA', 'tau_prot', 'ps_a', 'ps_0']

# Parameter name, minimum search value, initial search value, maximum search value
REPRESSILATOR_PARAMETER_DCT = {
    "KM": (0.001, 5, 10),
    "tau_mRNA": (0.001, 5, 10),
    "tau_mRNA": (0.001, 5, 10),
    "ps_a": (0.001, 5, 10),
    "ps_0": (0.001, 5, 10),
}

# %% Estimate parameters
# Todo:
# write simple parameter estimation


# Todo:
# Run Monte Carlo and store each set of parameters in a labeled file



# Todo:
# Use monte Carlo data to plot CI's


# Todo:
# Sample monte carlo to plot overlapping radar plots

df = pd.DataFrame({
    'group': ['set_1', 'set_2', 'set_3', 'set_4'],
    'KM': [38, 1.5, 30, 4],
    'tau_mRNA': [29, 10, 9, 34],
    'tau_prot': [8, 39, 23, 24],
    'kd_mRNA': [7, 31, 33, 14],
    'kd_prot': [28, 15, 32, 14]
})

