from heaan_utils import Heaan
import requests
from card_preprocessing import preprocess_card_number, preprocess_expiry_date,triple_preprocess_card_number
from card_validity import validate_card_num, check_card_brand_method1, check_card_brand_method2, check_card_brand_method3, check_expiry_date

# Flask 애플리케이션의 URL
api_url = 'http://127.0.0.1:5000'

# /card-info 엔드포인트에 GET 요청을 보내어 카드 정보를 가져옴
response = requests.get(f'{api_url}/card-info')

if response.status_code == 200:
    card_info = response.json()
    print("카드 정보:", card_info)

    # 카드 번호 전처리
    card_num_ctxt = preprocess_card_number(card_info)

    # Triple Card num preprocessing
    triple_card_num_ctxt = triple_preprocess_card_number(card_info)

    # 유효기간 전처리
    valid_thru_ctxt = preprocess_expiry_date(card_info)

    card_result = {}
    
    # Store the results in the dictionary
    card_result['card_validity'] = validate_card_num(card_num_ctxt)
    # card_result['card_brand_method1'] = check_card_brand_method1(card_num_ctxt)
    # card_result['card_brand_method2'] = check_card_brand_method2(card_num_ctxt)
    card_result['card_brand'] = check_card_brand_method3(card_num_ctxt)
    card_result['expiry_date_validity'] = check_expiry_date(valid_thru_ctxt)

    print(card_result)
    

else:
    print('카드 정보를 가져오는 데 실패했습니다:', response.status_code)

