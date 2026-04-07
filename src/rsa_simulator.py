from src.digit_serial_simulator import DigitSerialSimulator
from src.montgomery_domain import MontgomeryDomain


class RSASimulator:
    def __init__(self, n: int, e: int, d: int):
        self.domain = MontgomeryDomain(n)
        self.multiplier = DigitSerialSimulator(self.domain)

        self.e = e
        self.d = d
        self.n = n

    def encrypt(self, message_int: int):
        """Szyfrowanie: C = M^e mod N przy użyciu Montgomery'ego"""
        return self.multiplier.power(message_int, self.e)

    def decrypt(self, ciphertext_int: int):
        """Deszyfrowanie: M = C^d mod N przy użyciu Montgomery'ego"""
        return self.multiplier.power(ciphertext_int, self.d)

    def text_to_int(self, text: str) -> int:
        # Zamiana stringa na bajty, a potem na jedną wielką liczbę
        return int.from_bytes(text.encode('utf-8'), byteorder='big')

    def int_to_text(self, number: int) -> str:
        # Zamiana wielkiej liczby z powrotem na tekst
        byte_count = (number.bit_length() + 7) // 8
        return number.to_bytes(byte_count, byteorder='big').decode('utf-8')