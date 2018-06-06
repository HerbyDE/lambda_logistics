from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(InternalEnquiry)
admin.site.register(ExternalEnquiry)
admin.site.register(HelpDeskGuideLine)
admin.site.register(FAQ)
