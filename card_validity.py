from heaan_utils import Heaan
from card_preprocessing import preprocess_card_number, preprocess_expiry_date, triple_preprocess_card_number, preprocess_expiry_month
from datetime import datetime
import logging

# Configure logging to output DEBUG level messages
logging.basicConfig(level=logging.DEBUG)

# Create and initialize a Heaan instance
he = Heaan()

def validate_card_num(ctxt):
    """
    Validate the card number using homomorphic encryption.

    Args:
        ctxt: Encrypted card number context.

    Returns:
        int: 1 if valid, 0 if not valid.
    """
    # Double the value of digits at odd positions
    double_odd_ctxt = he.multiply(ctxt, 2)

    # If doubling results in a two-digit number, sum the digits
    cnt, remain = he.division(double_odd_ctxt, 10)

    # Sum the digits of two-digit numbers
    addition_remain_cnt = he.addition(cnt, remain)
    addition_remain_cnt_msg = he.decrypt(addition_remain_cnt)

    total = he.feat_msg_generate([0])
    total_ctxt = he.encrypt(total)

    # Sum all digits
    for i in range(16):
        if i % 2 == 0:
            if round(addition_remain_cnt_msg[i].real, 2) > 0:
                total_ctxt = he.addition(addition_remain_cnt, total_ctxt)
            else:
                total_ctxt = he.addition(double_odd_ctxt, total_ctxt)
        else:
            total_ctxt = he.addition(total_ctxt, ctxt)

        addition_remain_cnt = he.left_rotate(addition_remain_cnt, 1)
        double_odd_ctxt = he.left_rotate(double_odd_ctxt, 1)
        ctxt = he.left_rotate(ctxt, 1)

    # Check if the total sum is divisible by 10
    final_cnt, final_remain = he.division(total_ctxt, 10)
    result = he.equal_zero(final_remain)
    result_msg = he.decrypt(result)

    # Set msg value: valid = 1, not valid = 0
    if round(result_msg[0].real, 2) == 1:
        msg = 1  # VALID
    else:
        msg = 0  # NOT VALID
    
    return msg

def check_card_brand_method1(ctxt):
    """
    Check the card brand using method 1.

    Args:
        ctxt: Encrypted card number context.

    Returns:
        int: Brand code (0 for Visa, 1 for Master, 3 for Domestic, 4 for NOT valid).
    """
    visa_msg = he.feat_msg_generate([4])
    master_msg = he.feat_msg_generate([5])
    domestic_msg = he.feat_msg_generate([9])

    visa_ctxt = he.encrypt(visa_msg)
    master_ctxt = he.encrypt(master_msg)
    domestic_ctxt = he.encrypt(domestic_msg)

    # Check Visa
    result_visa = he.subtract(ctxt, visa_ctxt)
    result_visa = he.equal_zero(result_visa)
    result_visa_msg = he.decrypt(result_visa)

    # Check Master
    result_master = he.subtract(ctxt, master_ctxt)
    result_master = he.equal_zero(result_master)
    result_master_msg = he.decrypt(result_master)

    # Check Domestic
    result_domestic = he.subtract(ctxt, domestic_ctxt)
    result_domestic = he.equal_zero(result_domestic)
    result_domestic_msg = he.decrypt(result_domestic)

    # Result
    if round(result_visa_msg[0].real, 2) == 1:
        msg = 0  # Visa
    elif round(result_master_msg[0].real, 2) == 1:
        msg = 1  # Master
    elif round(result_domestic_msg[0].real, 2) == 1:
        msg = 3  # Domestic
    else:
        msg = 4  # NOT valid
    
    return msg

def check_card_brand_method2(ctxt):
    """
    Check the card brand using method 2.

    Args:
        ctxt: Encrypted card number context.

    Returns:
        int: Brand code (0 for Visa, 1 for Master, 3 for Domestic, 4 for NOT valid).
    """
    bin = [4] + [0]*15 + [5] + [0]*15 + [9]
    bin_msg = he.feat_msg_generate(bin)
    bin_ctxt = he.encrypt(bin_msg)

    # Check Visa
    result_visa = he.subtract(bin_ctxt, ctxt)
    result_visa = he.equal_zero(result_visa)
    result_visa_msg = he.decrypt(result_visa)

    # Check Master
    bin_ctxt = he.left_rotate(bin_ctxt, 16)
    result_master = he.subtract(bin_ctxt, ctxt)
    result_master = he.equal_zero(result_master)
    result_master_msg = he.decrypt(result_master)

    # Check Domestic
    bin_ctxt = he.left_rotate(bin_ctxt, 16)
    result_domestic = he.subtract(bin_ctxt, ctxt)
    result_domestic = he.equal_zero(result_domestic)
    result_domestic_msg = he.decrypt(result_domestic)

    # Result
    if round(result_visa_msg[0].real, 2) == 1:
        msg = 0  # Visa
    elif round(result_master_msg[0].real, 2) == 1:
        msg = 1  # Master
    elif round(result_domestic_msg[0].real, 2) == 1:
        msg = 3  # Domestic
    else:
        msg = 4  # NOT valid

    return msg

def check_card_brand_method3(ctxt):
    """
    Check the card brand using method 3.

    Args:
        ctxt: Encrypted card number context.

    Returns:
        int: Brand code (0 for Visa, 1 for Master, 3 for Domestic, 4 for NOT valid).
    """
    # Create all bin keys
    bin = [4] + [0]*15 + [5] + [0]*15 + [9]
    bin_msg = he.feat_msg_generate(bin)
    bin_ctxt = he.encrypt(bin_msg)

    # Subtract bin - card_num
    result = he.subtract(bin_ctxt, ctxt)
    
    # Check equality to zero for the entire result
    result = he.equal_zero(result)

    # Check Visa
    result_visa_msg = he.decrypt(result)
    
    if round(result_visa_msg[0].real, 2) == 1:
        msg = 0  # Visa
    else:
        # Check Master
        result_master = he.left_rotate(result, 16)
        result_master_msg = he.decrypt(result_master)

        if round(result_master_msg[0].real, 2) == 1:
            msg = 1  # Master
        
        else:
            # Check Domestic
            result_domestic = he.left_rotate(result_master, 16)
            result_domestic_msg = he.decrypt(result_domestic)

            if round(result_domestic_msg[0].real, 2) == 1:
                msg = 3  # Domestic
            else:
                msg = 4  # NOT valid

    return msg

def check_expiry_date(ctxt, month_ctxt):
    """
    Validate the card's expiration date.

    Args:
        ctxt: Encrypted expiration date context.
        month_ctxt: Encrypted expiration month context.

    Returns:
        int: 1 if valid, 0 if not valid.
    """
    date = [int(datetime.today().strftime("%y%m"))]
    date_ctxt = he.encrypt(date)

    # Check the Month: JAN ~ DEC
    # Check: month > 0
    zero_month = he.feat_msg_generate([0])
    zero_month_ctxt = he.encrypt(zero_month)

    result_month = he.comparing(month_ctxt, zero_month_ctxt)
    result_month_msg = he.decrypt(result_month)

    if round(result_month_msg[0].real, 2) <= 0.5:
        msg = 0
        return msg  # NOT