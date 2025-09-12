import numpy as np
from dataload import dataload, load_parameters, load_opt_parameters
from spectrum_simulator import simulate_spectrum, fit_spectrum, gaussian, simulate_spectra_conditional
from differential import differential, difference
from run_simulation import run_simulation
         
def main():
    outputfilename = "differential_spectra_original" # O nome do arquivo gerado contendo todas as diferenças entre os espectros normalizados da corrida (o mesmo nome em pastas differentes)

    # primeira corrida:
    foldername = "C:/Users/admin/Documents/Alexandre Honorato/Mestrado/Projeto/DADOS/PROCDATA/Tratamento dos dados - novo/Second_Run-spec_dataXtemp"
    filename = "Second_Run-spec_dataXtemp-original.txt"
    params_filename = "parameters.txt"
    run_simulation(foldername, filename, params_filename) # fazer simulação dos espectros
    difference(foldername, filename, outputfilename) # calcula diferença entre os espectros originais
    simulate_spectra_conditional(foldername, filename) # simula os espectros condicionais (apenas variação do pico ou da largura de linha) e calcula diferença entre espectros para essas condições

if __name__ == "__main__":
    main()