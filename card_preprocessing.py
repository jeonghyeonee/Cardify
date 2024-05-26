from heaan_utils import Heaan

# Heaan 클래스의 인스턴스 생성
heaan_instance = Heaan()

# Heaan 클래스의 메서드 호출
heaan_instance.initialize()


def preprocess_card_number(card_info):
    card_number = [int(num) for i in range(1, 5) for num in card_info[f'card_number_{i}']]

    card_num = heaan_instance.feat_msg_generate(card_number)

    card_num_ctxt = heaan_instance.encrypt(card_num)

    return card_num_ctxt

def preprocess_expiry_date(card_info):
    expiry_month = int(card_info['expiry_month'])
    expiry_year = int(card_info['expiry_year'])
    valid_thru = [expiry_year * 100 + expiry_month]

    valid_thru = heaan_instance.feat_msg_generate(valid_thru)

    valid_thru_ctxt = heaan_instance.encrypt(valid_thru)

    return valid_thru_ctxt

def preprocess_expiry_month(card_info):
    expiry_month = int(card_info['expiry_month'])

    month_msg = heaan_instance.feat_msg_generate([expiry_month])

    month_ctxt = heaan_instance.encrypt(month_msg)

    month_ctxt = heaan_instance.multiply(month_ctxt, 0.01)

    return month_ctxt

def triple_preprocess_card_number(card_info):
    card_number = [int(num) for i in range(1, 5) for num in card_info[f'card_number_{i}']]

    triple_card_num = card_number * 3

    card_num = heaan_instance.feat_msg_generate(triple_card_num)

    card_num_ctxt = heaan_instance.encrypt(card_num)

    return card_num_ctxt
