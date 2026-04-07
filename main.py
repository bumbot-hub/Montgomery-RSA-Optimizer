from src.rsa_simulator import RSASimulator
from sympy import mod_inverse
import math

def main():
    # Generowanie  parametrów RSA
    p = 1000003
    q = 1000033
    N = p * q
    phi = (p - 1) * (q - 1)

    E = 65537
    if math.gcd(E, phi) != 1:
        print("E i phi(N) nie są względnie pierwsze!")
        return

    D = mod_inverse(E, phi)

    print(f"N: {N}")
    print(f"E: {E}")
    print(f"D: {D}")
    print(f"Moduł ma {N.bit_length()} bitów\n")

    rsa = RSASimulator(N, E, D)
    text = "Hello"
    M = rsa.text_to_int(text)

    print(f"Tekst: '{text}'")
    print(f"M: {M}")

    if M >= N:
        print("Tekst zbyt długi dla podanego N!")
        return

    c = rsa.encrypt(M)
    print(f"Szyfogram: {c}")

    M_dec = rsa.decrypt(c)
    print(f"Odszyfrowana liczba: {M_dec}")

    if M == M_dec:
        decoded = rsa.int_to_text(M_dec)
        print(f"Sukces: '{decoded}'")
    else:
        print("Błąd RSA!")


if __name__ == "__main__":
    main()