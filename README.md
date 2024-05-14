# Correlation Power Analysis Attack

## Hardware Security Project

### Master of Cybersecurity

The goal of the project is to implement a correlation power analysis (CPA) attack to the 128-bit AES encryption algorithm and retrieve the 16 bytes of the key.

The students will be provided with a set of power consumption traces acquired when a microcontroller (PIC18F4520) is running the AES encryption algorithm over several plaintexts. The current is probed via the voltage drop across a series connected resistor as indicated in Figure 1.

![Figure 1: Diagram of the experimental setup to acquire the power consumption traces](assets/image.png)

_Figure 1: Diagram of the experimental setup to acquire the power consumption traces_

## Overview

```
├── LICENSE
├── README.md
├── assets
│   └── image.png
├── attack1.ipynb
├── data
│   └── dataset1
│       ├── cleartext.txt
│       ├── trace0.txt
│       ├── trace1.txt
│       ├── trace2.txt
│       ├── trace3.txt
│       ├── trace4.txt
│       ├── trace5.txt
│       ├── trace6.txt
│       ├── trace7.txt
│       ├── trace8.txt
│       ├── trace9.txt
│       ├── trace10.txt
│       ├── trace11.txt
│       ├── trace12.txt
│       ├── trace13.txt
│       ├── trace14.txt
│       └── trace15.txt
└── requirements.txt
```

## Instructions

1. Clone the repository

```bash
git clone https://github.com/blueh0rse/cpa-attack
```

2. Create a virtual environment

```bash
python3 -m venv .venv
```

3. Activate the virtual environment

```bash
source .venv/bin/activate
```

4. Install the dependencies

```bash
(.venv)$ pip install -r requirements.txt
```

5. Select a python kernel for the notebook

Example: `.venv (Python 3.10.12)`

6. You can now run the following files:

- `attack1.ipynb`: to see how we solved dataset1
- `attack2.ipynb`: to see how we solved dataset2
- `script_multi.py`: to run our fastest, most optimized code

Output example for dataset 1:

```bash
(.venv)$ python3 script_multi.py 1
Selected dataset: 1
Loading cleartexts...
Loading traces...
Computing Weights...
Started working on box 0
Started working on box 1
...
finished box 4
finished box 2
Key bytes: [65, 117, 115, 116, 114, 97, 108, 111, 112, 105, 116, 104, 101, 99, 117, 115]
Key checksum: 1712
Attack was successful :)
Attack performed in: 00:00:48
```

Output example for dataset 2:

```bash
(.venv)$ python3 script_multi.py 2
Selected dataset: 2
Loading cleartexts...
Loading traces...
Loading clocks...
Computing Weights...
Working on flanks...
Started working on box 0
Started working on box 1
...
finished box 7
finished box 13
Key bytes: [84, 104, 97, 116, 115, 32, 109, 121, 32, 75, 117, 110, 103, 32, 70, 117]
Key checksum: 1434
Attack was successful :)
Attack performed in: 00:00:27
```

## Steps

### 1. Process the traces

- We first initialized a 3D NumPy array to hold all the traces from `data/dataset1`.
  - Dimensions: 16 key bytes x 150 traces x 50000 samples
- Then a second 2D NumPy array to hold the plaintexts of `data/dataset1/cleartext.txt`.
  - Dimensions: 150 plaintexts x 16 bytes

### 2. Generate hypotheses

- For simplicity and transparency reasons we initialized a fixed array containing the AES substitution box values
- Created an array of all possible byte values (0 to 255) for key guessing
- Added an extra dimension to the plaintext array to prepare it for element-wise operations with the key guesses
  - This was needed for performance reason as loops in python can be very slow when dealing with very large amount of data
- Adjusts the shape of the key guesses array to facilitate broadcasting with the expanded plaintext array.
- Performs a bitwise XOR between every plaintext byte and each key guess, simulating the first step of the AES encryption (AddRoundKey).
- Uses the XOR results as indices to retrieve values from the S-box, converting the output into 8-bit unsigned integers for bit manipulation.
- Converts the S-box output to uint8, unpacks each byte to bits, and then reshapes and sums these bits to compute the Hamming weights for each byte.
