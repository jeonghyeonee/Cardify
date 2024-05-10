from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 전역 변수를 초기화합니다.
card_info = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    global card_info
    card_info = {
        "card_number_1": request.form['card_number_1'],
        "card_number_2": request.form['card_number_2'],
        "card_number_3": request.form['card_number_3'],
        "card_number_4": request.form['card_number_4'],
        "expiry_month": request.form['expiry_month'],
        "expiry_year": request.form['expiry_year']
    }
    print("카드 정보를 성공적으로 받았습니다.")
    return '카드 정보를 성공적으로 받았습니다.'

@app.route('/card-info', methods=['GET'])
def get_card_info():
    global card_info
    return jsonify(card_info)

if __name__ == '__main__':
    app.run(debug=True)
