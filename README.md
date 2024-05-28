# Cardify

## Overview

Cardify is a Python web application that provides card number and expiry date validation using encryption technology. The program is built using the PI-HEAAN (Homomorphic Encryption for Arithmetic of Approximate Numbers) library. It allows users to input credit card information through a user-friendly web interface and validates the entered card number and expiry date.

## Installation

### Windows

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jeonghyeonee/Cardify.git
   ```

2. **Setup Virtual Environment:**
   ```bash
   python -m venv your_virtual_environment_name
   your_virtual_environment_name\Scripts\activate
   pip install -r requirements.txt
   ```

### Linux / MacOS

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jeonghyeonee/Cardify.git
   ```

2. **Setup Virtual Environment:**
   ```bash
   python3 -m venv your_virtual_environment_name
   source your_virtual_environment_name/bin/activate
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Web Application:**

   ```bash
   python app.py
   ```

2. **Access the Web Interface:**
   Open your web browser and navigate to [http://localhost:5000](http://localhost:5000)

3. **Input Credit Card Information:**
   Follow the prompts on the web page to input the credit card number and expiry date in the specified format.

4. **View Validation Result:**
   The program will validate the entered card number and expiry date, determine the card brand, and display the validation result on the web page.

## Web Interface

The web interface provides a user-friendly way to input credit card information and view the validation result.

### Input Credit Card Information

Follow the prompts on the web page to input the credit card number and expiry date in the specified format.

Example:

```
Card Number: 1234-5678-9012-3456
Expiry Date: 12/25
```

### Output

The validation result will be displayed on the web page, indicating whether the card number and expiry date are valid.

#### Master

##### Input

![image](https://github.com/jeonghyeonee/Cardify/assets/33801356/33d252e6-e41f-465e-bd1f-882655bb4901)

##### Result

![image](https://github.com/jeonghyeonee/Cardify/assets/33801356/95d85a61-51cf-47d1-8b7f-ece922cca569)

#### Visa

##### Input

![image](https://github.com/jeonghyeonee/Cardify/assets/33801356/4aa45991-1aab-45ee-8308-6f8088adc439)

##### Result

![image](https://github.com/jeonghyeonee/Cardify/assets/33801356/75c7d9ef-bf75-41b2-853c-bc915fd746f9)

#### Invalid

##### Input

![image](https://github.com/jeonghyeonee/Cardify/assets/33801356/fbc93da0-03aa-40bf-bb9a-39fbc289118b)

##### Result

![image](https://github.com/jeonghyeonee/Cardify/assets/33801356/f98f9e58-9140-41da-b958-8ade16a59e16)

### References

[Test Card Numbers](https://support.bluesnap.com/docs/test-credit-card-numbers)
