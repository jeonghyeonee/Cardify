import sys
import json
from heaan_utils import Heaan
from card_preprocessing import preprocess_card_number, preprocess_expiry_date, triple_preprocess_card_number
from card_validity import validate_card_num, check_card_brand_method1, check_card_brand_method2, check_card_brand_method3, check_expiry_date

def main(card_info):
    # 카드 번호 전처리
    card_num_ctxt = preprocess_card_number(card_info)

    # Triple Card num preprocessing
    triple_card_num_ctxt = triple_preprocess_card_number(card_info)

    # 유효기간 전처리
    valid_thru_ctxt = preprocess_expiry_date(card_info)

    card_result = {}
    
    # Store the results in the dictionary
    card_result['card_validity'] = validate_card_num(card_num_ctxt)
    card_result['card_brand'] = check_card_brand_method3(triple_card_num_ctxt)
    card_result['expiry_date_validity'] = check_expiry_date(valid_thru_ctxt)

    return card_result

if __name__ == '__main__':
    # 명령줄 인수로 전달된 JSON 문자열을 파싱합니다.
    card_info = json.loads(sys.argv[1])
    result = main(card_info)
    print(json.dumps(result))