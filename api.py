from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import desc


################## CONFIG ##################

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

ma = Marshmallow(app)


################## MODELS ##################

class StockModel(db.Model):
    __tablename__ = "stock"
    __table_args__ = (
        db.UniqueConstraint('name'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)



class StockSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StockModel
        load_instance = True



################## RECREATE DATABASE ##################

db.drop_all()
db.create_all()
db.session.commit()


################## REQUEST PARSERS ##################

stocks_put_args = reqparse.RequestParser()
stocks_put_args.add_argument(
    "name", type=str, help="Stock's name", required=True)
stocks_put_args.add_argument(
    "price", type=float, help="Stocks's price", required=True)


stocks_post_args = reqparse.RequestParser()
stocks_post_args.add_argument(
    "price", type=float, help="Stocks's price", required=True)


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Float
}


################## RESOURCES ##################


class StockGet(Resource):

    @marshal_with(resource_fields)
    def get(self, name):
        result = StockModel.query.filter_by(name=name.upper()).first()
        return result


class StockPut(Resource):

    @marshal_with(resource_fields)
    def put(self):
        args = stocks_put_args.parse_args()
        
        stock = StockModel(name=args['name'], price=args['price'])
        db.session.add(stock)
        db.session.commit()
        stocky_schema = StockSchema()
        
        return stocky_schema.dump(stock)


class StockPost(Resource):

    @marshal_with(resource_fields)
    def post(self, name):
        args = stocks_post_args.parse_args()
        
        stock = StockModel.query.filter_by(name=name.upper()).first()
        stock.price = args['price']
        db.session.commit()

        stocky_schema = StockSchema()
        
        return stocky_schema.dump(stock)

class StockOrder(Resource):

    @marshal_with(resource_fields)
    def get(self):
        stock= StockModel.query.order_by(desc(StockModel.price)).all()

        stocky_schema = StockSchema(many=True)
        
        return stocky_schema.dump(stock)


api.add_resource(StockPut, "/stock/create")
api.add_resource(StockPost, "/stock/<name>/update")
api.add_resource(StockGet, "/stock/<name>")
api.add_resource(StockOrder, "/stock/all")




################## MAIN ##################

if __name__ == "__main__":
    app.run(debug=True)

