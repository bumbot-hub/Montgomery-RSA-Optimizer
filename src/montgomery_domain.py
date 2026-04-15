from typing import Tuple

# Class that handles the logic of the Montgomery domain
class MontgomeryDomain:
    # The constructor of the class
    def __init__(self, n: int):
        self.N = n                      # The base module
        self.k = self.N.bit_length()    # The power of the domain module (got from the length of 'n' bits)
        self.R = 1 << self.k            # calculating the domain module by using bitwise shift 'n' times
        self.R2 = (self.R**2) % self.N  # Calculating R2 to easier the way to enter the domain

        # Calculation of constants.
        self.r_inv, self.n_prime = self._extended_gdc(self.R, self.N) # Using extended gdc to obtain R^-1 and N'

        self.r_inv = self.r_inv % self.N
        self.n_prime = (-self.n_prime) % self.R

    # The extended GCD* algorithm to obtain R^-1 and N'
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

    # Multiplication and reduction of Montgomery
    def redc(self, T: int) -> int:
        m = ((T & (self.R - 1)) * self.n_prime) & (self.R - 1)  # ((T mod R) * n_prime) (mod R), where 'mod R' will be cut to k-bits
        t = (T + (m * self.N)) >> self.k                        # (T + m * N) / R, where the division is a bitwise shift right 'k' times

        if t >= self.N:
            return t - self.N
        return t

    # Getting into Montgomery domain
    def to_domain(self, num: int) -> int:
        return self.redc(num * self.R2)

    # Getting out of Montgomery domain
    def from_domain(self, num: int) -> int:
        return self.redc(num)
