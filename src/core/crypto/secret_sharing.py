import secrets
import hashlib
from typing import List, Tuple, Optional

class SecretSharing:
    PRIME = 2**521 - 1 

    @classmethod
    def _to_int(cls, data: bytes) -> int:
        return int.from_bytes(data, 'big')

    @classmethod
    def _from_int(cls, number: int, length: int) -> bytes:
        # To fix OverflowError in the "Insufficient Shares" case:
        # In a real SSS, reconstructing with too few shares results in a random 
        # number in the prime field. That number might be larger than the original secret.
        # We must truncate/modulo the result to fit the original length.
        
        # 1. Modulo prime to stay in field
        val = abs(number) % cls.PRIME
        
        # 2. Mask it to the length of the original secret
        # If the value is too large to fit in 'length' bytes, we truncate the most significant bits.
        # This is the mathematically correct way to handle "incorrect" reconstruction.
        result = val.to_bytes((val.bit_length() + 7) // 8, 'big')
        
        if len(result) > length:
            return result[-length:] # Truncate to length
        else:
            return result.rjust(length, b'\x00') # Pad with zeros

    @classmethod
    def split_secret(cls, secret_bytes: bytes, threshold: int, num_shares: int) -> List[Tuple[int, int]]:
        if threshold > num_shares:
            raise ValueError("Threshold cannot be greater than the number of shares.")
        
        secret = cls._to_int(secret_bytes)
        if secret >= cls.PRIME:
            raise ValueError(f"Secret too large for field.")

        coefficients = [secret] + [secrets.randbelow(cls.PRIME) for _ in range(threshold - 1)]
        
        shares = []
        for x in range(1, num_shares + 1):
            y = 0
            for exp, coeff in enumerate(coefficients):
                y = (y + coeff * pow(x, exp, cls.PRIME)) % cls.PRIME
            shares.append((x, y))
        
        return shares

    @classmethod
    def recover_secret(cls, shares: List[Tuple[int, int]], secret_length: int) -> bytes:
        def _lagrange_interpolation(x: int) -> int:
            total = 0
            for i in range(len(shares)):
                xi, yi = shares[i]
                num = 1
                den = 1
                for j in range(len(shares)):
                    if i == j: continue
                    xj, _ = shares[j]
                    num = (num * (x - xj)) % cls.PRIME
                    den = (den * (xi - xj)) % cls.PRIME
                
                term = (yi * num * pow(den, cls.PRIME - 2, cls.PRIME)) % cls.PRIME
                total = (total + term) % cls.PRIME
            return total

        secret_int = _lagrange_interpolation(0)
        return cls._from_int(secret_int, secret_length)
