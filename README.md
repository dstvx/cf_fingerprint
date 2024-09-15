# cf_fingerprint

A Python implementation for generating a 32-bit fingerprint of files. This implementation is inspired by a [C++ version](https://github.com/meza/curseforge-fingerprint/blob/main/src/addon/fingerprint.cpp) of the CurseForge fingerprint algorithm and optimized using NumPy for efficient array operations, including memory mapping for handling large files.

## Installation

Clone the repository:

```bash
git clone https://github.com/dstvx/cf_fingerprint.git
cd cf_fingerprint
```

Install the necessary dependencies:

```bash
pip install numpy
```

## Usage

The script provides a function `get_fingerprint` that computes a 32-bit fingerprint for a given file.

### Example:

```python
from pathlib import Path
from cf_fingerprint import get_fingerprint

# File path to be fingerprinted
file_path = Path('path/to/your/file.ext')

# Compute the fingerprint
fingerprint = get_fingerprint(file_path)
print(f'Fingerprint: {fingerprint}')
```

### Arguments:
- `file_path` (Union[str, Path]): The path to the file you want to compute the fingerprint for. Can be provided as a string or a `Path` object.

### Returns:
- `int`: The 32-bit fingerprint of the file. If an error occurs, `None` is returned.

## Acknowledgments
This project was inspired by the [C++ implementation](https://github.com/meza/curseforge-fingerprint/blob/main/src/addon/fingerprint.cpp) created by [meza](https://github.com/meza).