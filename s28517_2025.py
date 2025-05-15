# =====================================================================
# CEL PROGRAMU:
# Program generuje losową sekwencję DNA (nukleotydy: A, C, G, T) 
# o długości podanej przez użytkownika. Wstawia imię użytkownika
# w losowym miejscu sekwencji (litery imienia nie wpływają na statystyki).
# Zapisuje wynik w formacie FASTA i oblicza statystyki zawartości 
# nukleotydów oraz stosunek CG do AT.
# =====================================================================

import random  # Biblioteka do losowego generowania danych
import os      # Biblioteka pomocna przy obsłudze plików i nazw

# Funkcja do generowania losowej sekwencji DNA
def generate_dna_sequence(length):
    return ''.join(random.choices('ACGT', k=length))

# Funkcja do obliczania statystyk zawartości nukleotydów
def calculate_statistics(sequence):
    total = len(sequence)
    counts = {nuc: sequence.count(nuc) for nuc in 'ACGT'}
    percentages = {nuc: (counts[nuc] / total) * 100 for nuc in 'ACGT'}
    cg = counts['C'] + counts['G']
    at = counts['A'] + counts['T']
    cg_at_ratio = (cg / at) * 100 if at > 0 else 0
    return percentages, cg_at_ratio

# Funkcja do wstawienia imienia użytkownika w losowym miejscu sekwencji
def insert_name_into_sequence(sequence, name):
    insert_pos = random.randint(0, len(sequence))
    return sequence[:insert_pos] + name + sequence[insert_pos:]

# Funkcja do zapisywania sekwencji w formacie FASTA
def save_to_fasta(file_name, seq_id, description, sequence_with_name):
    with open(file_name, 'w') as file:
        file.write(f">{seq_id} {description}\n")
        file.write(sequence_with_name + '\n')

# ULEPSZENIE 1:
# Funkcja do sanityzacji ID sekwencji (np. usunięcie niedozwolonych znaków w nazwie pliku)
def sanitize_id(seq_id):
    return ''.join(c for c in seq_id if c.isalnum() or c in ['_', '-'])

# Główna funkcja programu
def main():
    try:
        length = int(input("Podaj długość sekwencji: "))  # Pobranie długości od użytkownika
        if length <= 0:
            raise ValueError("Długość musi być większa od zera.")
    except ValueError as ve:
        print("Nieprawidłowa długość sekwencji:", ve)
        return

    # ORIGINAL:
    # seq_id = input("Podaj ID sekwencji: ").strip()
    # MODIFIED (walidacja ID sekwencji w celu usunięcia niedozwolonych znaków):
    seq_id_raw = input("Podaj ID sekwencji: ").strip()
    seq_id = sanitize_id(seq_id_raw)

    description = input("Podaj opis sekwencji: ").strip()
    name = input("Podaj imię: ").strip()

    dna_seq = generate_dna_sequence(length)  # Generowanie sekwencji DNA
    dna_stats, cg_at_ratio = calculate_statistics(dna_seq)  # Obliczanie statystyk

    final_sequence = insert_name_into_sequence(dna_seq, name)  # Dodanie imienia do sekwencji

    # ORIGINAL:
    # file_name = f"{seq_id}.fasta"
    # MODIFIED (sprawdzenie, czy plik już istnieje i dodanie numeru jeśli tak):
    file_name = f"{seq_id}.fasta"
    counter = 1
    while os.path.exists(file_name):  # ULEPSZENIE 2: zabezpieczenie przed nadpisaniem pliku
        file_name = f"{seq_id}_{counter}.fasta"
        counter += 1

    save_to_fasta(file_name, seq_id, description, final_sequence)  # Zapis do pliku

    print(f"\nSekwencja została zapisana do pliku {file_name}")
    print("Statystyki sekwencji:")

    # ORIGINAL:
    # for nuc in 'ACGT':
    #     print(f"{nuc}: {dna_stats[nuc]:.1f}%")
    # MODIFIED (lepsze formatowanie wyjścia):
    # ULEPSZENIE 3: wyświetlenie w jednej linii z odstępami, łatwiejsze do odczytania
    print(" | ".join([f"{nuc}: {dna_stats[nuc]:5.1f}%" for nuc in sorted(dna_stats)]))
    print(f"%CG: {dna_stats['C'] + dna_stats['G']:.1f}")
    print(f"Stosunek CG do AT: {cg_at_ratio:.1f}%")

# Uruchomienie programu
if __name__ == "__main__":
    main()
