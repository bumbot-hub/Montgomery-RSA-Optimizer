from typing import Tuple

class MontgomeryDomain:
    def __init__(self, N: int):
        self.N = N
        self.k = N.bit_length()
        self.R = 1 << self.k    # Używamy przesunięcia bitowego zamiast obliczania R logarytmem który zwraca float
        self.R2 = (self.R**2) % self.N

        # Wyliczenie stałych
        self.r_inv, self.n_prime = self._extended_gdc(self.R, self.N)

        self.r_inv = self.r_inv % self.N
        self.n_prime = (-self.n_prime) % self.R

    def _extended_gdc(self, a: int, b: int) -> Tuple[int,int]:
        old_r, curr_r = a, b
        old_x, curr_x = 1, 0
        old_y, curr_y = 0, 1

        while curr_r != 0:
            q = old_r // curr_r
            old_r, curr_r = curr_r, old_r - q * curr_r
            old_x, curr_x = curr_x, old_x - q * curr_x
            old_y, curr_y = curr_y, old_y - q * curr_y

        return old_x, old_y

    def redc(self, T: int) -> int:
        m = ((T & (self.R - 1)) * self.n_prime) & (self.R - 1)  #((T mod R) * n_prime) mod R, gdzie 'mod R' to będzie ucięcie do k-bitów
        t = (T + (m * self.N)) >> self.k                        #(T + m * N) / R, gdzie dzielenie to przesunięcie bitowe w prawo o k pozycji

        if t >= self.N:
            return t - self.N
        return t

    def to_domain(self, num: int) -> int:
        return self.redc(num * self.R2)

    def from_domain(self, num: int) -> int:
        return self.redc(num)
