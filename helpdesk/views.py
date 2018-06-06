from django.shortcuts import render, HttpResponseRedirect
from .models import *
from .forms import *

def index(request):
    template = 'help_index.html'
    guideline = HelpDeskGuideLine.objects.all().order_by('date_created')
    int_faq_list = FAQ.objects.all().order_by('title')
    ext_faq_list = FAQ.objects.filter(internal=False).order_by('title')
    int_form = InternalEnquiryForm()
    ext_form = ExternalEnquiryForm()

    context = {
        'guideline': guideline,
        'int_faq_list': int_faq_list,
        'ext_faq_list': ext_faq_list,
        'int_form': int_form,
        'ext_form': ext_form,
    }

    return render(request, template, context)

def enquire(request):
    if request.user.is_authenticated:
        form = InternalEnquiryForm()
        if request.method == 'POST':
            if form.is_valid():
                form = InternalEnquiryForm(request.POST)
                form.user_detail = request.user
                form.save()
                return render(request, 'enquiry_confirmation.html', {'enquiry': form})
        else:
            return HttpResponseRedirect('help_index')
    else:
        form = InternalEnquiryForm()
        if request.method == 'POST':
            if form.is_valid():
                form = ExternalEnquiryForm(request.POST)
                form.save()
                return render(request, 'enquiry_confirmation.html', {'enquiry': form})
        else:
            return HttpResponseRedirect('help_index')