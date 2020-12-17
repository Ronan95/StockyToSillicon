from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import os, connexion


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

ma = Marshmallow(app)


class StocksModel(db.Model):
    __tablename__ = "stocky"
    stocky_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    #def __repr__(self):
        #return f"Stocks(name = {name}, price = {price})"

class StockSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StocksModel
        sqla_session = db.session
        #dicen que load_instance = True es mejor

stocks_put_args = reqparse.RequestParser()
stocks_put_args.add_argument(
    "name", type=str, help="Stock´s name", required=True)
stocks_put_args.add_argument(
    "price", type=int, help="Stocks´s price", required=True)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Integer
}

class StockGet(Resource):

    @marshal_with(resource_fields)
    def get(self, stock_id):
        result = StocksModel.query.filter_by(id=stock_id).first()
        return result

class StockPut(Resource):

    @marshal_with(resource_fields)
    def put(self):
        args = stocks_put_args.parse_args()
        stock = StocksModel(name=args['name'], price=args['price'])
        db.session.add(stock)
        db.session.commit()
        stocky_schema = StockSchema()
        return stocky_schema.dump(stocks).data



api.add_resource(StockGet, "/stock/<int:stock_id>")
api.add_resource(StockPut, "/stock/create")

if __name__ == "__main__":
    app.run(debug=True)

