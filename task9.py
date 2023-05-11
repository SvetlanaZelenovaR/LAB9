import flask
from flask_sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:456@localhost/mydatabase'
db = SQLAlchemy(app)


class HardwarePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hardware_part = db.Column(db.String(512), nullable=False)

    def __init__(self, hardware_part, prices):
        self.hardware_part = hardware_part
        self.prices = [
            Price(text=price) for price in prices.split(',')
        ]


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Float, nullable=False)

    hardware_part_id = db.Column(db.Integer, db.ForeignKey('hardware_part.id'), nullable=False)
    hardware_part = db.relationship('HardwarePart', backref=db.backref('prices', lazy=True))


@app.route('/', methods=['GET'])
def hello():
    return flask.render_template('index.html', messages=HardwarePart.query.all())


@app.route('/add_price', methods=['POST'])
def add_price():
    text = flask.request.form['hardware_part']
    tag = flask.request.form['price']
    db.session.add(HardwarePart(text, tag))
    db.session.commit()

    return flask.redirect(flask.url_for('hello'))


with app.app_context():
    db.create_all()
app.run()
