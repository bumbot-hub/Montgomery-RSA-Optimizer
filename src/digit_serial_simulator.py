from src.montgomery_domain import MontgomeryDomain


class DigitSerialSimulator:
    def __init__(self, domain: MontgomeryDomain):
        self.domain = domain

    def multiply(self, A: int, B: int) -> int:
        T = A * B   # Liczby muszą być już w domenie
        return self.domain.redc(T)

    def power(self, m: int, e: int) -> int:
        """
        Główna operacja RSA: m^e mod N.
        """

        # Wejście do domeny
        m_bar = self.domain.to_domain(m)
        res_bar = self.domain.to_domain(1)

        for bit in bin(e)[2:]:
            res_bar = self.multiply_serial(res_bar, res_bar)
            if bit == '1':
                res_bar = self.multiply_serial(res_bar, m_bar)

        return self.domain.from_domain(res_bar)

    def multiply_serial(self, a_bar: int, b_bar: int) -> int:
        """
        Implementacja mnożenia szeregowego (Digit-Serial Radix-2).
        Symuluje procesor przetwarzający liczbę bit po bicie.
        """

        s = 0   # Akumulator (rejestr)
        n = self.domain.N
        k = self.domain.k

        for i in range(k):
            a_i = (a_bar >> i) & 1  # Pobieranie i-tego bitu mnożnika

            if a_i:
                s += b_bar

            # Redukcja Montgomery'ego w każdym kroku (REDC bitowe)
            # Sprawdzamy LSB akumulatora - jeśli jest 1, dodajemy N, aby S było parzyste
            if s & 1:
                s += n
            # Przesunięcie o 1 bit w prawo (zastępuje dzielenie przez R)
            s >>= 1

        # Korekta końcowa (Conditional Subtraction)
        if s >= n:
            s -= n

        return s