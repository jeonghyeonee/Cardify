# Cardify

### Card Number and Expiry Date Validation Program

This program is a Python script that validates card numbers and expiry dates using encryption technology. The program is developed using the PI-HEAAN (Homomorphic Encryption for Arithmetic of Approximate Numbers) library.

## Setup Environment

1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/jeonghyeonee/Cardify.git
```

2. Install Python virtual environment

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

### Input Credit Card Information

Follow the prompts to input the credit card number and expiry date in the specified format.

Example:

```
카드 번호를 입력하세요 (형식: xxxx-xxxx-xxxx-xxxx): 1234-5678-9012-3456
카드 유효기간을 mm/yy 형태로 입력하세요: 12/25
```

### Output

The script will validate the input card number and expiry date, encrypt the information, determine the brand of the card, and check if the card is still valid based on the expiry date.

Example Output:

```
입력한 카드 번호: 4234-5678-9012-3456
입력한 유효기간: 12/25
===========================================================================
Method 1
master
Method 2
master
valid
```

## Notes

- This program is developed using the PI-HEAAN library. Installation and setup of the PI-HEAAN library are required.
