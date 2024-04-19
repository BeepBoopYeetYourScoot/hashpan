from rest_framework import serializers


class TransportOrderSerializer(serializers.Serializer):
    num = serializers.IntegerField()
    order_num = serializers.CharField()
    oper_code = serializers.IntegerField()
    route = serializers.CharField()
    term_code = serializers.IntegerField()
    smena = serializers.IntegerField()
    ticket_number = serializers.CharField()
    card_mask = serializers.CharField()
    hashpan = serializers.CharField()
    amount = serializers.FloatField()
    date_of = serializers.DateTimeField()
    date_payment = serializers.DateTimeField(required=False, allow_null=True)
    state = serializers.CharField()
    comment = serializers.CharField(required=False, allow_blank=True)
    approval = serializers.CharField(required=False, allow_blank=True)
