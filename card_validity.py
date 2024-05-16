from heaan_utils import Heaan

def validate_card_info(card_info):
    """
    카드 정보의 유효성을 검증합니다.
    
    Args:
        card_info (dict): 카드 정보 딕셔너리
    
    Returns:
        bool: 카드 정보의 유효성 여부
    """
    heaan_instance = Heaan()
    
    # 카드 번호 유효성 검사
    card_num_valid = heaan_instance.validate_card_number(card_info['card_number'])
    
    # 유효기간 유효성 검사
    expiry_date_valid = heaan_instance.validate_expiry_date(card_info['expiry_date'])
    
    return card_num_valid and expiry_date_valid

def main():
    # 카드 정보 딕셔너리
    card_info = {
        'card_number_1': '1234',
        'card_number_2': '1234',
        'card_number_3': '5678',
        'card_number_4': '5678',
        'expiry_month': '01',
        'expiry_year': '28'
    }
    
    # 카드 정보 유효성 검사
    if validate_card_info(card_info):
        print("카드 정보가 유효합니다.")
    else:
        print("유효하지 않은 카드 정보입니다.")

if __name__ == "__main__":
    main()
