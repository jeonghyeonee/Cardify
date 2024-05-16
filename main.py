from heaan_utils import Heaan
import requests
from card_preprocessing import preprocess_card_number, preprocess_expiry_date
from card_validity import validate_card_num

# Flask 애플리케이션의 URL
api_url = 'http://127.0.0.1:5000'

# /card-info 엔드포인트에 GET 요청을 보내어 카드 정보를 가져옴
response = requests.get(f'{api_url}/card-info')

if response.status_code == 200:
    card_info = response.json()
    print("카드 정보:", card_info)

    # 카드 번호 전처리
    card_num_ctxt = preprocess_card_number(card_info)

    # 유효기간 전처리
    valid_thru = preprocess_expiry_date(card_info)

    # print("카드 번호:", card_num_ctxt)
    # print("유효기간:", valid_thru)
    print(validate_card_num(card_num_ctxt))

    # TODO: card_validation, identifier, expiration 함수 생성
    # TODO: main에서 3개 함수를 불러서 실행만 하도록 함.

    


else:
    print('카드 정보를 가져오는 데 실패했습니다:', response.status_code)

