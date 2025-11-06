import numpy as np
from dataload import dataload, load_parameters, load_opt_parameters
from spectrum_simulator import simulate_spectrum, fit_spectrum, gaussian, simulate_spectra_conditional
from differential import differential, difference, normspectra, deltanu
from peak_finder import peak_intensity, peak_wavenumber, fwhm_calculate
from run_simulation import run_simulation
         
def main():
    outputfilename1 = "difference_spectra_original" # O nome do arquivo gerado contendo todas as diferenças entre os espectros normalizados da corrida (o mesmo nome em pastas differentes)
    outputfilename2 = "_normalized_spectra_shift_"

    # # primeira corrida:
    # foldername = "C:/Users/admin/Documents/Alexandre Honorato/Mestrado/Projeto/DADOS/PROCDATA/Tratamento dos dados - novo/Fluorescence Range Comercial"
    # filename = "SESSFSvalltempeq-090425.txt"
    # params_filename = "SESSFSvalltempeq-090425parameters.txt"
    # run_simulation(foldername, filename, params_filename) # fazer simulação dos espectros 
    # normspectra(foldername, filename, outputfilename1) # calcula diferença entre os espectros originais
    # simulate_spectra_conditional(foldername, filename) # simula os espectros condicionais (apenas variação do pico ou da largura de linha) e calcula diferença entre espectros para essas condições

    # pelo tempo
    foldername = "C:/Users/honoa/Documents/Mestrado/Dados/PROCDATA/Tratamento dos dados - novo/Time fluorescence Ocean Optics Data"
    filename = "SESSFSto100425-selected_spectra.txt"
    times, wavelengths, intensities = dataload(f"{foldername}/{filename}")
    wavenumbers = 1e7/wavelengths
    parameters = []
    for i in range(intensities.shape[1]):
        intensity = intensities[:,i]
        intensitymax, intmaxid = peak_intensity(intensity)
        wnmax = peak_wavenumber(wavenumbers, intmaxid)
        fwhm = fwhm_calculate(intensity, wavenumbers)
        parameters.append([intensitymax, wnmax, fwhm])
    data = np.column_stack((wavenumbers, intensities))
    print(data.shape)
    np.savetxt(f"{foldername}/parameters.txt", parameters, comments='', delimiter='\t')
    np.savetxt(f"{foldername}/{filename.replace('.txt', '')}1.txt", data, header='\t'+'\t'.join(times), comments='', delimiter='\t')
    newfilename = f"{filename.replace('.txt', '')}1.txt"
    normspectra(foldername, newfilename, outputfilename1)




if __name__ == "__main__":
    main()