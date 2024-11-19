from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from models import * 
class ArrivalSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Arrival
        include_fk = True
        load_instance = True
        fields = ('id', 'mode', 'detail', 'time', 'is_assign', 'reservation_id')
class DepartureSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Departure
        include_fk = True
        load_instance = True
        fields = ('id', 'mode', 'detail', 'time', 'is_assign', 'reservation_id')
class SpecialDiscountSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SpecialDiscount
        include_fk = True
        load_instance = True
        fields = ('id', 'req_id', 'req_code', 'req_name', 'disc', 'disc_type', 'reservation_id')
class DiscountCouponSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DiscountCoupon
        include_fk = True
        load_instance = True
        fields = ('id', 'code', 'disc', 'disc_type', 'disc_amount', 'reservation_id')
class CustomFieldSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CustomField
        include_fk = True
        load_instance = True
        fields = ('id', 'code', 'name', 'value', 'reservation_id')
class BedSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Bed
        include_fk = True
        load_instance = True
        fields = ('id', 'room_id')
class RsvRoomSchema(SQLAlchemyAutoSchema):
    beds = fields.Nested('BedSchema', many=True, exclude=['id'])  

    class Meta:
        model = RsvRoom
        include_fk = True
        load_instance = True
        fields = ('id', 'reservation_id', 'beds')
class RsvRmGuestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RsvRmGuest
        include_fk = True
        load_instance = True
        fields = ('id', 'reservation_id')
class RsvRmMessageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RsvRmMessage
        include_fk = True
        load_instance = True
        fields = ('id', 'reservation_id')
class RsvRmTariffRateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RsvRmTariffRate
        include_fk = True
        load_instance = True
        fields = ('id', 'tariff_id')
class RsvRmTariffInclusionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RsvRmTariffInclusion
        include_fk = True
        load_instance = True
        fields = ('id', 'tariff_id')
class RsvRoomTransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RsvRoomTransaction
        include_fk = True
        load_instance = True
        fields = ('id', 'tariff_id')
class RsvRmTariffSchema(SQLAlchemyAutoSchema):
    rsv_tariff_rates = fields.Nested('RsvRmTariffRateSchema', many=True)
    rsv_tariff_inclusions = fields.Nested('RsvRmTariffInclusionSchema', many=True)

    class Meta:
        model = RsvRmTariff
        include_fk = True
        load_instance = True
        fields = ('id', 'reservation_id', 'rsv_tariff_rates', 'rsv_tariff_inclusions')
class ReservationSchema(SQLAlchemyAutoSchema):
    arrival = fields.Nested(ArrivalSchema, many=False, exclude=['id'])
    departure = fields.Nested(DepartureSchema, many=False, exclude=['id'])
    special_discounts = fields.Nested(SpecialDiscountSchema, many=True, exclude=['id'])
    discount_coupons = fields.Nested(DiscountCouponSchema, many=True, exclude=['id'])
    custom_fields = fields.Nested(CustomFieldSchema, many=True, exclude=['id'])
    room_stays = fields.Nested(RsvRoomSchema, many=True, exclude=['id'])
    guests = fields.Nested(RsvRmGuestSchema, many=True, exclude=['id'])
    messages = fields.Nested(RsvRmMessageSchema, many=True, exclude=['id'])
    tariffs = fields.Nested(RsvRmTariffSchema, many=True, exclude=['id'])

    class Meta:
        model = Reservation
        include_fk = True
        load_instance = True
        fields = (
            'id', 'regnum', 'type', 'wed_refid', 'checkin_date', 'checkout_date', 'checkin_time',
            'checkout_time', 'night', 'purpose', 'business_src', 'guest_type', 'market_segment',
            'res_status', 'is_dayuse', 'is_houseuse', 'created_on', 'modified_on', 'canceled_on',
            'created_by', 'modified_by', 'preference', 'arrival', 'departure', 'special_discounts',
            'discount_coupons', 'custom_fields', 'room_stays', 'guests', 'messages', 'tariffs'
        )
