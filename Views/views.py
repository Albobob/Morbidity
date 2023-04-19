from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from Morbidity.Controller.SMP import get_smp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/SimonyanAR.FCGIE/Desktop/Project/Morbidity/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def home():
    date_first = 2010
    date_last = 2019
    nz_input = 29
    rg_id = 5

    value = get_smp(date_first, date_last, nz_input, rg_id)
    return render_template(f'index.html')


if __name__ == '__main__':
    app.run(debug=True)

