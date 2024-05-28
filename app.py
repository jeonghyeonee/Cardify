from flask import Flask, render_template, jsonify, request, redirect, url_for
import subprocess
import json

app = Flask(__name__)

# Initialize global variables to store card information and validation result.
card_info = {}
validation_result = None

@app.route('/')
def index():
    """
    Render the main page with the card input form.
    """
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    """
    Handle form submission, process card information, and render the result page.
    """
    global card_info, validation_result

    # Collect card information from the form.
    card_info = {
        "card_number_1": request.form['card_number_1'],
        "card_number_2": request.form['card_number_2'],
        "card_number_3": request.form['card_number_3'],
        "card_number_4": request.form['card_number_4'],
        "expiry_month": request.form['expiry_month'],
        "expiry_year": request.form['expiry_year']
    }
    print("Successfully received card information.")
    
    # Convert card_info to a JSON string.
    card_info_json = json.dumps(card_info)
    
    # Use subprocess to execute main.py with card_info_json and capture the result.
    result = subprocess.check_output(["python", "main.py", card_info_json])
    
    # Parse the result and store it in validation_result.
    validation_result = json.loads(result.decode("utf-8").strip())
    
    print("Validation result: ", validation_result)
    
    # Render the result page without redirection to stay on the current page.
    return render_template('result.html', validation_result=validation_result)

@app.route('/card-info', methods=['GET'])
def get_card_info():
    """
    Return the current card information as JSON.
    """
    global card_info
    return jsonify(card_info)

@app.route('/result')
def result():
    """
    Render the result page with the validation result.
    """
    global validation_result
    return render_template('result.html', validation_result=validation_result)

if __name__ == '__main__':
    app.run(debug=True)