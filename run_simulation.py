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
    
    # Initial arrays for data storage
    all_simulated_spectra = [x] # Create an array for simulated spectra data
    all_simulated_spectra_normalizedpeak = [x] # Create an array for simulated spectra data
    std_list = [] # Desvio padrão
    r_2list = [] # R^2

    # Simulate spectrum for each temperature
    for i, y in enumerate(ys.T):
        
        # Get the parameters for the current spectrum
        initial_params = parameters[i]
        temperature = temperatures[i] # A temperatura da amostra que foi medido o espectro
        
        print(f"Optimizing Parameters for {temperatures[i]}")
        # Otimização do espectro
        optimized_params, covariance = fit_spectrum(x, y, initial_params)
        print(f"Finished optimized parameters for {temperatures[i]}")
        
        # Simulação do espectro com parâmetros otimizados
        print(f"Simulating spectrum for {temperatures[i]}")
        simulated_spectrum = simulate_spectrum(x, optimized_params)
        
        # Normalizando o espectro
        peak = np.max(simulated_spectrum) # Encontrando o pico
        normalized_spectrum = simulated_spectrum / peak
        
        # Tentar fazer métricas estatísticas:
        try:
            if len(y) != len(simulated_spectrum): # Confirmar que y_real e y_simulado
                raise ValueError("Os conjuntos de dados não têm o mesmo tamanho!")
            else:
                # Calcular os valores de  R^2
                ss_res = np.sum((y - simulated_spectrum)**2) # soma do quadrado dos resíduos
                y_mean = np.mean(y) # Achar y_médio da curva real
                ss_tot = np.sum((y - y_mean)**2) # soma dos quadrados totais
                r_sq = 1 - ss_res/ss_tot # Achar R^2
                r_2list.append(r_sq) # Adiciona valor do R^2 à lista       
                
                # Calcular os valores de  desvio padrão
                n = len(y) # achar tamanho do conjunto de dados (n)
                std = np.sqrt(ss_res/n) # cálculo desvio padrão
                std_list.append(std) # Adiciona valor do desvio padrão à lista       

        # Excessões:
        except ValueError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
        
        # Append spectrum in the dataset
        all_simulated_spectra.append(simulated_spectrum)
        all_simulated_spectra_normalizedpeak.append(normalized_spectrum)
        
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
        output_filename = f"{foldername}/normalized_simulated_spectrum_{temperature}.txt"
        np.savetxt(output_filename, np.column_stack(gaussians), header='Wavenumber\tMajor Gaussian\tMinor Gaussian', comments='', delimiter='\t')

        # Salvar os dados de covariância de cada simulação
        headcol = np.array(["amplitude1", "peak center1", "fwhm1", "amplitude2", "peak center2", "fwhm2"]) # Coluna de parâmetros
        output_filename = f"{foldername}/covariance_value_simulated_spectrum_at_{temperature}.txt"
        np.savetxt(output_filename, np.column_stack((headcol, covariance)), header='\tamplitude1\tpeak center1\tfwhm1\tamplitude2\tpeak center2\tfwhm2', comments='', fmt='%s', delimiter='\t')

        # Save optimized parameters
        params_filename = f"{foldername}/{filename.replace('.txt', f'{temperature}-')}optimized_parameters.txt"
        np.savetxt(params_filename, optimized_params.reshape(1, -1), header='Amplitude1\tCenter1\tFWHM1\tAmplitude2\tCenter2\tFWHM2', comments='', delimiter='\t')
        print(f"Finished simulation for {temperatures[i]}")

    # Salvando os dados estatísticos de todas as simulações
    stat_met = np.array([temperatures, r_2list, std_list]) # Create an array of statistical metrics and the temperature 
    output_filename = f"{foldername}/all_simulated_spectra_statiscal_metrics.txt"
    np.savetxt(output_filename, np.column_stack(stat_met), header='TEMPERATURE OF THE RUN\tR^2\tSTANDARD DEVIATION', comments='', fmt='%s', delimiter='\t')

    # Verificar se todos os espectros têm o mesmo tamanho
    all_simulated_spectra = np.array(all_simulated_spectra)

    # Save results
    output_filename = f"{foldername}/simulated_spectra.txt"
    np.savetxt(output_filename, np.column_stack(all_simulated_spectra), header='Wavenumber\t' + '\t'.join(temperatures).replace('C', '\u00B0C'), comments='', delimiter='\t')
    output_filename2 = f"{foldername}/normalized_simulated_spectra.txt"
    np.savetxt(output_filename2, np.column_stack(all_simulated_spectra_normalizedpeak), header='Wavenumber\t' + '\t'.join(temperatures).replace('C', '\u00B0C'), comments='', delimiter='\t')

    # Load spectrum data
    filename = f"{foldername}/normalized_simulated_spectra.txt"
    temps, x, y = dataload(filename)

    # Calculando diferança entre os espectros
    subs, sub_names = differential(temps, x, y)

    # Salvando o arquivo
    subs = np.array(subs)
    output_filename = f"{foldername}/differential_spectra.txt"
    np.savetxt(output_filename, np.column_stack(subs), header='Wavenumber\t' + '\t'.join(sub_names), comments='', delimiter='\t')
    print(f"Saved data for {foldername}")