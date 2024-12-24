def get_set_bits_positions(n):
    positions = []
    position = 1
    while n > 0:
        if n & 1:
            positions.append(position)
        n >>= 1
        position += 1
    return positions
