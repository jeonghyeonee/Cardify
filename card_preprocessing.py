from heaan_utils import Heaan

# Create an instance of the Heaan class.
heaan_instance = Heaan()

# Initialize the Heaan instance.
heaan_instance.initialize()

def preprocess_card_number(card_info):
    """
    Process and encrypt the card number.

    Args:
        card_info (dict): Dictionary containing card information.

    Returns:
        encrypted_card_num: Encrypted card number.
    """
    # Extract card number digits and convert to integers.
    card_number = [int(num) for i in range(1, 5) for num in card_info[f'card_number_{i}']]

    # Generate the feature message for the card number.
    card_num = heaan_instance.feat_msg_generate(card_number)

    # Encrypt the card number.
    card_num_ctxt = heaan_instance.encrypt(card_num)

    return card_num_ctxt

def preprocess_expiry_date(card_info):
    """
    Process and encrypt the card expiration date.

    Args:
        card_info (dict): Dictionary containing card information.

    Returns:
        encrypted_expiry_date: Encrypted expiration date.
    """
    # Extract and process expiration month and year.
    expiry_month = int(card_info['expiry_month'])
    expiry_year = int(card_info['expiry_year'])
    valid_thru = [expiry_year * 100 + expiry_month]

    # Generate the feature message for the expiration date.
    valid_thru = heaan_instance.feat_msg_generate(valid_thru)

    # Encrypt the expiration date.
    valid_thru_ctxt = heaan_instance.encrypt(valid_thru)

    return valid_thru_ctxt

def preprocess_expiry_month(card_info):
    """
    Process, encrypt, and scale the card expiration month.

    Args:
        card_info (dict): Dictionary containing card information.

    Returns:
        encrypted_expiry_month: Encrypted and scaled expiration month.
    """
    # Extract and convert the expiration month to an integer.
    expiry_month = int(card_info['expiry_month'])

    # Generate the feature message for the expiration month.
    month_msg = heaan_instance.feat_msg_generate([expiry_month])

    # Encrypt the expiration month.
    month_ctxt = heaan_instance.encrypt(month_msg)

    # Scale the encrypted expiration month.
    month_ctxt = heaan_instance.multiply(month_ctxt, 0.01)

    return month_ctxt

def triple_preprocess_card_number(card_info):
    """
    Triple the card number digits, process, and encrypt them.

    Args:
        card_info (dict): Dictionary containing card information.

    Returns:
        encrypted_triple_card_num: Encrypted tripled card number.
    """
    # Extract card number digits and convert to integers.
    card_number = [int(num) for i in range(1, 5) for num in card_info[f'card_number_{i}']]

    # Triple the card number digits.
    triple_card_num = card_number * 3

    # Generate the feature message for the tripled card number.
    card_num = heaan_instance.feat_msg_generate(triple_card_num)

    # Encrypt the tripled card number.
    card_num_ctxt = heaan_instance.encrypt(card_num)

    return card_num_ctxt
