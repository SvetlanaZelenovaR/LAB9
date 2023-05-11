import flask
import sqlalchemy.sql
from flask_sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/newdatabaselab9'
db = SQLAlchemy(app)


class Hardware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hardware = db.Column(db.String(512), nullable=False)

    def __init__(self, hardware, prices):
        self.hardware = hardware
        self.prices = [
            Price(text=price) for price in prices.split(',')
        ]


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Float, nullable=False)

    hardware_id = db.Column(db.Integer, db.ForeignKey('hardware.id'), nullable=False)
    hardware = db.relationship('Hardware', backref=db.backref('prices', lazy=True))


@app.route('/', methods=['GET'])
def hello():
    return flask.render_template('index.html', messages=Hardware.query.all())


@app.route('/add_price', methods=['POST'])
def add_price():
    text = flask.request.form['text']
    tag = flask.request.form['price']
    db.session.add(Hardware(text, tag))
    db.session.commit()

    return flask.redirect(flask.url_for('hello'))


@app.route('/clear', methods=['POST'])
def clear():
    db.session.execute(sqlalchemy.sql.text("DELETE FROM price"))
    db.session.commit()

    return flask.redirect(flask.url_for('hello'))


with app.app_context():
    db.create_all()
app.run()
