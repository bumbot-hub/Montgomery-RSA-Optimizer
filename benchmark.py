import time
import matplotlib.pyplot as plt
import numpy as np
from src.rsa_simulator import RSASimulator
from sympy import mod_inverse, nextprime

def estimate_hardware_performance(bit_size, frequency_mhz=200):
    """
    Oblicza teoretyczne parametry sprzętowe dla architektury Digit-Serial Radix-2.
    """
    # 1 mnożenie REDC = k cykli (gdzie k to liczba bitów)
    cycles_per_mult = bit_size
    # Średnio 1.5 * k mnożeń na jedno potęgowanie RSA (Square-and-Multiply)
    avg_mults_per_exp = int(1.5 * bit_size)
    total_cycles = cycles_per_mult * avg_mults_per_exp
    
    # Czas [s] = Cykle / Częstotliwość [Hz]
    estimated_time_ms = (total_cycles / (frequency_mhz * 1_000_000)) * 1000
    return total_cycles, estimated_time_ms

def run_benchmark():
    bit_sizes = [512, 1024, 2048, 4096, 8192]
    times_python = []      # Czas zmierzony w Pythonie (symulacja)
    times_hardware = []    # Estymowany czas rzeczywisty na FPGA (200MHz)
    cycles_list = []       # Liczba cykli zegara
    ff_costs = []          # Liczba przerzutników FF

    print(f"{'Bity':<7} | {'Python (ms)':<15} | {'FPGA Est. (ms)':<15} | {'Cykle zegara':<15} | {'FF Cost'}")
    print("-" * 75)

    for bits in bit_sizes:
        # Generowanie parametrów
        p = nextprime(1 << (bits // 2))
        q = nextprime(p + 1000)
        n, e = p * q, 65537
        d = mod_inverse(e, (p-1)*(q-1))
        
        rsa = RSASimulator(n, e, d)
        msg = n // 3

        # Pomiar w Pythonie
        start = time.time()
        rsa.encrypt(msg)
        t_py_ms = (time.time() - start) * 1000
        times_python.append(t_py_ms)

        # Estymacja sprzętowa (200 MHz)
        cycles, t_hw_ms = estimate_hardware_performance(bits, frequency_mhz=200)
        times_hardware.append(t_hw_ms)
        cycles_list.append(cycles)
        ff_costs.append(4 * bits)

        print(f"{bits:<7} | {t_py_ms:<15.2f} | {t_hw_ms:<15.2f} | {cycles:<15} | {4*bits}")

    # GENEROWANIE WYKRESÓW
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Porównanie: Python vs Real Hardware (Skala logarytmiczna)
    ax1.plot(bit_sizes, times_python, 'o-', label='Symulacja (Python)', color='tab:red')
    ax1.plot(bit_sizes, times_hardware, 's--', label='Estymacja FPGA (200MHz)', color='tab:green')
    ax1.set_yscale('log')
    ax1.set_title('Symulacja vs. Realny Sprzęt')
    ax1.set_xlabel('Długość klucza (bity)')
    ax1.set_ylabel('Czas (ms) - skala logarytmiczna')
    ax1.grid(True, which="both", ls="-", alpha=0.5)
    ax1.legend()

    # 2. Liczba cykli zegara (Złożoność kwadratowa)
    ax2.plot(bit_sizes, cycles_list, 'D-', color='tab:blue')
    ax2.set_title('Całkowita liczba cykli zegara')
    ax2.set_xlabel('Długość klucza (bity)')
    ax2.set_ylabel('Liczba cykli')
    ax2.grid(True)

    # 3. Koszt sprzętowy (Złożoność liniowa)
    ax3.plot(bit_sizes, ff_costs, 's-', color='tab:orange')
    ax3.set_title('Zasoby sprzętowe (Rejestry FF)')
    ax3.set_xlabel('Długość klucza (bity)')
    ax3.set_ylabel('Liczba przerzutników (FF)')
    ax3.grid(True)

    plt.tight_layout()
    plt.savefig('analiza_sprzetowa.png')
    print("\n[SUKCES] Wygenerowano wykresy: 'analiza_sprzetowa.png'")
    plt.show()

if __name__ == "__main__":
    run_benchmark()