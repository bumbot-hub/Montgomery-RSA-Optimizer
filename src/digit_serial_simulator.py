from src.montgomery_domain import MontgomeryDomain


class DigitSerialSimulator:
    def __init__(self, domain: MontgomeryDomain):
        self.domain = domain

    def multiply(self, A: int, B: int) -> int:
        T = A * B   # Liczby muszą być już w domenie
        return self.domain.redc(T)

    def power(self, base: int, exp: int) -> int:
        # Wejście do domeny
        base_bar = self.domain.to_domain(base)
        res_bar = self.domain.to_domain(1)

        # Obliczanie po bicie
        for bit in bin(exp)[2:]:
            res_bar = self.multiply(res_bar, res_bar)
            if bit == '1':
                res_bar = self.multiply(res_bar, base_bar)

        return self.domain.from_domain(res_bar)