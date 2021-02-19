import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import h5py


def get_data(model, noise_level, time_start, time_end, num_pts, species):
    """
    Returns a noisy synthetic dataset for a model to use in the workspace.

    model : RoadRunner object instance
    noise_level : float
    time_start : float
    time_end: float
    num_pts : int
    species : list
    """
    # Reset model to original state
    model.resetAll()

    # Run simulation, store data (concentration measurements) and time
    simulation_result = model.simulate(time_start, time_end, num_pts, ['time'] + species)

    # Create matrix of Gaussian distributed noise
    noise = np.random.normal(0, 1, simulation_result.shape)
    for col_idx in range(np.shape(noise)[1]):
        if col_idx == 0:
            # Set first column to 0, so time will be unchanged
            noise[:, col_idx] *= 0
        else:
            # Scale noise matrix
            noise[:, col_idx] *= max(simulation_result[:, col_idx]) * noise_level

    # Set negative values to zero for physiological relevance
    noise_data = np.where(simulation_result + noise < 0, 0, simulation_result + noise)
    return noise_data


if __name__ == "__main__":
    # Load model
    file_url = 'https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000012?filename=BIOMD0000000012_url.xml'
    repressilator_mod = te.loadSBMLModel(file_url)

    # Declare species to generate synthetic data for
    species = ['PX', 'PY', 'PZ']

    # Get synthetic dataset
    data = get_data(repressilator_mod, noise_level=0.3, time_start=0, time_end=500, num_pts=50,
                    species=species)

    # Visualize noisy synthetic data
    plt.plot(data[:, 0], data[:, 1:], '.')
    plt.legend(species)
    plt.show()

    # Save HDF5 dataset
    h5f = h5py.File('repressilator_data.h5', 'w')
    h5f.create_dataset('repressilator_synthetic_dataset', data=data)
    h5f.close()
