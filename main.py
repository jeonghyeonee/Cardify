import sys
import json
from heaan_utils import Heaan
from card_preprocessing import preprocess_card_number, preprocess_expiry_date, triple_preprocess_card_number, preprocess_expiry_month
from card_validity import validate_card_num, check_card_brand_method1, check_card_brand_method2, check_card_brand_method3, check_expiry_date

def main(card_info):
    """
    Main function to process and validate card information.

    Args:
        card_info (dict): Dictionary containing card information.

    Returns:
        card_result (dict): Dictionary containing validation results.
    """
    # Preprocess the card number.
    card_num_ctxt = preprocess_card_number(card_info)

    # Triple the card number digits and preprocess.
    triple_card_num_ctxt = triple_preprocess_card_number(card_info)

    # Preprocess the expiration date.
    valid_thru_ctxt = preprocess_expiry_date(card_info)

    # Preprocess the expiration month.
    valid_month = preprocess_expiry_month(card_info)

    # Dictionary to store the validation results.
    card_result = {}

    # Validate card number and store the result.
    card_result['card_validity'] = validate_card_num(card_num_ctxt)

    # Check card brand using the third method and store the result.
    card_result['card_brand'] = check_card_brand_method3(triple_card_num_ctxt)

    # Check the expiration date validity and store the result.
    card_result['expiry_date_validity'] = check_expiry_date(valid_thru_ctxt, valid_month)

    return card_result

if __name__ == '__main__':
    """
    Entry point of the script. Parses command line input and prints validation results.
    """
    # Parse JSON string passed as a command line argument.
    card_info = json.loads(sys.argv[1])

    # Call main function with the parsed card information.
    result = main(card_info)

    # Print the validation result as a JSON string.
    print(json.dumps(result))
