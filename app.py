from flask import Flask, render_template, request
from solver import EquationSolver

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    steps = []
    equation = ""
    if request.method == 'POST':
        equation = request.form.get('equation', '')
        if equation:
            solver = EquationSolver(equation)
            steps = solver.solve()

    return render_template('index.html', steps=steps, equation=equation)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')