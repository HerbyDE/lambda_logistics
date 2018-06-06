from django.db import models
import uuid

#Function to generate the Tracking number. To be improved by creating unique values.
def gen_tracking_no():
    return str(uuid.uuid4().hex[:8].upper())


class Office(models.Model):
    TYPE_CHOICE_LIST = (
        ('Headquarter', 'Headquarter'), ('Regional Hub', 'Regional Hub'), ('Satellite Office', 'Satellite Office')
    )

    name = models.CharField(max_length=70, unique=True)
    city = models.CharField(max_length=70, unique=True)
    address = models.CharField(max_length=70)
    type = models.CharField(max_length=25, choices=TYPE_CHOICE_LIST)

    def __str__(self):
        return str(self.name)


#Core Class
class Parcel(models.Model):
    CREATED = 'Created'
    FETCHED = 'Fetched'
    IN_HUB_INBOUND = 'In Hub Inbound'
    IN_HUB_OUTBOUND = 'In Hub Outbound'
    IN_TRANSIT = 'In Transit'
    DELIVERED = 'Delivered'
    DEL_FAIL = 'Delivery Failed'
    STATUS_CHOICE_LIST = (('Created', 'CREATED'), ('Fetched', 'FETCHED'), ('In Hub Inbound', 'IN HUB INBOUND'),
                          ('In Hub Outbound', 'IN HUB OUTBOUND'), ('In Transit', 'IN TRANSIT'),
                          ('Delivered', 'DELIVERED'), ('Delivery Failed', 'DELIVERY FAILED'))

    track_n = models.CharField(default=gen_tracking_no, blank=False, unique=True, max_length=8)
    confirmed = models.BooleanField(default=False)
    r_id_req = models.BooleanField(default=False)
    p_height = models.PositiveIntegerField(blank=False, null=False)
    p_width = models.PositiveIntegerField(blank=False)
    p_depth = models.PositiveIntegerField(blank=False)
    weight = models.PositiveIntegerField(blank=False)
    status = models.CharField(choices=STATUS_CHOICE_LIST, default='Created', max_length=25)
    failed = models.IntegerField(blank=True, default=0)
    distance = models.IntegerField(blank=False)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    sender_first_name = models.CharField(max_length=70, blank=False)
    sender_surname = models.CharField(max_length=70, blank=False)
    sender_address = models.CharField(max_length=100, blank=False)
    sender_city = models.ForeignKey(Office, to_field='city', related_name='+', default='Cape Town Central - Airport')
    sender_zip = models.IntegerField()
    recipient_first_name = models.CharField(max_length=70, blank=False)
    recipient_surname = models.CharField(max_length=70, blank=False)
    recipient_address = models.CharField(max_length=100)
    recipient_city = models.ForeignKey(Office, to_field='city', related_name='+', default='Cape Town Central - Airport')
    recipient_zip = models.IntegerField(blank=False, null=True)
    date_created = models.DateField(blank=True, null=True, auto_now_add=True)
    date_fetched = models.DateField(blank=True, null=True)
    date_inhub = models.DateField(blank=True, null=True)
    date_intransit = models.DateField(blank=True, null=True)
    date_delivered = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    current_location = models.ForeignKey(Office, blank=True, null=True)

    def sh_weight(self):
        return (self.p_height * self.p_width * self.P_depth) / 5000

    def __str__(self):
        return str(self.track_n)