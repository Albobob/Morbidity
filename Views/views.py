from flask import Flask, render_template, request, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from Morbidity.Controller.SMP import get_smp
from Morbidity.Controller.rg_info import get_tu_info
from Morbidity.Controller.nod_info import get_nz_info
from Morbidity.Controller.up_down_table import get_up_down
from Morbidity.Controller.form_2_info import get_fprm_2_info
from Morbidity.config import SQL_PATH

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'{SQL_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template(f'index.html', title='Главная')


@app.route('/tst', methods=['GET', 'POST'])
def tst():
    nz = get_nz_info()
    if request.method == 'POST':
        nz_id = int(request.form['nz_id'])
        form_2 = get_fprm_2_info('2009-12-20 00:00:00', nz_id, 1)
        return render_template(f'tst.html', title='Главная', nod=nz, form_2=form_2)
    else:
        return render_template(f'tst.html', title='Главная', nod=nz)



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
        # TODO: Сделать сохранение всех выгружаемых файлов в одну папку
        # TODO: Сделать проверку на существование файла

        print(f'{date_first} {date_last} {nz_id} {rg_id_1} {rg_id_2} {rg_id_3}')

        file_path = get_up_down(date_first, date_last, nz_id, rg_id_1, rg_id_2, rg_id_3)

        return send_file(file_path, as_attachment=True)
    else:
        return render_template(f'up_down.html', title='Таблица рост/снижение', regions=tu, nod=nz)


@app.route('/regions')
def regions():
    region = get_tu_info()
    print(region)
    rg_value = 2.1234
    return render_template(f'regions.html', title='Регионы', regions=region, rg_value=rg_value)
    pass


if __name__ == '__main__':
    app.run(debug=True)
