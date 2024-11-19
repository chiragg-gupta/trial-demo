from extensions import db, ma
from datetime import datetime
#tryyyyyyyyyyy
class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    regnum = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    wed_refid = db.Column(db.String)
    checkin_date = db.Column(db.Date)
    checkout_date = db.Column(db.Date)
    checkin_time = db.Column(db.Time)
    checkout_time = db.Column(db.Time)
    night = db.Column(db.Integer)
    purpose = db.Column(db.String)
    business_src = db.Column(db.Integer)
    guest_type = db.Column(db.Integer)
    market_segment = db.Column(db.Integer)
    res_status = db.Column(db.String)
    is_dayuse = db.Column(db.Boolean)
    is_houseuse = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    canceled_on = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer)
    modified_by = db.Column(db.Integer)
    preference = db.Column(db.String)

    # Relationships
    arrival = db.relationship("Arrival", backref="reservation", uselist=False)  # One-to-one
    departure = db.relationship("Departure", backref="reservation", uselist=False)  # One-to-one
    special_discounts = db.relationship("SpecialDiscount", backref="reservation", lazy="joined")  # One-to-many
    discount_coupons = db.relationship("DiscountCoupon", backref="reservation", lazy="joined")  # One-to-many
    custom_fields = db.relationship("CustomField", backref="reservation", lazy="joined")  # One-to-many
    room_stays = db.relationship('RsvRoom', backref='reservation', lazy=True)  # One-to-many
    guests = db.relationship('RsvRmGuest', backref='reservation', lazy=True)  # One-to-many
    messages = db.relationship('RsvRmMessage', backref='reservation', lazy=True)  # One-to-many
    tariffs = db.relationship('RsvRmTariff', backref='reservation', lazy=True)  # One-to-many
class Arrival(db.Model):
    __tablename__ = 'arrivals'
    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.Integer)
    detail = db.Column(db.String)
    time = db.Column(db.Time)
    is_assign = db.Column(db.Boolean)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
class Departure(db.Model):
    __tablename__ = 'departures'
    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.Integer)
    detail = db.Column(db.String)
    time = db.Column(db.Time)
    is_assign = db.Column(db.Boolean)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
class SpecialDiscount(db.Model):
    __tablename__ = 'special_discounts'
    id = db.Column(db.Integer, primary_key=True)
    req_id = db.Column(db.Integer)
    req_code = db.Column(db.String)
    req_name = db.Column(db.String)
    disc = db.Column(db.Float)
    disc_type = db.Column(db.String)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
class DiscountCoupon(db.Model):
    __tablename__ = 'discount_coupons'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String)
    disc = db.Column(db.Float)
    disc_type = db.Column(db.String)
    disc_amount = db.Column(db.Float)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
class CustomField(db.Model):
    __tablename__ = 'custom_fields'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String)
    name = db.Column(db.String)
    value = db.Column(db.String)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
class RsvRoom(db.Model):
    __tablename__ = 'rsvRooms'
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
    beds = db.relationship('Bed', backref='room', lazy=True)
class Bed(db.Model):
    __tablename__ = 'beds'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rsvRooms.id'))
class RsvRmGuest(db.Model):
    __tablename__ = 'rsvRmGuests'
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
class RsvRmMessage(db.Model):
    __tablename__ = 'rsvRmMessages'
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
class RsvRmTariff(db.Model):
    __tablename__ = 'rsvRmTariff'
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
    rsv_tariff_rates = db.relationship('RsvRmTariffRate', backref='tariff', lazy=True)
    rsv_tariff_inclusions = db.relationship('RsvRmTariffInclusion', backref='tariff', lazy=True)
    rsv_room_transactions = db.relationship('RsvRoomTransaction', backref='tariff', lazy=True)
class RsvRmTariffRate(db.Model):
    __tablename__ = 'rsvRmTariffRates'
    id = db.Column(db.Integer, primary_key=True)
    tariff_id = db.Column(db.Integer, db.ForeignKey('rsvRmTariff.id'))
class RsvRmTariffInclusion(db.Model):
    __tablename__ = 'rsvRmTariffInclusions'
    id = db.Column(db.Integer, primary_key=True)
    tariff_id = db.Column(db.Integer, db.ForeignKey('rsvRmTariff.id'))
class RsvRoomTransaction(db.Model):
    __tablename__ = 'rsvRoomTransactions'
    id = db.Column(db.Integer, primary_key=True)
    tariff_id = db.Column(db.Integer, db.ForeignKey('rsvRmTariff.id'))
