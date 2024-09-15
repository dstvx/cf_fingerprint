from numpy import (
    frombuffer,
    uint8,
    uint32,
    seterr,
    memmap
)

from pathlib import (
    Path
)

from typing import (
    Union
)


def get_fingerprint(file_path: Union[str, Path]) -> int:
    '''
    Computes a 32-bit fingerprint for a given file using an optimized algorithm.
    This implementation uses NumPy for efficient array operations and memory mapping for large files.

    Args:
        file_path (Union[str, Path]): Path to the file to be fingerprinted.

    Returns:
        int: The 32-bit fingerprint of the file, or None if an error occurs.
    '''

    MULTIPLEX = uint32(1540483477)
    MASK_32BIT = uint32(4294967295)

    seterr(all='ignore')  # Ignore NumPy warnings for potential overflows

    try:
        buffer = memmap(file_path, dtype=uint8, mode='r')
        buffer = buffer[(buffer != 9) & (buffer != 10) & (buffer != 13) & (buffer != 32)]

        fingerprint = uint32(1) ^ uint32(len(buffer))
        chunk_count = len(buffer) // 4

        if chunk_count > 0:
            chunks = buffer[:chunk_count * 4].view(dtype=uint32)
            
            fingerprint = uint32(fingerprint)
            
            batch_size = 1024
            num_batches = (len(chunks) + batch_size - 1) // batch_size

            for b in range(num_batches):
                start = b * batch_size
                end = min((b + 1) * batch_size, len(chunks))
                batch = chunks[start:end]
                
                temp1 = (batch * MULTIPLEX) & MASK_32BIT
                temp2 = ((temp1 ^ (temp1 >> 24)) * MULTIPLEX) & MASK_32BIT
                
                fingerprint = uint32(fingerprint)
                for t in temp2:
                    fingerprint = ((fingerprint * MULTIPLEX) & MASK_32BIT) ^ t

        # Handle remaining bytes that don't fit into 32-bit chunks
        remaining = buffer[chunk_count * 4:]
        if remaining.size:
            remaining_bytes = uint32(int.from_bytes(remaining.tobytes(), byteorder='little'))
            fingerprint = (fingerprint ^ remaining_bytes) * MULTIPLEX & MASK_32BIT

        fingerprint = ((fingerprint ^ (fingerprint >> 13)) * MULTIPLEX) & MASK_32BIT
        fingerprint = fingerprint ^ (fingerprint >> 15)

        return int(fingerprint)

    except FileNotFoundError:
        print(f'Error: File "{file_path}" not found.')
        return None
    except (TypeError, OSError) as e:
        print(f'Error: Invalid input "{file_path}".')
        print(f'Details: {str(e)}')
        return None