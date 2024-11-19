from flask import Flask, jsonify, request
import os
from extensions import db, ma
from dotenv import load_dotenv
from models import *
from datetime import datetime
from sqlalchemy.orm import joinedload
from Schema import *

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('FLASK_SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('FLASK_SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ('true', '1')
app.config['FLASK_SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

db.init_app(app)
ma.init_app(app)

@app.route('/reservations', methods=['GET'])
def get_reservations():
    try:
        reservations = Reservation.query.options(
            joinedload(Reservation.arrival),
            joinedload(Reservation.departure),
            joinedload(Reservation.special_discounts),
            joinedload(Reservation.discount_coupons),
            joinedload(Reservation.custom_fields),
            joinedload(Reservation.room_stays),
            joinedload(Reservation.guests),
            joinedload(Reservation.messages),
            joinedload(Reservation.tariffs)
        ).all()
        if not reservations:
            return jsonify({"message": "No reservations found"}), 404
        reservation_schema = ReservationSchema(many=True)
        result = reservation_schema.dump(reservations)
        return jsonify(result)    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/reservations/<int:id>',methods=['GET'])
def get_reservation(id):
    try:
        reservation = Reservation.query.options(
            joinedload(Reservation.arrival),
            joinedload(Reservation.departure),
            joinedload(Reservation.special_discounts),
            joinedload(Reservation.discount_coupons),
            joinedload(Reservation.custom_fields),
            joinedload(Reservation.room_stays),
            joinedload(Reservation.guests),
            joinedload(Reservation.messages),
            joinedload(Reservation.tariffs)
        ).filter_by(id=id).first()
        if not reservation:
            return jsonify({"message": "No reservation found"}), 404
        reservation_schema = ReservationSchema()
        result = reservation_schema.dump(reservation)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reservations', methods=['POST'])
def create_reservation():
    try:
        data = request.get_json()

        reservation = Reservation(
            regnum=data['regnum'],
            type=data['type'],
            wed_refid=data['wed_refid'],
            checkin_date=datetime.strptime(data['checkin_date'], '%Y-%m-%d').date(),
            checkout_date=datetime.strptime(data['checkout_date'], '%Y-%m-%d').date(),
            checkin_time=datetime.strptime(data['checkin_time'], '%H:%M:%S').time(),
            checkout_time=datetime.strptime(data['checkout_time'], '%H:%M:%S').time(),
            night=data['night'],
            purpose=data['purpose'],
            business_src=data['business_src'],
            guest_type=data['guest_type'],
            market_segment=data['market_segment'],
            res_status=data['res_status'],
            is_dayuse=data['is_dayuse'],
            is_houseuse=data['is_houseuse'],
            created_by=data['created_by'],
            modified_by=data['modified_by'],
            preference=data['preference'],
            created_on=datetime.utcnow(),
            modified_on=datetime.utcnow()
        )

        arrival = Arrival(
            mode=data['arrival']['mode'],
            detail=data['arrival']['detail'],
            time=datetime.strptime(data['arrival']['time'], '%H:%M:%S').time(),
            is_assign=data['arrival']['is_assign'],
            reservation=reservation # FOR STORING RESERVATION ID IN ARRIVAL MODEL
        )

        departure = Departure(
            mode=data['departure']['mode'],
            detail=data['departure']['detail'],
            time=datetime.strptime(data['departure']['time'], '%H:%M:%S').time(),
            is_assign=data['departure']['is_assign'],
            reservation=reservation
        )

        for disc in data['special_discounts']:
            special_discount = SpecialDiscount(
                req_id=disc['req_id'],
                req_code=disc['req_code'],
                req_name=disc['req_name'],
                disc=disc['disc'],
                disc_type=disc['disc_type'],
                reservation=reservation
            )
            db.session.add(special_discount)

        for coupon in data['discount_coupons']:
            discount_coupon = DiscountCoupon(
                code=coupon['code'],
                disc=coupon['disc'],
                disc_type=coupon['disc_type'],
                disc_amount=coupon['disc_amount'],
                reservation=reservation
            )
            db.session.add(discount_coupon)

        for field in data['custom_fields']:
            custom_field = CustomField(
                code=field['code'],
                name=field['name'],
                value=field['value'],
                reservation=reservation
            )
            db.session.add(custom_field)

        db.session.add(reservation)
        db.session.commit()

        reservation_schema = ReservationSchema()
        result = reservation_schema.dump(reservation)
        return jsonify(result), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
