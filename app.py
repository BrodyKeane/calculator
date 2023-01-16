from flask import Flask, render_template, url_for, redirect, request
from sympy import sympify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.static_url_path = '/static'
app.static_folder = 'static'

symbols =['(', ')','x^Y','CLR',
          '7', '8', '9', '÷',
          '6', '5', '4',  '*',
          '3', '2', '1',  '-',
          '.', '0', '=',  '+']

@app.get('/')
def redirect_from_root():
    return redirect(url_for('render_calculator', equation='0'))

@app.get('/<string:equation>')
def render_calculator(equation = '0'):
    return render_template('calculator.html', equation=equation, symbols=symbols)

@app.post('/')
def append_symbol():
    equation = request.form.get('equation', '0')
    symbol = request.form.get('symbol', '0')
    equation = update_equation(symbol, equation)
    return redirect(url_for('render_calculator', equation=equation))

def update_equation(symbol, equation):
    if symbol == 'CLR':
        equation = '0'
    elif equation == '0':
        equation = symbol
    elif symbol == '=':
        equation = solve_equation(equation)
    else:
        equation += str(symbol)
    return equation

def solve_equation(equation):
    equation = equation.replace('÷', '/')
    equation = sympify(equation)
    result = equation.evalf()
    result = remove_trailing_zeros(result)
    return result

def remove_trailing_zeros(result):
    result = str(result)
    for num in range(len(result)-1, -1, -1):
        if result[num] == '0':
            result = result[:-1]
        else:
            break
    return result






if __name__ == '__main__':
    app.run(debug=True)