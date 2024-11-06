# import time
# from tqdm import tqdm

# def process_data():
#     # Inicializa a barra de progresso
#     total_steps_1 = 5  # Passos para a parte 1
#     total_steps_2 = 7  # Passos para a parte 2

#     with tqdm(total=total_steps_1 + total_steps_2, dynamic_ncols=True, position=0) as progress_bar:
#         # Parte 1 do processamento
#         for i in range(total_steps_1):
#             time.sleep(1)  # Simula algum processamento
#             progress_bar.set_description(f"Processing part 1: step {i + 1}/{total_steps_1}")
#             progress_bar.update(1)  # Atualiza a barra de progresso
        
#         # Parte 2 do processamento
#         for i in range(total_steps_2):
#             time.sleep(1)  # Simula algum processamento
#             progress_bar.set_description(f"Processing part 2: step {i + 1}/{total_steps_2}")
#             progress_bar.update(1)  # Atualiza a barra de progresso

# def main():
#     process_data()

# if __name__ == "__main__":
#     main()

import numpy as np

# Arrays de exemplo
temp = np.array([20, 30, 40, 50])
y_real = np.array([3, 5, 2, 8])
y_ajustado = np.array([2.5, 5.2, 1.8, 7.9])

np.savetxt("output_filename.txt", np.column_stack([temp, y_real, y_ajustado]), header='Wavenumber\tMinor Gaussian\tMajor Gaussian', comments='', delimiter='\t')


# try:
#     # Verificando se os conjuntos de dados têm o mesmo tamanho
#     if len(y_real) != len(y_ajustado):
#         raise ValueError("Os conjuntos de dados não têm o mesmo tamanho!")
    
#     # Se não houver erro, o código continua aqui
#     else:
#         print("Os conjuntos de dados têm o mesmo tamanho. Continuando...")
#         n = len(y_real)

# except ValueError:  # Apenas captura o erro e segue
#     print("Erro detectado, mas não irá interromper o código.")
#     # Nenhuma ação adicional é feita aqui

# # O código que vem após o except, fora do try-except, vai continuar executando
# print("Este código será executado, independentemente do erro.")

# # Diferença ao quadrado entre os elementos dos arrays
# diferenca_quadrado = (y_real - y_ajustado) ** 2
# print(diferenca_quadrado)

# # Soma todos os elementos do conjunto
# total = np.sum(diferenca_quadrado)
# print(total)

# # Desvio padrão
# std = np.sqrt(total/n)
# print(std)