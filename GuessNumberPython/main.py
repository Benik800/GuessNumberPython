import numpy as np
from flask import Flask, render_template, url_for, request, session, redirect

app = Flask(__name__)

app.config['SECRET_KEY'] = 'I1WaNt2To3PaSs4Lr5NuMbEr3'
app.config['SESSION_TYPE'] = 'filesystem'

def printMessage(attempts):
    if attempts == 1:
        return "У вас осталась 1 попытка "
    elif attempts == 0:
        return "У вас не осталось попыток"
    elif attempts >= 2 and attempts <= 4:
        return f"У вас осталось {attempts} попытки"
    else:
        return f"У вас осталось {attempts} попыток"

@app.errorhandler(404)
def error404(e):
    return render_template("404.html"), 404

@app.route('/', methods=['POST','GET'])
def index():
    minValue = 1
    maxValue = 100
    if 'guessedNumber' not in session:
        session['guessedNumber'] = np.random.randint(minValue, maxValue + 1)
        session['maxAttempts'] = int(np.ceil(np.log2(maxValue - minValue + 1)))
        session['currentAttempts'] = session['maxAttempts']
        session['prevAttempts'] = ""
        session['message'] = printMessage(session['currentAttempts'])
        session['answer'] = ""
        session['victory'] = 0
    if request.method=='POST':
        data = request.form
        userNumber = int(data['userNumber'])
        if userNumber > maxValue or userNumber < minValue:
            session['victory'] = 0
            session['answer'] = "Выход за границы!"
            session['message'] = printMessage(session['currentAttempts'])
            session['currentAttempts'] = session['currentAttempts']
            return render_template("index.html", min=minValue, max=maxValue, maxAttempts=session['maxAttempts'], currentAttempts=session['currentAttempts'], prevAttempts=session['prevAttempts'], message=session['message'], answer=session['answer'], victory = session['victory'])
        elif userNumber==session['guessedNumber'] and session['currentAttempts'] > 0:
            session['victory'] = 1
            session['currentAttempts'] -= 1
            session['message'] = printMessage(session['currentAttempts'])
            session['answer'] =  f"Поздравляем! Вы победили! Загаданное число было {session['guessedNumber']}"
            session['prevAttempts'] += ("" if session['prevAttempts'] == "" else ", ") + str(userNumber)
            return redirect(url_for('index'))
        elif session['currentAttempts'] == 1:
            session['currentAttempts'] -= 1
            session['victory'] = 0
            session['answer'] = f"Вы проиграли! Игра окончена! Загаданное число было {session['guessedNumber']}"
            session['prevAttempts'] += ("" if session['prevAttempts'] == "" else ", ") + str(userNumber)
            session['message'] = printMessage(session['currentAttempts'])
            return redirect(url_for('index'))
        elif userNumber > session['guessedNumber'] and session['currentAttempts'] > 0:
            session['victory'] = 0
            session['currentAttempts'] -= 1
            session['message'] = printMessage(session['currentAttempts'])
            session['answer'] = f"Загаданное число меньше, чем {userNumber}"
            session['prevAttempts'] += ("" if session['prevAttempts'] == "" else ", ") + str(userNumber)
            return render_template("index.html",min = minValue,max = maxValue,maxAttempts = session['maxAttempts'], currentAttempts= session['currentAttempts'], prevAttempts=session['prevAttempts'], message=session['message'], answer= session['answer'], victory = session['victory'])
        elif userNumber < session['guessedNumber'] and session['currentAttempts'] > 0:
            session['victory'] = 0
            session['currentAttempts'] -= 1
            session['message'] = printMessage(session['currentAttempts'])
            session['answer'] = f"Загаданное число больше, чем {userNumber}"
            session['prevAttempts'] += ("" if session['prevAttempts'] == "" else ", ") + str(userNumber)
            return render_template("index.html", min=minValue, max=maxValue, maxAttempts = session['maxAttempts'], currentAttempts= session['currentAttempts'], prevAttempts=session['prevAttempts'], message=session['message'], answer= session['answer'], victory = session['victory'])
    if request.method == 'GET':
        if 'restart' in request.args:
            session.clear()
            return redirect(url_for('index'))
        return render_template("index.html", min=minValue, max=maxValue, maxAttempts=session['maxAttempts'], currentAttempts=session['currentAttempts'], prevAttempts=session['prevAttempts'],  message=session['message'], answer=session['answer'], victory=session['victory'])

if __name__ == "__main__":
    app.run(debug=True)
