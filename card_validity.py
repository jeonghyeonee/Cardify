from heaan_utils import Heaan
from card_preprocessing import preprocess_card_number
he = Heaan()

def validate_card_num(ctxt):
    # 홀수자리에 2배
    double_odd_ctxt = he.multiply(ctxt, 2)

    # 만약 2배 한 값이, 두 자리 수 일 경우, 두 자리 더하기
    cnt, remain = he.division(double_odd_ctxt, 10)

    addition_remain_cnt = he.addition(cnt, remain)
    addition_remain_cnt_msg = he.decrypt(addition_remain_cnt)


    total = he.feat_msg_generate([0])
    total_ctxt = he.encrypt(total)

    for i in range(16):
        if i%2 == 0:
            if round(addition_remain_cnt_msg[i].real, 2) > 0:
                # he.eval.add(total, addition_remain_cnt, total)
                total_ctxt = he.addition(addition_remain_cnt, total_ctxt)
            else:
                total_ctxt = he.addition(double_odd_ctxt, total_ctxt)
                
        else:
            # print("card num: ", ctxt)
            total_ctxt = he.addition(total_ctxt, ctxt)

        addition_remain_cnt = he.left_rotate(addition_remain_cnt, 1)
        double_odd_ctxt = he.left_rotate(double_odd_ctxt, 1)
        ctxt = he.left_rotate(ctxt, 1)

    # 최종 합이 10의 배수인지 확인
    final_cnt, final_remain = he.division(total_ctxt, 10)

    # print(final_remain)

    result = he.equal_zero(final_remain)

    result_msg = he.decrypt(result)

    # print(result)

    if round(result_msg[0].real, 2) == 1:
        msg = "VALID"
    else:
        msg = "NOT VALID"
    
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
        msg = "visa"
    elif round(result_master_msg[0].real, 2) == 1:
        msg = "master"
    elif round(result_domestic_msg[0].real, 2) == 1:
        msg = "domestic"
    else:
        msg = "NOT valid"
    
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

    return "Invalid card number"

def check_card_brand_method3(ctxt):
    return msg

def check_expiry_date(ctxt):
    
    
    return msg