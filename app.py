import json
import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mybase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        res = []
        for user in User.query.all():
            res.append(user.to_dict())
        return jsonify(res)
    if request.method == 'POST':
        try:
            user = json.loads(request.data)
            news_user_obj = User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone']
            )
            db.session.add(news_user_obj)
            db.session.commit()
            db.session.close()
            return "Пользователь создан в базе данных", 200
        except Exception as e:
            return e


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return "Не найдено"
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден", 404
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.phone = user_data['phone']
        user.role = user_data['role']
        user.email = user_data['email']
        user.age = user_data['age']
        db.session.add(user)
        db.session.commit()
        return f"Пользователь с id {user_id} изменен", 200

    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден", 404
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {user_id} удален", 200


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        res = []
        for order in Order.query.all():
            res.append(order.to_dict())
        return jsonify(res)
    if request.method == 'POST':
        try:
            order = json.loads(request.data)
            month_start, day_start, year_start = [int(_) for _ in order['start_date'].split("/")]
            month_end, day_end, year_end = [int(_) for _ in order['end_date'].split("/")]
            new_order_obj = Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.date(year=year_start, month=month_start, day=day_start),
                end_date=datetime.date(year=year_end, month=month_end, day=day_end),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id']
            )
            db.session.add(new_order_obj)
            db.session.commit()
            db.session.close()
            return "Заказ создан в базе данных", 200
        except Exception as e:
            return e


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    if request.method == 'GET':
        order = Order.query.get(order_id)
        if order is None:
            return "Заказ не найден"
        return jsonify(order.to_dict())

    elif request.method == 'PUT':
        order = db.session.query(Order).get(order_id)
        order_data = json.loads(request.data)
        month_start, day_start, year_start = [int(_) for _ in order_data['start_date'].split("/")]
        month_end, day_end, year_end = [int(_) for _ in order_data['end_date'].split("/")]


        if order is None:
            return "Заказ не найден", 404

        order.id = order_data['id']
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = order_data['start_date']
        order.end_date = order_data['end_date']
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']

        order.start_date = datetime.date(year=year_start, month=month_start, day=day_start)
        order.end_date = datetime.date(year=year_end, month=month_end, day=day_end)

        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f"Заказ с id {order_id} изменен", 200

    elif request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)
        if order is None:
            return "Заказ не найден", 404
        db.session.delete(order)
        db.session.commit()
        db.session.close()
        return f"Заказ с id {order_id} удален", 200


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        res = []
        for offer in Offers.query.all():
            res.append(offer.to_dict())
        return jsonify(res)
    if request.method == 'POST':
        offer = json.loads(request.data)
        news_offer_obj = Offers(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        )
        db.session.add(news_offer_obj)
        db.session.commit()
        db.session.close()
        return "Предложение создано в базе данных", 200


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offer_id):
    if request.method == 'GET':
        offer = Offers.query.get(offer_id)
        if offer is None:
            return "Предложение не найдено"
        return jsonify(offer.to_dict())

    elif request.method == 'PUT':
        offer = db.session.query(Offers).get(offer_id)
        offer_data = json.loads(request.data)
        if offer is None:
            return "Предложение не найдено", 404
        offer.id = offer_data['id']
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        return f"Предложение с id {offer_id} изменено", 200

    elif request.method == 'DELETE':
        offer = db.session.query(Offers).get(offer_id)
        if offer is None:
            return "Предложение не найдено", 404
        db.session.delete(offer)
        db.session.commit()
        db.session.close()
        return f"Предложение с id {offer_id} удалено", 200


if __name__ == '__main__':
    app.run()
