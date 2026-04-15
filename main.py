from src.rsa_simulator import RSASimulator
from sympy import mod_inverse
import math

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
    text = "Hello"
    M = rsa.text_to_int(text)

    print(f"Przykładowy tekst: '{text}' \n")
    print(f"M (tekst jako liczba): {M}")

    # Checking if text in bits is smaller than N
    if M >= N:
        print("Tekst zbyt długi dla podanego N!")
        return

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