from django import forms
from .models import Parcel


class TrackingForm(forms.Form):
    tracking_no = forms.CharField(required=True)


class ConfirmForm(forms.Form):
    check_box = forms.BooleanField(required=True)


class CreateParcel(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ('weight', 'p_height', 'p_depth', 'p_width', 'distance', 'r_id_req',
                  'sender_first_name', 'sender_surname', 'sender_address', 'sender_city', 'sender_zip',
                  'recipient_first_name', 'recipient_surname', 'recipient_address',
                  'recipient_city', 'recipient_zip', 'price', 'current_location')
        exclude = ('track_n', 'confirmed', 'sh_weight', 'status', 'failed', 'owner', 'sh_weight')
        widgets = {
            'weight': forms.NumberInput(attrs={'placeholder': 'Parcel weight in KG'}),
            'p_height': forms.NumberInput(attrs={'placeholder': 'Parcel height in CM'}),
            'p_width': forms.NumberInput(attrs={'placeholder': 'Parcel width in CM'}),
            'p_depth': forms.NumberInput(attrs={'placeholder': 'Parcel depth in CM'}),
            'distance': forms.NumberInput(attrs={'placeholder': 'Shipping Distance in KM'}),
            'sender_first_name': forms.TextInput(attrs={'placeholder': 'Sender First Name'}),
            'sender_surname': forms.TextInput(attrs={'placeholder': 'Sender Surname'}),
            'sender_address': forms.TextInput(attrs={'placeholder': 'Sender Address'}),
            'sender_city': forms.Select(attrs={'empty': 'Sender City'}),
            'sender_zip': forms.NumberInput(attrs={'placeholder': 'Sender ZIP code'}),
            'sender_personal_msg': forms.Textarea(attrs={'placeholder': "Sender's personal message"}),
            'recipient_first_name': forms.TextInput(attrs={'placeholder': 'Recipient First Name'}),
            'recipient_surname': forms.TextInput(attrs={'placeholder': 'Recipient Surname'}),
            'recipient_address': forms.TextInput(attrs={'placeholder': 'Recipient Address'}),
            'recipient_city': forms.Select(attrs={'placeholder': 'Recipient City'}),
            'recipient_zip': forms.NumberInput(attrs={'placeholder': 'Recipient ZIP code'}),
        }