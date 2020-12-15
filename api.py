from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshall_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class StocksModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Stocks(name = {name}, price = {price})"

stocks_put_args = reqparse.RequestParser()
stocks_put_args.add_argument("name", type=str, help="Stock´s name", required=True)
stocks_put_args.add_argument("price", type=int, help="Stocks´s price", required=True)

db.create_all()  

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Integer
}

class Stock(Resource):

    @marshall_with(resource_fields)
    def get(self, stock_id):
        result = StocksModel.query.filter_by(id=stock_id).first()
        return result

#acá usé put porque el flaco no dijo cómo usar post
    @marshall_with(resource_fields)
    def put(self, stock_id):
        args = video_put_args.parse_args()
        stock = StocksModel(id=stock_id, name=args['name'], price=args['price'])
        db.session.add(stock)
        db.session.commit()
        return stock

#y acá no sé cómo crear la otra url jajaja
api.add_resource(Stocks, "/stocks/<int:stock_id>")