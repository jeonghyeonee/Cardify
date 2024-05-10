from heaan_utils import Heaan
import requests

# Flask 애플리케이션의 URL
api_url = 'http://127.0.0.1:5000'

# /card-info 엔드포인트에 GET 요청을 보내어 카드 정보를 가져옴
response = requests.get(f'{api_url}/card-info')

if response.status_code == 200:
    card_info = response.json()
    print("카드 정보:", card_info)
else:
    print('카드 정보를 가져오는 데 실패했습니다:', response.status_code)