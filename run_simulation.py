import numpy as np
from dataload import dataload, load_parameters
from spectrum_simulator import simulate_spectrum, fit_spectrum, gaussian
from differential import differential

def run_simulation(foldername, filename, params_filename):
    print(f"Loading Data {foldername}")
    # Load spectrum data
    temperatures, x, ys = dataload(f"{foldername}/{filename}")

    # Load parameters from file
    parameters = load_parameters(f"{foldername}/{params_filename}")
    
    # Creat an array for simulated spectra data
    all_simulated_spectra = [x]

    # Simulate spectrum for each temperature
    for i, y in enumerate(ys.T):
        
        # Get the parameters for the current spectrum
        initial_params = parameters[i]
        
        print(f"Optimizing Parameters for {temperatures[i]}")
        # Fit spectrum
        optimized_params = fit_spectrum(x, y, initial_params)
        # optimized_params[1] = initial_params[1]
        print(f"Finished optimized parameters for {temperatures[i]}")
        
        print(f"Simulating spectrum for {temperatures[i]}")
        # Simulate spectrum with optimized parameters
        simulated_spectrum = simulate_spectrum(x, optimized_params)

        # Encontrando o pico
        peak = np.max(simulated_spectrum)
        
        # Normalizando o espectro
        normalized_spectrum = simulated_spectrum / peak

        #append spectrum in the dataset
        all_simulated_spectra.append(normalized_spectrum)
        
        # Calculating gaussians with optimized parameters
        gaussians = [x]
        for j in range(0, len(optimized_params), 3):
            amplitude = optimized_params[j]
            center = optimized_params[j + 1]
            fwhm = optimized_params[j + 2]
            gaus = gaussian(x, amplitude, center, fwhm)
            
            # Normalizing by the simulated spectrum
            normalized_gaus = gaus / peak
            gaussians.append(normalized_gaus)

        # Save gaussians
        gaussians = np.array(gaussians)
        temperature = temperatures[i]
        output_filename = f"{foldername}/simulated_spectrum_{temperature}.txt"
        np.savetxt(output_filename, np.column_stack(gaussians), header='Wavenumber\tMinor Gaussian\tMajor Gaussian', comments='', delimiter='\t')

        # Save optimized parameters
        temperature = temperatures[i]
        params_filename = f"{foldername}/optimized_params_{temperature}.txt"
        np.savetxt(params_filename, optimized_params.reshape(1, -1), header='Amplitude1\tCenter1\tFWHM1\tAmplitude2\tCenter2\tFWHM2', comments='', delimiter='\t')
        print(f"Finished simulation for {temperatures[i]}")

    # Verificar se todos os espectros têm o mesmo tamanho
    all_simulated_spectra = np.array(all_simulated_spectra)

    # Save results
    output_filename = f"{foldername}/simulated_spectrum.txt"
    np.savetxt(output_filename, np.column_stack(all_simulated_spectra), header='Wavenumber\t' + '\t'.join(temperatures).replace('C', '\u00B0C'), comments='', delimiter='\t')

    # Load spectrum data
    filename = f"{foldername}/simulated_spectrum.txt"
    temps, x, y = dataload(filename)

    # Calculando diferança entre os espectros
    subs, sub_names = differential(temps, x, y)

    # Salvando o arquivo
    subs = np.array(subs)
    output_filename = f"{foldername}/differential_spectra.txt"
    np.savetxt(output_filename, np.column_stack(subs), header='Wavenumber\t' + '\t'.join(sub_names), comments='', delimiter='\t')
    print(f"Saved data for {foldername}")