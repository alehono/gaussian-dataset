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
        temperature = temperatures[i] # A temperatura da amostra que foi medido o espectro
        
        print(f"Optimizing Parameters for {temperatures[i]}")
        # Fit spectrum
        optimized_params, covariance = fit_spectrum(x, y, initial_params)
        # optimized_params[1] = initial_params[1]
        print(f"Finished optimized parameters for {temperatures[i]}")
        
        print(f"Simulating spectrum for {temperatures[i]}")
        # Simulate spectrum with optimized parameters
        simulated_spectrum = simulate_spectrum(x, optimized_params)

        # Encontrando o pico
        peak = np.max(simulated_spectrum)
        
        # Normalizando o espectro
        normalized_spectrum = simulated_spectrum / peak
        
        # Tentar fazer métricas estatísticas:
        try:
            if len(y) != len(normalized_spectrum): # Confirmar que y_real e y_simulado
                raise ValueError("Os conjuntos de dados não têm o mesmo tamanho!")
            else:
                print("Os conjuntos de dados têm o mesmo tamanho.")

                # Calcular os valores de  R^2
                ss_res = np.sum((y - normalized_spectrum)**2) # soma do quadrado dos resíduos
                y_mean = np.mean(y) # Achar y_médio da curva real
                ss_tot = np.sum((y - y_mean)**2) # soma dos quadrados totais
                r_sq = 1 - ss_res/ss_tot # Achar R^2        
                
                # Calcular os valores de  desvio padrão
                n = len(y) # achar tamanho do conjunto de dados (n)
                std = np.sqrt(ss_res/n) # cálculo desvio padrão

        # Excessões:
        except ValueError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

        "SALVAR AS COVARIÂNCIAS EM UM ARQUIVO COM A PRIMEIRA COLUNA DA PRIMEIRA LINHA VAZIA, A PRIMEIRA LINHA COM O NOME DOS PARÂMETROS E A PRIMEIRA COLUNA TAMBÉM"
        "NOME DO ARQUIVO: covariance_value_simulated_spectrum_at_{}"
        headcol = np.array(["amplitude1", "peak center1", "fwhm1", "amplitude2", "peak center2", "fwhm2"])
        output_filename = f"{foldername}/covariance_value_simulated_spectrum_at_{temperature}.txt"
        np.savetxt(output_filename, np.column_stack((headcol, covariance)), header='\tamplitude1\tpeak center1\tfwhm1\tamplitude2\tpeak center2\tfwhm2', comments='', fmt='%s', delimiter='\t')

        "SALVAR AS MÉTRICAS ESTATÍSTICAS EM UM ARRAY E ANEXAR EM UM 'ARRAY' COM LINHAS RELACIONADAS ÀS"
        "TEMPERATURAS DA MEDIDA REFERENTE AO CONJUNTO DE DADOS USADO PARA O AJUSTE DA CURVA SIMULADA - PRECISA CRIAR O ARRAY INICIAL ANTES"
        "SALVAR UM ARQUIVO EM QUE OS DADOS ESTATÍSTICOS DO ARRAY ANTERIOR ESTÃO EM CADA LINHA COM A TEMPERATURA COMO PRIMEIRA COLUNA, R^2 COMO SEGUNDA E"
        "DESVIO PADRÃO COMO TERCEIRA EM QUE A PRIMEIRA LINHA SEJA UM CABEÇALHO COM O NOME DAS COLUNAS (VER ONDE ESSA PARTE DO CÓDIGO SE ENCAIXA)"

        # Append spectrum in the dataset
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
        output_filename = f"{foldername}/simulated_spectrum_{temperature}.txt"
        np.savetxt(output_filename, np.column_stack(gaussians), header='Wavenumber\tMinor Gaussian\tMajor Gaussian', comments='', delimiter='\t')

        # Save optimized parameters
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