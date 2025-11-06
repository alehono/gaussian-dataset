import numpy as np
from scipy.interpolate import interp1d
from dataload import dataload
import matplotlib.pyplot as plt

def differential(temps, x, y):
    # Cria as variáveis
    subs = []
    sub_names = []  # Lista para armazenar os nomes das subtrações
    subs = [x]

    # Loop para percorrer todas as colunas de ys
    for i in range(1, y.shape[1]):  # Percorre as colunas de índice 1 até o final
        for j in range(i):  # Percorre as colunas de índice menor que i
            diff = y[:, i] - y[:, j]  # Subtrai a coluna j da coluna i
            subs.append(diff)

            # Adiciona o nome da subtração à lista sub_names
            sub_name = "-".join([temps[i], temps[j]]).replace('\u00B0', '') # Formata o nome
            sub_names.append(sub_name)

    return subs, sub_names

def difference(foldername, filename, outputfilename):
    # Load spectrum data
    full_filename = f"{foldername}/{filename}"
    temps, x, ys = dataload(full_filename)

    # Calculando diferança entre os espectros
    subs, sub_names = differential(temps, x, ys) # Calculando diferança entre os espectros

    # Salvando o arquivo
    subs = np.array(subs)
    output_filename = f"{foldername}/{outputfilename}.txt"
    np.savetxt(output_filename, np.column_stack(subs), header='Wavenumber\t' + '\t'.join(sub_names), comments='', delimiter='\t')
    print(f"Saved data for differencial spectra of {filename} in {foldername}")

# Função para normlaizar os espectros e calcular a diferença:
def normspectra(foldername, filename, outputfilename):
    # Load spectrum data
    full_filename = f"{foldername}/{filename}"
    temps, x, ys = dataload(full_filename)
    print(ys.shape)
    
    # Normalizar
    yn = []
    for i in range(ys.shape[1]):
        spectrum = ys[:, i]  # seleciona a i-ésima coluna (1175 pontos)
        peak = np.max(spectrum)
        print(f"Spectrum {i} peak: {peak}")
        spectrum = spectrum - np.min(spectrum)
        normalized = spectrum / peak
        yn.append(normalized)
    yn = np.array(yn).T
    print(yn.shape)
    # Salvar espectro normalizado
    np.savetxt(f"{foldername}/normalized_spectra.txt", np.column_stack((x, yn)), header='Wavenumber\t' + '\t'.join(temps), comments='', delimiter='\t')
    print(f"Saved data for spectra of normalized {filename} in {foldername}")

    # Calculando diferança entre os espectros
    subs, sub_names = differential(temps, x, yn) # Calculando diferança entre os espectros

    # Salvando o arquivo
    subs = np.array(subs)
    output_filename = f"{foldername}/{outputfilename}.txt"
    np.savetxt(output_filename, np.column_stack(subs), header='Wavenumber\t' + '\t'.join(sub_names), comments='', delimiter='\t')
    print(f"Saved data for differencial spectra of normalized {filename} in {foldername}")

# Interpolação
def interpolatiors(nu, Is):
    intleft = []
    intright = []
    peak_ids = []

    for i in range(Is.shape[1]):
        I = Is[:, i]
        peak_id = np.argmax(I)
        peak_ids.append(peak_id)

        # Lado esquerdo + pico
        Il = I[:peak_id + 1]
        nul = nu[:peak_id + 1]

        # Lado direito
        Ir = I[peak_id:]
        Ir = Ir[::-1]
        nur = nu[peak_id:]
        nur = nur[::-1]

        # interpoladores
        left = interp1d(Il, nul, bounds_error=False, fill_value=np.nan)
        right = interp1d(Ir, nur, bounds_error=False, fill_value=np.nan)

        intleft.append(left)
        intright.append(right)
    
    return intleft, intright, peak_ids

# Fução que cria as grades
def grids(Is, peak_ids, n_p=100):
    n_espectros = Is.shape[1]

    min_lefts = []
    min_rights = []
    min_peak = 1.0
    for i in range(n_espectros):
        I = Is[:, i]
        peak_id = peak_ids[i]
        peak = I[peak_id]
        min_lefts.append(I[0])  # valor mais à esquerda (mínimo para o lado esquerdo)
        min_rights.append(I[-1])  # valor mais à direita (mínimo para o lado direito)
        # pega o valor do pico e compara
        print("pico do espectro", i+1, "é", peak)
        if peak < min_peak:
            min_peak = peak

    print('o menor pico é', min_peak)
    min_left = max(min_lefts) # maior mínimo para garantir todos dentro do intervalo
    min_right = max(min_rights) 
    max_right = 1.0

    I_grid_left = np.linspace(min_left, min_peak, n_p)
    I_grid_right = np.linspace(min_right, min_peak, n_p)
    
    return I_grid_left, I_grid_right

# Função de interpolação
def interpolate(intleft, intright, lgrid, rgrid):
    nspectra = len(intleft)
    nleft = len(lgrid)
    nright = len(rgrid)

    # matrizes
    nul = np.zeros((nleft, nspectra))
    nur = np.zeros((nright, nspectra))

    # Faz interpolação dos dois lados
    for i in range(nspectra):
        nul[:, i] = intleft[i](lgrid)
        nur[:, i] = intright[i](rgrid)
    
    return nul, nur

# Plot data
def plot_data(I_grid_left, nu_left, I_grid_right, nu_right, headers=None):
    n_espectros = nu_left.shape[1]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

    # Lado esquerdo
    ax_left = axes[0]
    for i in range(n_espectros):
        label = headers[i] if headers is not None else f"Espectro {i}"
        ax_left.plot(I_grid_left, nu_left[:, i], label=label)
    ax_left.set_xlabel("Intensidade (esquerda)")
    ax_left.set_ylabel("Frequência ν")
    ax_left.set_title("Interpolação - Lado Esquerdo")
    ax_left.grid(True)
    ax_left.legend()

    # Lado direito
    ax_right = axes[1]
    for i in range(n_espectros):
        label = headers[i] if headers is not None else f"Espectro {i}"
        ax_right.plot(I_grid_right, nu_right[:, i], label=label)
    ax_right.set_xlabel("Intensidade (direita)")
    ax_right.set_title("Interpolação - Lado Direito")
    ax_right.grid(True)
    ax_right.legend()

    plt.tight_layout()
    plt.show()

# Calcular o deslocamento dos espectros:
def deltanu(foldername, filename, outputfilename, saveit=1, plotit=0):
    # Ler arquivo:
    full_filename = f"{foldername}/{filename}"
    temps, x, ys = dataload(full_filename)
    
    # Criar interpoladores
    intleft, intright, peak_ids = interpolatiors(x, ys)

    # Cortar os espectros em duas regiões: uma a direita do pico e outra a esquerda do pico
    lgrid, rgrid = grids(ys, peak_ids) # criar grades

    # Interpolar valores de Intensidade para cada espectro
    freql, freqr= interpolate(intleft, intright, lgrid, rgrid)
    
    # Fazer a subtração entre os dois espectros Dv = vi - vj (i,j = 1,...,n)
    lshifts, lheaders = differential(temps, lgrid, freql)
    rshifts, rheaders = differential(temps, rgrid, freqr)
    lshifts = np.array(lshifts).T
    rshifts = np.array(rshifts).T
    
    print("Shift data has been created for the spectra using interpolation!!")

    # Salvar dados
    if saveit == 1:
        output_filename = f"{foldername}/{outputfilename}left.txt"
        np.savetxt(output_filename, np.column_stack(lshifts), header='Intensity\t' + '\t'.join(lheaders), comments='', delimiter='\t')
        output_filename = f"{foldername}/{outputfilename}right.txt"
        np.savetxt(output_filename, np.column_stack(rshifts), header='Intensity\t' + '\t'.join(rheaders), comments='', delimiter='\t')
        print(f"Saved data for spectra shift of {filename} in {foldername}")
    
    # plot_data(lgrid, freql, rgrid, freqr)
    if plotit == 1:
        plot_data(lshifts[:, 0], lshifts[:, 1:], rshifts[:, 0], rshifts[:, 1:], lheaders)

if __name__ == "__main__":
    foldername = "C:/Users/admin/Documents/Alexandre Honorato/Mestrado/Projeto/DADOS/PROCDATA/Tratamento dos dados - novo/Fluorescence Range Ocean Optics Data - 130924"
    filename = "normalized_simulated_spectrum.txt"
    deltanu(foldername, filename)
    print("Deu tudo certo!!!")