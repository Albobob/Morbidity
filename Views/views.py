from flask import Flask, render_template, request, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from Morbidity.Controller.SMP import get_smp, compare_value
from Morbidity.Controller.rg_info import get_tu_info
from Morbidity.Controller.nod_info import get_nz_info
from Morbidity.Controller.up_down_table import get_up_down
from Morbidity.Controller.form_2_info import get_fprm_2_info, get_min_max_year, get_top_5_regions, get_down_5_regions
from Morbidity.Controller.ticks_info import contacted_sum_total, get_min_max_year_week, get_rg_ids, get_average_value, \
    get_min_max_value

()
from Morbidity.config import SQL_PATH
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'{SQL_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template(f'index.html', title='Главная')


@app.route('/ticks', methods=['GET', 'POST'])
def ticks():
    min_max = get_min_max_year_week()
    current_week = datetime.date.today().isocalendar()[1]
    date_now = datetime.datetime.now().strftime("%d.%m.%Y")
    current_year = datetime.datetime.now().year

    if request.method == 'POST':
        week = int(request.form['input_week'])
        year = int(request.form['input_year'])
        current_week = week
        current_year = year
        previous_year = year - 1
        contacted_date = contacted_sum_total(year, week, 1)['current_date']
        contacted_current = contacted_sum_total(year, week, 1)['current_value']
        contacted_current_chl = contacted_sum_total(year, week, 6)['current_value']  # Дети
        contacted_previous = contacted_sum_total(year, week, 1)['previous_value']

        current_rg_ids = get_rg_ids(year, week)['current_rg_ids']
        previous_rg_ids = get_rg_ids(year, week)['previous_rg_ids']
        average_value = get_average_value(min_max[0], year, week)
        min_value = get_min_max_value(min_max[0], year, week)['min']
        max_value = get_min_max_value(min_max[0], year, week)['max']
        txt_1 = f'По данным оперативного еженедельного мониторинга на {contacted_date} в {current_rg_ids} субъектах ' \
                f'Российской Федерации\n в медицинские организации обратились {contacted_current} пострадавших от укусов ' \
                f' клещей (в {previous_year} г. в {previous_rg_ids} субъекте, {contacted_previous} человека), ' \
                f'в том числе {contacted_current_chl} детей.'
        txt_2 = f'Обращаемость пострадавших от укусов клещей в сравнении с  среднемноголетним значением ' \
                f'(СМП – {average_value}) {compare_value(contacted_current, average_value)}. ' \
                f'Ежегодно в аналогичный период обращались в медицинские организации от {min_value} до {max_value} ' \
                f'пострадавших от укусов клещей. За {week} неделю обратились в медицинские организации' \
                f' {43724} пострадавших от укусов клещей.'

        # week_number = current_date.isocalendar()[1]

        return render_template(f'ticks.html',
                               title='Клещи',
                               current_week=current_week,
                               current_year=current_year,
                               previous_year=previous_year,
                               date_now=date_now,
                               min_year=min_max[0],
                               max_year=min_max[1],
                               min_week=min_max[2],
                               max_week=min_max[3],
                               txt_1=txt_1

                               )
    else:
        return render_template(f'ticks.html',
                               title='Клещи',
                               current_week=current_week,
                               current_year=current_year,
                               date_now=date_now,
                               min_year=min_max[0],
                               max_year=min_max[1],
                               min_week=min_max[2],
                               max_week=min_max[3],
                               )


@app.route('/tst', methods=['GET', 'POST'])
def tst():
    current_year = datetime.datetime.now().year
    min_year = get_min_max_year()[0]
    max_year = get_min_max_year()[1]
    nz = get_nz_info()
    if request.method == 'POST':
        year = request.form['input_year_map']
        current_year = year
        nz_id = int(request.form['nz_id'])
        form_2 = get_fprm_2_info(f'{year}-01-01 00:00:00.000000', nz_id, 1)
        value = []
        name_nz = 'Название нозологии'
        for i in get_nz_info():
            if i[0] == int(nz_id):
                name_nz = i[1]
        rf_mrb = None

        for i in form_2:
            value.append(i['value'])
            if i['rg_id'] == 90:
                rf_mrb = i['value']

        smp_rf = round(get_smp(2010, 2019, nz_id, 90), 2)
        ud = compare_value(rf_mrb, smp_rf)
        top_reg = get_top_5_regions(int(year), nz_id)
        top_reg_list = []
        for i in top_reg:
            value_rg = i[1]
            smp_rg = round(get_smp(2010, 2019, nz_id, i[0]), 2)
            ud_rg = compare_value(value_rg, smp_rg)
            print(f'{value_rg} * {smp_rg} / {ud_rg}')
            top_reg_list.append((i[0], value_rg, smp_rg, ud_rg))

        down_reg = get_down_5_regions(int(year), nz_id)
        tu = get_tu_info()
        max_mrb = max(value)
        color_value = 198

        return render_template(f'tst.html',
                               title='Главная',
                               nod=nz,
                               form_2=form_2,
                               color=color_value,
                               max_mrb=max_mrb,
                               current_year=current_year,
                               min_year=min_year,
                               max_year=max_year,
                               name_nz=name_nz,
                               smp_rf=smp_rf,
                               rf_mrb=rf_mrb,
                               ud=ud,
                               top_reg=top_reg,
                               top_reg_list=top_reg_list,
                               tu=tu,
                               down_reg=down_reg)
    else:
        return render_template(f'tst.html',
                               title='Главная',
                               nod=nz,
                               current_year=current_year,
                               min_year=min_year,
                               max_year=max_year
                               )


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
