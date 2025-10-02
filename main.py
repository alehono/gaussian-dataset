import numpy as np
from dataload import dataload, load_parameters, load_opt_parameters
from spectrum_simulator import simulate_spectrum, fit_spectrum, gaussian, simulate_spectra_conditional
from differential import differential, difference, normspectra, deltanu
from run_simulation import run_simulation
         
def main():
    outputfilename1 = "difference_spectra_original" # O nome do arquivo gerado contendo todas as diferenças entre os espectros normalizados da corrida (o mesmo nome em pastas differentes)
    outputfilename2 = "_normalized_spectra_shift_"

    # primeira corrida:
    foldername = "C:/Users/admin/Documents/Alexandre Honorato/Mestrado/Projeto/DADOS/PROCDATA/Tratamento dos dados - novo/Fluorescence Range Comercial"
    filename = "SESSFSvalltempeq-090425.txt"
    params_filename = "SESSFSvalltempeq-090425parameters.txt"
    run_simulation(foldername, filename, params_filename) # fazer simulação dos espectros 
    normspectra(foldername, filename, outputfilename1) # calcula diferença entre os espectros originais
    simulate_spectra_conditional(foldername, filename) # simula os espectros condicionais (apenas variação do pico ou da largura de linha) e calcula diferença entre espectros para essas condições
    deltanu(foldername, "normalized_spectra.txt", f"original{outputfilename2}")
    deltanu(foldername, "normalized_simulated_spectra.txt", f"simulated{outputfilename2}")

if __name__ == "__main__":
    main()