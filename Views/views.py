from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from Morbidity.Controller.SMP import get_smp
from Morbidity.Controller.rg_info import get_tu_info
from Morbidity.Controller.nod_info import get_nz_info

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/SimonyanAR.FCGIE/Desktop/Project/Morbidity/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

tu = get_tu_info()
nz = get_nz_info()


@app.route('/')
def home():
    return render_template(f'index.html', title='Главная')


@app.route('/smp', methods=['GET', 'POST'])
def smp():
    if request.method == 'POST':

        date_first = int(request.form['date_first'])
        date_last = int(request.form['date_last'])
        nz_input = int(request.form['nz_input'])
        # rg_id = int(request.form['rg_id'])
        rg_id = int(request.form['rg_id'])
        a = int(request.form['nz_id'])

        print(f'{date_first} {date_last} {nz_input} {rg_id} {a}')

        value = get_smp(date_first, date_last, nz_input, rg_id)
        return render_template('smp.html', value_smp=value, regions=tu, nod=nz)
    else:
        return render_template('smp.html')


if __name__ == '__main__':
    app.run(debug=True)
