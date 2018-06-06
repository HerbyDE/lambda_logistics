from rest_framework import serializers
from corelogistics.models import Parcel

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ('track_n', 'weight', 'p_height', 'p_depth', 'p_width', 'distance', 'r_id_req',
                  'sender_first_name', 'sender_surname', 'sender_address', 'sender_city', 'sender_zip',
                  'recipient_first_name', 'recipient_surname', 'recipient_address',
                  'recipient_city', 'recipient_zip')


class ParcelPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ('track_n', 'price')
