# Cardify

# Card Number and Expiry Date Validation Program

This program is a Python script that validates card numbers and expiry dates using encryption technology. The program is developed using the HEAAN (Homomorphic Encryption for Arithmetic of Approximate Numbers) library.

## Setup Environment

1. Install Python virtual environment

```bash
python -m venv your_virtual_environment_name
```

Replace `your_virtual_environment_name` with the name you want to use for your virtual environment.

2. Activate the virtual environment

Windows:

```bash
your_virtual_environment_name\Scripts\activate
```

Unix or MacOS:

```bash
source your_virtual_environment_name/bin/activate
```

3. Install required packages

```bash
pip install -r requirements.txt
```

**Note:** If you encounter installation errors with the `pi-heaan` library, it's recommended to use Python version 3.8.x. Please ensure your Python version matches this recommendation before proceeding with the installation.

## How to Run

1. Before running the program, you need to install the HEAAN library. Refer to the official documentation of the HEAAN library for installation instructions.

2. To run the program, execute the following command:

```bash
python validate_card.py
```

3. The program will prompt you to enter the card number and expiry date. It will then validate the entered card number and expiry date, and print the result.

## Notes

- This program is developed using the PI-HEAAN library. Installation and setup of the PI-HEAAN library are required.
