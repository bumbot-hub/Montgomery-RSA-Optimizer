from src.montgomery_domain import MontgomeryDomain

# Hardware-accurate simulator of a Radix-2 Digit-Serial architecture
class DigitSerialSimulator:
    # Constructor 
    def __init__(self, domain: MontgomeryDomain):
        self.domain = domain    # Creating a Montgomery domain

    # Computes the intermediate product T before Montgomery reduction
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
            # Checking LSB of the accumulator; if odd, add modulus N to ensure divisibility by 2
            if s & 1:
                s += n
            # shift 1 bit right (To not use division by R)
            s >>= 1

        # Final correction (Conditional Subtraction)
        if s >= n:
            s -= n

        return s
    
    # Checking how much hardware will be used
    def estimate_hardware_cost(self, key_size: int):
        # In Radix-2 architecture we need registers for A, B, N and accumulator S.
        flip_flops = 4 * key_size 
        
        # Serial multiplication bit by bit requires exactly 'k' clock cycles
        cycles_per_mult = key_size
        
        # Exponentiation Square-and-Multiply requires 1.5 * k multiplications on average
        avg_mults_per_exp = int(1.5 * key_size)
        
        total_cycles = cycles_per_mult * avg_mults_per_exp

        print(f"\n--- Estymacja sprzętowa (klucz {key_size}-bitowy) ---")
        print(f"Architektura: Digit-Serial Radix-2")
        print(f"Wymagane rejestry (Przerzutniki FF): ~{flip_flops}")
        print(f"Cykle zegara na jedno mnożenie REDC: {cycles_per_mult}")
        print(f"Średnia l. cykli na pełne potęgowanie RSA: ~{total_cycles}")
        print("-" * 55)