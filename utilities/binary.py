
def snoob(x):
    """
    Returns the next integer slightly larger than x with the same number of 1 bits.
    Based on Gosper's Hack (HAKMEM Item 175).
    """
    if x == 0:
        return 0
        
    smallest = x & -x
    ripple = x + smallest
    ones = x ^ ripple
    ones = (ones >> 2) // smallest
    return ripple | ones


def generate_binary_progression(start: int = 4095, limit: int = 4095) -> int:
    """
    Generates a progression of numbers starting from `start` up to `limit`
    maintaining the same number of set bits (popcount).
    """

    current = start
    while current <= limit:
        yield current
        next_val = snoob(current)
        #if next_val == 0: # Should not happen for non-zero start unless overflow behavior
        #     break
        current = next_val


def max_binary(binary_length: int = 8, bits: int = 3) -> int:
    """
    Example:
      max_bin(8, 3)   # 224 (0b11100000)
      max_bin(16, 4)  # 61440 (0b1111000000000000)
    """
    if bits > binary_length:
        raise ValueError(f"Count of 1s '{bits}' cannot exceed the total length '{binary_length}'.")
    
    ones = (1 << bits) - 1
    
    # 00000111 << (8-3) = 11100000
    result = ones << (binary_length - bits)
    
    return result
