from flask import Flask, request, render_template
from gdax import gdax_web_service

app = Flask(__name__)


@app.route('/', methods=['POST'])
def test():
    return gdax_web_service(request.get_json())


@app.route('/', methods=['GET', 'POST'])  # The app accepts methods GET and POST
def index():  # This function is executed for '/' i.e root directory
    if request.method == 'POST':  # POST method is used to pass variables from HTML forms
        action = request.form['action']
        bc = request.form['bc']
        qc = request.form['qc']
        amount = request.form['amount']
        input_object = {"action": action, "base_currency": bc, "quote_currency": qc, "amount": amount}
        # Variables are used to create input_object
        return str(input_object)
    else:
        return (render_template('index.html'))  # This page is returned for regular GET methods


if __name__ == "__main__":
    app.run(debug=True)
