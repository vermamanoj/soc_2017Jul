from django.forms import ModelForm
from gentelella.core.models import CustomerInfo

class CustomerInfoForm(ModelForm):
    class Meta:
        model = CustomerInfo
        fields = ['uid','customer_name','customer_location']