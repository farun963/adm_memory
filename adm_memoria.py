import csv
from collections import deque, OrderedDict


class PageReplacementAlgorithms:
    def __init__(self, frame_size=3):
        self.frame_size = frame_size

    def read_csv(self, filename):
        """Lee la secuencia de páginas desde un archivo CSV"""
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            return [int(page) for row in reader for page in row]

    def fifo_algorithm(self, pages):
        """Implementación del algoritmo FIFO (First In First Out)"""
        frames = []
        page_faults = 0
        page_fault_history = []

        for page in pages:
            # Si la página no está en los marcos actuales
            if page not in frames:
                page_faults += 1

                # Si los marcos están llenos, elimina el primero (más antiguo)
                if len(frames) == self.frame_size:
                    frames.pop(0)

                # Agrega la nueva página
                frames.append(page)

            # Registra el estado actual de los marcos
            page_fault_history.append(list(frames) + ['-'] * (self.frame_size - len(frames)))

        return page_faults, page_fault_history

    def lru_algorithm(self, pages):
        """Implementación del algoritmo LRU (Least Recently Used)"""
        frames = OrderedDict()
        page_faults = 0
        page_fault_history = []

        for page in pages:
            # Si la página ya está en los marcos, actualiza su posición
            if page in frames:
                frames.move_to_end(page)
            else:
                page_faults += 1

                # Si los marcos están llenos, elimina el menos recientemente usado
                if len(frames) == self.frame_size:
                    frames.popitem(last=False)

                # Agrega la nueva página
                frames[page] = None

            # Registra el estado actual de los marcos
            current_frames = list(frames.keys()) + ['-'] * (self.frame_size - len(frames))
            page_fault_history.append(current_frames)

        return page_faults, page_fault_history

    def write_results(self, algorithm_name, page_faults, page_fault_history):
        """Escribe los resultados en un archivo de texto"""
        filename = f"{algorithm_name.lower()}_results.txt"
        with open(filename, 'w') as file:
            file.write(f"{algorithm_name} Algoritmo de Reemplazo de Páginas\n")
            file.write(f"Tamaño de Marco: {self.frame_size}\n")
            file.write(f"Fallos de Página: {page_faults}\n\n")
            file.write("Historial de Estados de Marcos:\n")
            for i, frame_state in enumerate(page_fault_history):
                file.write(f"Paso {i + 1}: {frame_state}\n")


def main():
    # Ruta del archivo CSV
    csv_filename = 'seq_pag.csv'

    # Crear instancia de los algoritmos
    page_replacement = PageReplacementAlgorithms(frame_size=3)

    # Leer páginas desde el CSV
    pages = page_replacement.read_csv(csv_filename)

    # Ejecutar algoritmo FIFO
    fifo_faults, fifo_history = page_replacement.fifo_algorithm(pages)
    page_replacement.write_results("FIFO", fifo_faults, fifo_history)

    # Ejecutar algoritmo LRU
    lru_faults, lru_history = page_replacement.lru_algorithm(pages)
    page_replacement.write_results("LRU", lru_faults, lru_history)

    # Imprimir resultados
    print(f"FIFO - Fallos de Página: {fifo_faults}")
    print(f"LRU  - Fallos de Página: {lru_faults}")


if __name__ == "__main__":
    main()