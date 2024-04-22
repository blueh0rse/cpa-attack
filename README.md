# Correlation Power Analysis Attack

## Hardware Security Project

### Master of Cybersecurity

The goal of the project is to implement a correlation power analysis (CPA) attack to the 128-bit AES encryption algorithm and retrieve the 16 bytes of the key.

The students will be provided with a set of power consumption traces acquired when a microcontroller (PIC18F4520) is running the AES encryption algorithm over several plaintexts. The current is probed via the voltage drop across a series connected resistor as indicated in Figure 1.

![Figure 1: Diagram of the experimental setup to acquire the power consumption traces](assets/image.png)

_Figure 1: Diagram of the experimental setup to acquire the power consumption traces_

## Instructions

1. Clone the repository

```bash
git clone https://github.com/blueh0rse/cpa-attack
```

2. Create a virtual environment

```bash
python3 -m venv .env
```

3. Activate the virtual environment

```bash
source .env/bin/activate
```

4. Install the dependencies

```bash
pip install -r requirements.txt
```
