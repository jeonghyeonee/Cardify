from heaan_utils import Heaan
from card_preprocessing import preprocess_card_number
he = Heaan()

def validate_card_num(ctxt):
    # 홀수자리에 2배
    double_odd_ctxt = he.multiply(ctxt, 2)

    # 만약 2배 한 값이, 두 자리 수 일 경우, 두 자리 더하기
    cnt, remain = he.division(double_odd_ctxt, 10)
    # print("2times", cnt)
    # print("2times rm", remain)
    addition_remain_cnt = he.addition(cnt, remain)
    addition_remain_cnt_msg = he.decrypt(addition_remain_cnt)
    # print("addition r&c", addition_remain_cnt)

    total = he.feat_msg_generate([0])
    total_ctxt = he.encrypt(total)

    for i in range(16):
        if i%2 == 0:
            if round(addition_remain_cnt_msg[i].real, 2) > 0:
                # he.eval.add(total, addition_remain_cnt, total)
                total_ctxt = he.addition(double_odd_ctxt, total_ctxt)
            else:
                total_ctxt = he.addition(double_odd_ctxt, total_ctxt)
                # he.eval.add(total, double_odd_ctxt, total)
                # total_ctxt[0] += double_odd[i]
        else:
            total_ctxt = he.addition(total_ctxt, ctxt)
            # he.eval.add(total, ctxt, total)
        
        # print("total in for: ", total_ctxt)
        # 사용되는 모든 암호문 왼쪽으로 rotation
        # he.eval.left_rotate(addition_remain_cnt, 1, addition_remain_cnt)
        # he.eval.left_rotate(double_odd_ctxt, 1, double_odd_ctxt)
        # he.eval.left_rotate(ctxt, 1, ctxt)

        addition_remain_cnt = he.left_rotate(addition_remain_cnt, 1)
        double_odd_ctxt = he.left_rotate(double_odd_ctxt, 1)
        ctxt = he.left_rotate(ctxt, 1)
    print("-----------------------------------")
    print(total_ctxt)

    # 최종 합이 10의 배수인지 확인
    final_cnt, final_remain = he.division(total_ctxt, 10)

    # print(final_remain)

    result = he.equal_zero(final_remain)

    result_msg = he.decrypt(result)

    if round(result_msg[0].real, 2) == 1:
        msg = "This card num is VALID!!!!"
    else:
        msg = "It is NOT valid."
    
    
    return msg