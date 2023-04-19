from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from Morbidity.Controller.SMP import get_smp
from Morbidity.Controller.rg_info import get_tu_info
from Morbidity.Controller.nod_info import get_nz_info

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/SimonyanAR.FCGIE/Desktop/Project/Morbidity/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template(f'index.html', title='Главная')


@app.route('/smp', methods=['GET', 'POST'])
def smp():
    tu = get_tu_info()
    nz = get_nz_info()
    if request.method == 'POST':
        date_first = int(request.form['date_first'])
        date_last = int(request.form['date_last'])
        rg_id = int(request.form['tu_id'])
        nz_id = int(request.form['nz_id'])

        print(f'{date_first} {date_last} {nz_id} {rg_id}')

        value = get_smp(date_first, date_last, nz_id, rg_id)
        return render_template('smp.html', value_smp=value, regions=tu, nod=nz)
    else:
        return render_template('smp.html', regions=tu, nod=nz)


@app.route('/up_down')
def up_down():
    return render_template(f'up_down.html', title='Главная')

if __name__ == '__main__':
    app.run(debug=True)
