import numpy as np
from scipy.optimize import curve_fit
from dataload import dataload, load_opt_parameters
from differential import difference

def gaussian(x, amplitude, center, fwhm):
    """Gaussian function."""
    return amplitude * np.exp(-4 * np.log(2) * ((x - center) / fwhm) ** 2)

def simulate_spectrum(x, params):
    """Simulate the spectrum based on the provided parameters."""
    y_simulated = np.zeros_like(x)
    for i in range(0, len(params), 3):
        amplitude = params[i]
        center = params[i + 1]
        fwhm = params[i + 2]
        y_simulated += gaussian(x, amplitude, center, fwhm)
    return y_simulated

def fit_spectrum(x, y, initial_guess):
    """Fit the spectrum using the initial guess for parameters."""
    try:
        optimized_params, covariance = curve_fit(lambda x, *params: simulate_spectrum(x, params), x, y, p0=initial_guess)
    except RuntimeError as e:
        print("Error in fitting:", e)
        optimized_params = initial_guess  # Use initial guess if fitting fails
        covariance = ["none"] # Se o fitting falhar
    return optimized_params, covariance

def simulate_spectra_conditional(foldername, filename):
    # Definindo caminho dos arquivos
    fullfilename = f"{foldername}/{filename}"

    # Ler o arquivo de parâmetros para o espectro a 20ºC:
    "Precisa de especificar o nome do arquivo (algo do tipo foldername/optimized_parameter_20C.txt)"
    param20cfilename = f"{foldername}/optimized_params_20C.txt"
    par20c = load_opt_parameters(param20cfilename)

    # Lê arquivo de valores
    "Criar lista com os valores de temperatura"
    temperatures, x, ys = dataload(fullfilename)

    # Tabelas iniciais:
    peakshiftspectra = [x] # Variação do pico central
    headerpeak = ["peakcenter"]
    fwhmchangespectra = [x] # Variação da largura de linha
    headerfwhm = ["fwhm"]
    
    # simulação dos espectros condicionais:
    for temp in temperatures:
        # Ler o arquivo de parâmetros para o outro espectro:
        "Para cada um vai ter 'foldername/optimized_parameter_{temp}.txt' diferente"
        tempparamfilename = f"{foldername}/optimized_params_{temp}.txt"
        tempparam = load_opt_parameters(tempparamfilename)

        # Calcular o espectro da segunda temperatura apenas com o valor central do pico:
        "Aqui os espectros vão precisar ser calculados e salvos em uma tabela (usando append)"
        peakshiftparams = [par20c[0], tempparam[1], par20c[2], par20c[3], tempparam[4], par20c[5]]
        peakshiftspectrum = simulate_spectrum(x, peakshiftparams)
        "Precisa renormalizar o espectro"
        peakmax = np.max(peakshiftspectrum) # Encontrando o máximo
        norm_peakshiftspectrum = peakshiftspectrum / peakmax # Normalizando a partir do máximo
        peakshiftspectra.append(norm_peakshiftspectrum)
        peak = f"{peakshiftparams[1]}-{temp}"
        headerpeak.append(peak)
        
        # Calcular o espectro da segunda temperatura apenas com o valor da largura de linha:
        "Aqui os espectros vão precisar ser calculados e salvos em uma tabela (usando append)"
        fwhmchangeparams = [par20c[0], par20c[1], tempparam[2], par20c[3], par20c[4], tempparam[5]]
        fwhmchangespectrum = simulate_spectrum(x, fwhmchangeparams)
        "Precisa renormalizar o espectro"
        peakmax = np.max(fwhmchangespectrum) # Encontrando o máximo
        norm_fwhmchangespectrum = fwhmchangespectrum / peakmax # Normalizando a partir do máximo
        fwhmchangespectra.append(norm_fwhmchangespectrum)
        fwhm = f"{peakshiftparams[2]}-{temp}"
        headerfwhm.append(fwhm)
    
    # Salvar resultados:
    # Variação do pico:
    output_filename = f"{foldername}/simulated_peakshift.txt"
    np.savetxt(output_filename, np.column_stack(peakshiftspectra), header='\t'.join(headerpeak).replace('C', '\u00B0C'), comments='', delimiter='\t')
    # Variação da largura de linha:
    output_filename = f"{foldername}/simulated_fwhmchange.txt"
    np.savetxt(output_filename, np.column_stack(fwhmchangespectra), header='\t'.join(headerfwhm).replace('C', '\u00B0C'), comments='', delimiter='\t')

    # Calcular diferença entre os espectros:
    difference(foldername, "simulated_peakshift.txt", "difference_peakshift.txt") # Variação no pico
    difference(foldername, "simulated_fwhmchange.txt", "difference_fwhmchange.txt") # variação na largura de linha