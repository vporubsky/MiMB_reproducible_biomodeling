"""
Author: Veronica Porubsky
Description: Program to generate figures for MiMB reproducible modeling study.
(Elowitz and Leibler repressilator model, 2000, DOI: 10.1038/35002125)
See: https://www.ebi.ac.uk/biomodels/BIOMD0000000012 for model documentation on BioModels Database.
"""
# Todo: decide whether to include in final release
import numpy as np
import pandas as pd
from math import pi
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'font.size': 12})


# %% PARAMETER ESTIMATION FIGURES FUNCTIONS
def set_radar_plot_properties(data):
    categories = list(data.keys())
    N = len(categories)

    # Axes angles
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise radar plot
    ax = plt.subplot(111, polar=True)

    # Draw one axe per parameter, and add parameter names
    plt.xticks(angles[:-1], categories)

    # Draw parameter value labels
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4], ["1", "2", "3", "4"], color="grey", size=7)
    plt.ylim(0, 5)

    return ax, angles


#%% Create Radar plot for two sets of parameters -------------------------------------------------------------------------
monte_carlo_data = pd.read_hdf('BIOMD0000000012_monte_carlo_data.h5', 'BIOMD0000000012_estimated_parameters')

ax, angles = set_radar_plot_properties(monte_carlo_data)
parameter_set_idx = [100, 10]
colors = ['b', 'r']
labels = ['parameter set 1', 'parameter set 2']
for idx, set_val in enumerate(parameter_set_idx):
    values = monte_carlo_data.loc[set_val].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=labels[idx])
    ax.fill(angles, values, colors[idx], alpha=0.1)

plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
plt.savefig('BIOMD0000000012_parameter_estimation_two_sets.png', dpi=300)
plt.show()

# Create Radar plot of all parameter sets, use kmeans clustering to identify "families" of parameter values ------------
mat = monte_carlo_data.values
km = KMeans(n_clusters=2)
km.fit(mat)
labels = km.labels_

ax, angles = set_radar_plot_properties(monte_carlo_data)
for i in range(np.shape(monte_carlo_data)[0]):
    values = monte_carlo_data.loc[i].values.flatten().tolist()
    values += values[:1]
    if labels[i] == 1:
        ax.plot(angles, values, linewidth=1, color='royalblue', alpha=0.05, linestyle='solid')
    else:
        ax.plot(angles, values, linewidth=1, color='darkorange', alpha=0.05, linestyle='solid')

plt.savefig('BIOMD0000000012_parameter_estimation_clusters.png', dpi=300)
plt.show()

#%% Plot confidence intervals on histograms ------------------------------------------------------------------------------
sns.set_theme()
sns.set_style('white')
DATA = monte_carlo_data.to_numpy()

CI_lower = np.percentile(DATA, q=2.5, axis=0)
CI_upper = np.percentile(DATA, q=97.5, axis=0)

plt.rcParams.update({'font.size': 14})
fig = plt.figure(figsize=(10, 10))

for i in range(np.shape(DATA)[1]):
    fig.add_subplot(2, 2, i + 1)
    plt.xlabel(monte_carlo_data.keys()[i])
    height, bins, patches = plt.hist(DATA[:, i], bins=25)
    plt.vlines(x=[CI_lower[i], CI_upper[i]], ymin=0, ymax=height.max(), linestyles='dashed')
    plt.fill_betweenx([0, height.max()], CI_lower[i], CI_upper[i], color='b', alpha=0.1)

plt.savefig('BIOMD0000000012_parameter_estimation_histograms.png', dpi=300)
plt.show()

# %%
