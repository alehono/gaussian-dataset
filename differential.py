import numpy as np
from dataload import dataload

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
    print(f"Saved data for {foldername}")