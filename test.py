import time
from tqdm import tqdm

def process_data():
    # Inicializa a barra de progresso
    total_steps_1 = 5  # Passos para a parte 1
    total_steps_2 = 7  # Passos para a parte 2

    with tqdm(total=total_steps_1 + total_steps_2, dynamic_ncols=True, position=0) as progress_bar:
        # Parte 1 do processamento
        for i in range(total_steps_1):
            time.sleep(1)  # Simula algum processamento
            progress_bar.set_description(f"Processing part 1: step {i + 1}/{total_steps_1}")
            progress_bar.update(1)  # Atualiza a barra de progresso
        
        # Parte 2 do processamento
        for i in range(total_steps_2):
            time.sleep(1)  # Simula algum processamento
            progress_bar.set_description(f"Processing part 2: step {i + 1}/{total_steps_2}")
            progress_bar.update(1)  # Atualiza a barra de progresso

def main():
    process_data()

if __name__ == "__main__":
    main()