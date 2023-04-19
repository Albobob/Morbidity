from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from Morbidity.Controller.SMP import get_smp
from Morbidity.Controller.rg_info import get_tu_info
from Morbidity.Controller.nod_info import get_nz_info
from Morbidity.Controller.up_down_table import get_up_down

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

        value = round(get_smp(date_first, date_last, nz_id, rg_id), 4)
        return render_template('smp.html', value_smp=value, regions=tu, nod=nz)
    else:
        return render_template('smp.html', regions=tu, nod=nz)


@app.route('/up_down', methods=['GET', 'POST'])
def up_down():
    tu = get_tu_info()
    nz = get_nz_info()
    if request.method == 'POST':
        date_first = int(request.form['date_first'])
        date_last = int(request.form['date_last'])
        nz_id = int(request.form['nz_id'])
        rg_id_1 = int(request.form['tu_id_1'])
        rg_id_2 = int(request.form['tu_id_2'])
        rg_id_3 = int(request.form['tu_id_3'])
        # TODO: Сделать сохранение всех выгружаемых файлов в папку
        # TODO: Сделать проверку на существование файла

        print(f'{date_first} {date_last} {nz_id} {rg_id_1} {rg_id_2} {rg_id_3}')

        file_path = get_up_down(date_first, date_last, nz_id, rg_id_1, rg_id_2, rg_id_3)

        return send_file(file_path, as_attachment=True)
    else:
        return render_template(f'up_down.html', title='Таблица рос/снижение', regions=tu, nod=nz)


if __name__ == '__main__':
    app.run(debug=True)
