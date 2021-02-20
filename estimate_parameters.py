"""
Author: Veronica Porubsky
Description: Script to estimate parameters for BIOMD0000000012
(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import h5py
from lmfit import Minimizer, Parameters, Parameter

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
        self.num_params = len(self.params_ids)

    def get_residuals(self, params):
        """ Returns matrix of residuals, or differences between the
        observed (synthetic) dataset and the simulated dataset.

        :param params:
        :return:
        """
        # reset model to initial concentration conditions
        self.model.reset()
        # generate matrix of residuals between predicted and ground truth values
        vals = params.valuesdict()
        for param in list(vals.keys()):
            self.model.setValue(param, vals[param])

        # define simulation experiment time sampling
        time_start = self.data[0,0]; time_end = self.data[-1,0] ; num_pts = np.shape(self.data)[0]

        # simulate model using estimated parameter set to predict output
        model_prediction = self.model.simulate(time_start, time_end, num_pts, list(vals.keys()))
        return model_prediction - self.data

    def rmse_obj_function(self, params):
        """Returns the root mean squared error generated from the
         observed (synthetic) dataset and the simulated dataset.

        :param params:
        :return:
        """
        residuals = self.get_residuals(params)
        return np.sum(np.square(residuals)/self.num_params)

    def estimate_parameters(self):

        # add parameters to estimate to Parameters() dictionary
        params = Parameters()
        for idx, param_id in enumerate(self.params_ids):
            params[param_id] = Parameter(name=param_id,
                                   value=self.params_ranges[idx][1],
                                   min=self.params_ranges[idx][0],
                                   max=self.params_ranges[idx][2])

        # initialize minimization routine
        fitter = Minimizer(userfcn=self.get_residuals(params=params), params=params)

        # Minimize the objective using parameter ranges and lmfit
        optimized_params = fitter.minimize()
        estimated_params_data = {'optimized_vals': optimized_params}

        return estimated_params_data

    def monte_carlo(self, num_itr):
        """Excute multiple iterations of parameter estimation.

        num_itr : int
        """
        parameter_sets = np.zeros((self.params, num_itr))
        set_num = []
        for i in range(num_itr):


            # resampled dataset
            # add residuals
            resampled_data = []

            # estimate parameters
            est_params = self.estimate_parameters(experimental_data=resampled_data)

            # add optimized parameters to array
            parameter_sets[:, i] = est_params

            # add set number tag to list
            set_num += [f'set_{i + 1}']

        monte_carlo = pd.DataFrame(parameter_sets, columns=self.params)
        monte_carlo.insert(0, "Group", set_num, True)

        return

    def plot_confidence_interval(self, parameter_sets, save_to_file = True, file_name=None):
        """

        :param parameter_sets:
        :param save_to_file:
        :param file_name:
        :return:
        """


        return


    def plot_radar(self, parameter_sets, save_to_file = True, file_name = None):
        """

        :param parameter_sets:
        :param save_to_file:
        :param file_name:
        :return:
        """
        # ------- PART 1: Create background

        # number of variable
        categories = list(df)[1:]
        N = len(categories)

        # Define angles for each axis
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        ax = plt.subplot(111, polar=True)

        # First axis at top position:
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)

        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], categories)

        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([10, 20, 30], ["10", "20", "30"], color="grey", size=7)
        plt.ylim(0, 40)

        # ------- PART 2: Add plots

        # Plot each individual = each line of the data
        # I don't do a loop, because plotting more than 3 groups makes the chart unreadable

        # Ind1
        values = df.loc[0].drop('group').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label="group A")
        ax.fill(angles, values, 'b', alpha=0.1)

        # Ind2
        values = df.loc[1].drop('group').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label="group B")
        ax.fill(angles, values, 'r', alpha=0.1)

        # Add legend
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        plt.show()

        if save_to_file:
            # save figure
            if file_name is None:
                file_name = 'radar_plot.png'
            else:
                plt.savefig(file_name, dpi=300)
                print('saved to file')


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
REPRESSILATOR_PARAMETERS = {
    "KM": (0.001, 5, 10),
    "tau_mRNA": (0.001, 5, 10),
    "tau_mRNA": (0.001, 5, 10),
    "ps_a": (0.001, 5, 10),
    "ps_0": (0.001, 5, 10),
}

test_1 =  ParameterEstimation(model=repressilator_mod, data=data, params=REPRESSILATOR_PARAMETERS)
test_1.estimate_parameters()
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

df = pd.DataFrame({
    'group': ['A', 'B', 'C', 'D'],
    'var1': [38, 1.5, 30, 4],
    'var2': [29, 10, 9, 34],
    'var3': [8, 39, 23, 24],
    'var4': [7, 31, 33, 14],
    'var5': [28, 15, 32, 14]
})

repressilator_pe = ParameterEstimation(model=repressilator_mod,
                                       data=data,
                                       params=REPRESSILATOR_PARAMETERS)
repressilator_pe.plot_radar(parameter_sets=df)
