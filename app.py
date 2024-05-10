from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    card_number_1 = request.form['card_number_1']
    card_number_2 = request.form['card_number_2']
    card_number_3 = request.form['card_number_3']
    card_number_4 = request.form['card_number_4']
    
    expiry_month = request.form['expiry_month']
    expiry_year = request.form['expiry_year']
    
    # 각 카드 번호와 유효기간을 출력하거나 다른 작업을 수행할 수 있음
    print(f'카드 번호: {card_number_1}-{card_number_2}-{card_number_3}-{card_number_4}')
    print(f'유효기간: {expiry_month}/{expiry_year}')
    
    # 여기서 유효성 검사 로직을 추가할 수 있음
    
    return '카드 정보를 성공적으로 받았습니다.'

if __name__ == '__main__':
    app.run(debug=True)
