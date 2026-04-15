from src.montgomery_domain import MontgomeryDomain

# Class that handles the simulation of the digital-series mechanism
class DigitSerialSimulator:
    # Constructor 
    def __init__(self, domain: MontgomeryDomain):
        self.domain = domain    # Creating a Montgomery domain

    # Multiplication to get teh T
    def multiply(self, A: int, B: int) -> int:
        T = A * B   # Numbers must be in a domain
        return self.domain.redc(T)

    # Main operation for RSA: M^e (mod N)
    def power(self, m: int, e: int) -> int:
        # Entering the domain
        m_bar = self.domain.to_domain(m)
        res_bar = self.domain.to_domain(1)

        for bit in bin(e)[2:]:      # Getting the exponent as binary number and going through it
            res_bar = self.multiply_serial(res_bar, res_bar)    # Multiplying the result by itself
            if bit == '1':
                res_bar = self.multiply_serial(res_bar, m_bar)  # If our number is 1 we multiply by 'm'

        return self.domain.from_domain(res_bar)

    # Implementation of Digit-Serial multiplication. Simulating the procesor processing bit by bit
    def multiply_serial(self, a_bar: int, b_bar: int) -> int:
        s = 0               # accumulator (register)
        n = self.domain.N
        k = self.domain.k

        for i in range(k):
            a_i = (a_bar >> i) & 1  # Getting the i-th bit of multiplayer

            if a_i:
                s += b_bar

            # Montgomery's reduction in every step (bit REDC)
            # Checking LSB of accumulator - if its 1, add N, to make S even
            if s & 1:
                s += n
            # shift 1 bit right (To not use division by R)
            s >>= 1

        # Final correction (Conditional Subtraction)
        if s >= n:
            s -= n

        return s