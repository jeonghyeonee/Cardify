from heaan_utils import Heaan
from card_preprocessing import preprocess_card_number, preprocess_expiry_date, triple_preprocess_card_number
from datetime import datetime

he = Heaan()

def validate_card_num(ctxt):
    # Double the value of digits at odd positions
    double_odd_ctxt = he.multiply(ctxt, 2)

    # If doubling results in a two-digit number, sum the digits
    cnt, remain = he.division(double_odd_ctxt, 10)

    addition_remain_cnt = he.addition(cnt, remain)
    addition_remain_cnt_msg = he.decrypt(addition_remain_cnt)

    total = he.feat_msg_generate([0])
    total_ctxt = he.encrypt(total)

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

    # Check if the total sum is dicided in 10
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
        msg = 0  # visa
    elif round(result_master_msg[0].real, 2) == 1:
        msg = 1  # master
    elif round(result_domestic_msg[0].real, 2) == 1:
        msg = 3  # domestic
    else:
        msg = 4  # NOT valid
    
    return msg

def check_card_brand_method2(ctxt):
    bin = [4] + [0]*(15) + [5] + [0]*(15) + [9]
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
        msg = 0  # visa
    elif round(result_master_msg[0].real, 2) == 1:
        msg = 1  # master
    elif round(result_domestic_msg[0].real, 2) == 1:
        msg = 3  # domestic
    else:
        msg = 4  # NOT valid

    return msg

def check_card_brand_method3(ctxt):
    # Create all bin keys
    bin = [4] + [0]*(15) + [5] + [0]*(15) + [9]
    bin_msg = he.feat_msg_generate(bin)
    bin_ctxt = he.encrypt(bin_msg)

    # Subtract bin - card_num
    result = he.subtract(bin_ctxt, ctxt)
    
    # Check equality to zero for the entire result
    result = he.equal_zero(result)

    # Check Visa
    result_visa_msg = he.decrypt(result)
    
    if round(result_visa_msg[0].real, 2) == 1:
        msg = 0  # visa
    else:
        # Check Master
        result_master = he.left_rotate(result, 16)
        result_master_msg = he.decrypt(result_master)

        if round(result_master_msg[0].real, 2) == 1:
            msg = 1  # master
        
        else:
            # Check Domestic
            result_domestic = he.left_rotate(result_master, 16)
            result_domestic_msg = he.decrypt(result_domestic)

            if round(result_domestic_msg[0].real, 2) == 1:
                msg = 3  # domestic
            else:
                msg = 4  # NOT valid

    return msg

def check_expiry_date(ctxt):
    date = [int(datetime.today().strftime("%y%m"))]
    date_msg = he.feat_msg_generate(date)
    date_ctxt = he.encrypt(date)

    result_date = he.subtract(ctxt, date_ctxt)
    result_date_msg = he.decrypt(result_date)

    # Set msg value: valid = 1, not valid = 0
    if round(result_date_msg[0].real, 2) >= 0:
        msg = 1  # valid
    else:
        msg = 0  # NOT valid

    return msg