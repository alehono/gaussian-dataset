import numpy as np

def dataload(filename):
    """Load data from a file, ignoring the first value in the first row and first column."""
    # Load data, ignoring the first row
    data = np.loadtxt(filename, delimiter='\t', dtype=str)
    
    # Temperatures: all values from the first row except the first
    temperatures = data[0, 1:]
    temperatures = [temp.replace('Âº', '').replace('Â°', '') for temp in temperatures]
    
    # Convert commas to dots for decimal numbers
    data = data[1:, ]
    data = np.array([[float(x.replace(',', '.')) for x in line] for line in data])
    
    # Wavenumber: all values from the first column, starting from the second row
    x = data[:, 0]  
    # Spectrum columns: all columns starting from the second column
    ys = data[:, 1:]  

    return temperatures, x, ys

def load_parameters(filename):
    """Load fitting parameters from a file."""
    # Carregar parâmetros e converter vírgulas em pontos
    params = np.loadtxt(filename, delimiter=None, dtype=str)
    params = np.array([[float(x.replace(',', '.')) for x in line] for line in params])
    return params

def load_opt_parameters(filename):
    """Load fitting parameters from a file."""
    # Carregar parâmetros e converter vírgulas em pontos
    data = np.loadtxt(filename, delimiter=None, dtype=str)
    params = data[1, :]
    params = np.array([float(x.replace(',', '.')) for x in params])
    return params