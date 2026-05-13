from src.rsa_simulator import RSASimulator
from sympy import mod_inverse
import math

def run_diagnostics(rsa):
    print("\n[DIAGNOSTYKA] Uruchamianie testów przypadków brzegowych...")
    
    # Testing "weird" numbers: zero, one and max possible message (N-1)
    test_cases = [
        ("Wiadomość M = 0", 0),
        ("Wiadomość M = 1", 1),
        ("Wiadomość M = N-1 (Maksymalna)", rsa.n - 1)
    ]
    
    for name, val in test_cases:
        try:
            enc = rsa.encrypt(val)
            dec = rsa.decrypt(enc)
            status = "SUKCES" if dec == val else "BŁĄD WYNIKU"
            print(f" > {name:<35} -> {status}")
        except Exception as e:
            print(f" > {name:<35} -> BŁĄD KRYTYCZNY ({e})")
    print("-" * 55)

def main():
    # Generating the RSA parameters
    p = 1000003     # First prime number
    q = 1000033     # Second prime number
    N = p * q       # N is the multiplication of prime numbers
    phi = (p - 1) * (q - 1)

    E = 65537       # Number 'E' co-prime with phi (1 <= E <= phi)

    # Checking if E and phi are Co-prime
    if math.gcd(E, phi) != 1:
        print("E i phi(N) nie są względnie pierwsze!")
        return

    D = mod_inverse(E, phi)

    print(f"N: {N}")
    print(f"E: {E}")
    print(f"D: {D}")
    print(f"Moduł ma {N.bit_length()} bitów\n")

    rsa = RSASimulator(N, E, D)
    rsa.multiplier.estimate_hardware_cost(N.bit_length())
    run_diagnostics(rsa)
    text = "Hello"

    M = rsa.text_to_int(text)

    print(f"Przykładowy tekst: '{text}' \n")
    print(f"M (tekst jako liczba): {M}")

    # Cyphering the text in bit form
    c = rsa.encrypt(M)
    print(f"Szyfrogram (zaszyfrowane M): {c}\n")

    # Deciphering the text in a bit form
    M_dec = rsa.decrypt(c)
    print(f"Odszyfrowana liczba: {M_dec}")

    # Checking if deciphered text is equal to text before cyphering 
    if M == M_dec:
        # Changing back the number into text
        decoded = rsa.int_to_text(M_dec)
        print(f"Sukces (zdekodowany tekst): '{decoded}'")
    else:
        print("Błąd RSA!")


if __name__ == "__main__":
    main()