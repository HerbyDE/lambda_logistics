from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q
from .forms import *
from .models import *
from .plotting import *
from .custom_decorators import group_required

from django.db.models import Sum



# PARCEL HANDLING VIEWS AND FUNCTIONS
@group_required('Client', 'Warehouse Manager')
@login_required #Running
def create_parcel(request):
    if request.method == 'POST':
        form = CreateParcel(request.POST)
        if form.is_valid():
            form.save(commit=False)
            parcel = form.save()
            sh_weight = (parcel.p_depth * parcel.p_depth * parcel.p_height) / (5000*1000)
            if parcel.distance > 500:
                if sh_weight > parcel.weight:
                    c = round(sh_weight * 199)
                    print(1)
                else:
                    c = round(parcel.weight * 199)
                    print(2)
            else:
                if sh_weight > parcel.weight:
                    c = round(sh_weight * 99)
                    print(3)
                else:
                    c = round(parcel.weight * 99)
                    print(4)
            print(c)
            parcel.price = c
            parcel.owner = request.user
            parcel.current_location = form.cleaned_data['sender_city']
            parcel.confirmed = True
            parcel.save()
            return render(request, 'confirm_parcel.html', {'parcel': parcel})
        else:
            print(form.errors)
            return render(request, 'create_parcel.html', {'form': form})
    else:
        form = CreateParcel()
    return render(request, 'create_parcel.html', {'form': form})

#running
def confirm_parcel(request, pk):
    obj = Parcel.objects.get(pk=pk)
    if request.GET.get['confirm'] == 'confirm':
        con = obj.save()
        con.confirmed = True
        con.save()
        return HttpResponseRedirect('parcel_list')
    elif request.GET.get['cancel'] == 'cancel':
        obj.delete()
        return HttpResponseRedirect('parcel_list')
    else:
        return HttpResponseRedirect('parcel_list')

#running
@login_required
def cancel_parcel(request, pk):
    obj = get_object_or_404(Parcel, pk=pk)
    obj.confirmed = 'True'
    obj.save()
    return HttpResponseRedirect('parcel_list')

#running
@login_required #running
def parcel_list(request):
    model = Parcel.objects.all()
    template = 'parcel_list.html'
    data = model.exclude(status='DE')
    data2 = model
    data3 = model.filter(status='DC')
    dict = {
        'parcel_list_active': data,
        'parcel_list_all': data2,
        'parcel_list_delivered': data3,
    }
    return render(request, template, dict)

#running
@login_required #running; for administrative use only
def status_update_admin(request, pk):
    parcel = Parcel.objects.get(pk=pk)
    if parcel.status == 'Created':
        parcel.status = 'Fetched'
        parcel.date_fetched = date.today()
        parcel.save()
        return redirect('/core/parcel/list/')
    else:
        if parcel.status == 'Fetched':
            parcel.status = 'In Hub Inbound'
            parcel.date_inhub = date.today()
            parcel.save()
            return redirect('/core/parcel/list/')
        else:
            if parcel.status == 'In Hub Inbound':
                parcel.status = 'In Hub Outbound'
                parcel.date_inhub = date.today()
                parcel.save()
                return redirect('/core/parcel/list/')
            else:
                if parcel.status == 'In Hub Outbound':
                    parcel.status = 'In Transit'
                    parcel.current_location = parcel.recipient_city
                    parcel.date_intransit = date.today()
                    parcel.save()
                    return redirect('/core/parcel/list/')
                else:
                    if parcel.status == 'In Transit':
                        parcel.status = 'Delivered'
                        parcel.date_delivered = date.today()
                        parcel.save()
                        return redirect('/core/parcel/list/')
                    else:
                        if parcel.status == 'Delivery Failed':
                            parcel.status = 'Delivered'
                            parcel.date_delivered = date.today()
                            parcel.save()
                            return redirect('/core/parcel/list/')
                        else:
                            return redirect('/core/parcel/list/')

#running
@login_required #failing
def delivery_fails_admin(request, pk):
    parcel = Parcel.objects.get(pk=pk)
    if parcel.status == 'In Transit' or parcel.status == 'Delivery Failed':
        parcel.status = 'Delivery Failed'
        parcel.failed += 1
        parcel.save()
        return redirect('/core/parcel/list/')
    else:
        return redirect('/core/parcel/list/')

#running
@login_required
def delivery_reset_admin(request, pk):
    parcel = Parcel.objects.get(pk=pk)
    parcel.status = 'Created'
    parcel.save()
    return redirect('/core/parcel/list/')

#running
@login_required #running; View to update parcels as warehouse mgr and driver
def status_update(request, pk):
    parcel = Parcel.objects.get(pk=pk)
    if parcel.status == 'Created':
        parcel.status = 'Fetched'
        parcel.date_fetched = date.today()
        parcel.save()
        return redirect('/core/driver/log/')
    else:
        if parcel.status == 'Fetched':
            parcel.status = 'In Hub Inbound'
            parcel.date_inhub = date.today()
            parcel.save()
            return redirect('/core/driver/log/')
        else:
            if parcel.status == 'In Hub Inbound':
                parcel.status = 'In Hub Outbound'
                parcel.date_inhub = date.today()
                parcel.save()
                return redirect('/core/driver/log/')
            else:
                if parcel.status == 'In Hub Outbound':
                    parcel.status = 'In Transit'
                    parcel.current_location = parcel.recipient_city
                    parcel.date_intransit = date.today()
                    parcel.save()
                    return redirect('/core/driver/log/')
                else:
                    if parcel.status == 'In Transit':
                        parcel.status = 'Delivered'
                        parcel.date_delivered = date.today()
                        parcel.save()
                        return redirect('/core/driver/log/')
                    else:
                        if parcel.status == 'Delivery Failed':
                            parcel.status = 'Delivered'
                            parcel.date_delivered = date.today()
                            parcel.save()
                            return redirect('/core/driver/log/')
                        else:
                            return redirect('/core/driver/log/')

#running
@login_required #failing
def delivery_fails(request, pk):
    parcel = Parcel.objects.get(pk=pk)
    if parcel.status == 'In Transit' or parcel.status == 'Delivery Failed':
        parcel.status = 'Delivery Failed'
        parcel.failed += 1
        parcel.save()
        return redirect('/core/driver/log/')
    else:
        return redirect('/core/driver/log/')

#running
@login_required
def delivery_reset(request, pk):
    parcel = Parcel.objects.get(pk=pk)
    parcel.status = 'Created'
    parcel.save()
    return redirect('/core/parcel/list/')

#running
@login_required #running
def parcel_detail(request, pk):
    parcel = get_object_or_404(Parcel, pk=pk)
    return render_to_response('parcel_detail.html', {'parcel': parcel})


#running
def track_parcel(request):
    parcel = Parcel.objects.all()
    query = request.GET.get('term')
    if query:
        parcel = parcel.filter(Q(track_n__iexact=query))
        return render(request, 'search.html', {'parcel': parcel})
    else:
        return render(request, 'search.html')


# OTHER VIEWS
#running !!! loader.template does not pass any data except the template. So no user authentication possible.
def landing_page(request):
    template = 'index.html'
    context = ''
    return render(request, template, {'context': context})


#running
def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render(request, 'login.html')


#running
@group_required('Management', 'Client')
@login_required
def dashboard(request):
    ###### MANAGEMENT DASHBOARD ######
    # Status Chart
    ccr = Parcel.objects.filter(status='Created').count()
    cft = Parcel.objects.filter(status='Fetched').count()
    chbi = Parcel.objects.filter(status='In Hub Inbound').count()
    chbo = Parcel.objects.filter(status='In Hub Outbound').count()
    cit = Parcel.objects.filter(status='In Transit').count()
    cde = Parcel.objects.filter(status='Delivered').count()
    cdf = Parcel.objects.filter(status='Delivery Failed').count()
    current = barchart(x_data=['Created', 'Fetched', 'In Hub Inbound', 'In Hub Outbound', 'In Transit', 'Delivered',
                               'Delivery Failed'],
                       y_data=[ccr, cft, chbi, chbo, cit, cde, cdf], name='Logistics')

    # Overview Chart
    parcel = Parcel.objects.all()
    dates_created = []
    dates_fetched = []
    dates_inhub = []
    dates_intransit = []
    dates_delivered = []

    for i in parcel:
        # Creation Date
        c = i.date_created
        dates_created.append(c)
        # Fetch Date
        f = i.date_fetched
        dates_fetched.append(f)
        # Dates Inhub
        h = i.date_inhub
        dates_inhub.append(h)
        # Dates In Transit
        t = i.date_intransit
        dates_intransit.append(t)
        # Dates Delivered
        d = i.date_delivered
        dates_delivered.append(d)

    created = dict()
    for date in dates_created:
        if date in created:
            created[date] += 1
        else:
            created[date] = 1

    fetched = dict()
    for date in dates_fetched:
        if date in fetched:
            fetched[date] += 1
        else:
            fetched[date] = 1

    inhub = dict()
    for date in dates_inhub:
        if date in inhub:
            inhub[date] += 1
        else:
            inhub[date] = 1

    transit = dict()
    for date in dates_intransit:
        if date in transit:
            transit[date] += 1
        else:
            transit[date] = 1

    delivered = dict()
    for date in dates_delivered:
        if date in delivered:
            delivered[date] += 1
        else:
            delivered[date] = 1

    overview = linegraph(x_data=list(created.keys()), y1=list(created.values()), y2=list(fetched.values()),
                         y3=list(inhub.values()), y4=list(transit.values()), y5=list(delivered.values()))

    # Pie Chart for Weight Distribution and Distance statistics
    total = Parcel.objects.all().count()
    # Weight statistics (if statement to avoid division by zero error)
    if total > 0:
        d1 = (Parcel.objects.filter(weight__lt=5)).count() / total
        d2 = (Parcel.objects.filter(weight__range=(5, 10))).count() / total
        d3 = (Parcel.objects.filter(weight__range=(10, 20))).count() / total
        d4 = (Parcel.objects.filter(weight__range=(20, 30))).count() / total
        d5 = (Parcel.objects.filter(weight__range=(30, 50))).count() / total
        d6 = (Parcel.objects.filter(weight__gte=50)).count() / total
        # Distance Statistics
        d7 = (Parcel.objects.filter(distance__lt=500)).count() / total
        d8 = (Parcel.objects.filter(distance__gte=500)).count() / total
    else:
        d1 = 0
        d2 = 0
        d3 = 0
        d4 = 0
        d5 = 0
        d6 = 0
        d7 = 0
        d8 = 0
    dist_charts = pie_chart(d1=d1, d2=d2, d3=d3, d4=d4, d5=d5, d6=d6, l1='< 5kg', l2='5kg < x < 10kg',
                            l3='10kg < x < 20kg', l4='20kg < x < 30kg', l5='30kg < x < 50kg', l6='> 50kg', d7=d7,
                            d8=d8, l7='Short Distance', l8='Long Distance')

    year = datetime.now().year
    month = datetime.now().month
    previous_month = month-1
    total_costs = Parcel.objects.all().aggregate(Sum('price')).get('price__sum', 0.00)
    costs_current = Parcel.objects.filter(date_created__month=month, date_created__year=year).aggregate(Sum('price')).get('price__sum', 0.00)
    costs_previous = Parcel.objects.filter(date_created__month=previous_month, date_created__year=year).aggregate(Sum('price')).get('price__sum', 0.00)

    ###### CLIENT DASHBOARD ######
    client = request.user
    # Status Chart
    ccr_c = Parcel.objects.filter(status='Created', owner=client).count()
    cft_c = Parcel.objects.filter(status='Fetched', owner=client).count()
    chbi_c = Parcel.objects.filter(status='In Hub Inbound', owner=client).count()
    chbo_c = Parcel.objects.filter(status='In Hub Outbound', owner=client).count()
    cit_c = Parcel.objects.filter(status='In Transit', owner=client).count()
    cde_c = Parcel.objects.filter(status='Delivered', owner=client).count()
    cdf_c = Parcel.objects.filter(status='Delivery Failed').count()
    current_c = barchart(x_data=['Created', 'Fetched', 'In Hub Inbound', 'In Hub Outbound', 'In Transit', 'Delivered',
                                 'Delivery Failed'],
                         y_data=[ccr_c, cft_c, chbi_c, chbo_c, cit_c, cde_c, cdf_c], name='Logistics')

    # Client Overview Chart
    parcel_c = Parcel.objects.filter(owner=client)
    dates_created_c = []
    dates_fetched_c = []
    dates_inhub_c = []
    dates_intransit_c = []
    dates_delivered_c = []

    for i in parcel_c:
        # Creation Date
        c = i.date_created
        dates_created_c.append(c)
        # Fetch Date
        f = i.date_fetched
        dates_fetched_c.append(f)
        # Dates Inhub
        h = i.date_inhub
        dates_inhub_c.append(h)
        # Dates In Transit
        t = i.date_intransit
        dates_intransit_c.append(t)
        # Dates Delivered
        d = i.date_delivered
        dates_delivered_c.append(d)

    created_c = dict()
    for date in dates_created_c:
        if date in created_c:
            created_c[date] += 1
        else:
            created_c[date] = 1

    fetched_c = dict()
    for date in dates_fetched_c:
        if date in fetched_c:
            fetched_c[date] += 1
        else:
            fetched_c[date] = 1

    inhub_c = dict()
    for date in dates_inhub_c:
        if date in inhub_c:
            inhub_c[date] += 1
        else:
            inhub_c[date] = 1

    transit_c = dict()
    for date in dates_intransit_c:
        if date in transit_c:
            transit_c[date] += 1
        else:
            transit_c[date] = 1

    delivered_c = dict()
    for date in dates_delivered_c:
        if date in delivered_c:
            delivered_c[date] += 1
        else:
            delivered_c[date] = 1

    overview_c = linegraph(x_data=list(created_c.keys()), y1=list(created_c.values()), y2=list(fetched_c.values()),
                         y3=list(inhub_c.values()), y4=list(transit_c.values()), y5=list(delivered_c.values()))

    # Pie Chart for Weight Distribution and Distance statistics
    total_c = Parcel.objects.filter(owner=client).count()
    # Weight statistics (if statement to avoid division by zero error)
    if total_c > 0:
        d1_c = (Parcel.objects.filter(weight__lt=5, owner=client)).count() / total_c
        d2_c = (Parcel.objects.filter(weight__range=(5, 10), owner=client)).count() / total_c
        d3_c = (Parcel.objects.filter(weight__range=(10, 20), owner=client)).count() / total_c
        d4_c = (Parcel.objects.filter(weight__range=(20, 30), owner=client)).count() / total_c
        d5_c = (Parcel.objects.filter(weight__range=(30, 50), owner=client)).count() / total_c
        d6_c = (Parcel.objects.filter(weight__gte=50, owner=client)).count() / total_c
        # Distance Statistics
        d7_c = (Parcel.objects.filter(distance__lt=500, owner=client)).count() / total_c
        d8_c = (Parcel.objects.filter(distance__gte=500, owner=client)).count() / total_c
    else:
        d1_c = 0
        d2_c = 0
        d3_c = 0
        d4_c = 0
        d5_c = 0
        d6_c = 0
        d7_c = 0
        d8_c = 0
    dist_charts_c = pie_chart(d1=d1_c, d2=d2_c, d3=d3_c, d4=d4_c, d5=d5_c, d6=d6_c, l1='< 5kg', l2='5kg < x < 10kg',
                            l3='10kg < x < 20kg', l4='20kg < x < 30kg', l5='30kg < x < 50kg', l6='> 50kg', d7=d7_c,
                            d8=d8_c, l7='Short Distance', l8='Long Distance')

    ###### DASHBOARD MANAGEMENT ######
    client_total_costs = Parcel.objects.filter(owner=client).aggregate(Sum('price')).get('price__sum', 0.00)
    client_costs_current = Parcel.objects.filter(date_created__month=month, date_created__year=year, owner=client).aggregate(
        Sum('price')).get('price__sum', 0.00)
    client_costs_previous = Parcel.objects.filter(date_created__month=previous_month, date_created__year=year, owner=client).aggregate(
        Sum('price')).get('price__sum', 0.00)


    context = {
        'current': current,
        'overview': overview,
        'stat_pie': dist_charts,
        'tot_costs': total_costs,
        'current_costs': costs_current,
        'previous_costs': costs_previous,
        'client_tot_costs': client_total_costs,
        'client_costs_current': client_costs_current,
        'client_costs_previous': client_costs_previous,
        'overview_c': overview_c,
        'current_c': current_c,
        'dist_charts_c': dist_charts_c,
    }
    return render(request, 'dashboard.html', context)

@login_required
@group_required('Driver', 'Warehouse Manager')
def driver_logbook_initial(request):
    city = Parcel.objects.all()
    template = 'logbook.html'
    user = request.user.employee
    city_parcel_inbound = Parcel.objects.filter(current_location__city__icontains=user.location.city,
                                                status='In Hub Inbound')
    city_parcel_outbound = Parcel.objects.filter(current_location__city__icontains=user.location.city,
                                                status='In Hub Outbound')
    office = Office.objects.all()
    term = request.GET.get('term')
    analytics = []

    for i in city:
        h = i.date_inhub
        analytics.append(h)

    hub = dict()
    for date in analytics:
        if date in hub:
            hub[date] += 1
        else:
            hub[date] = 1

    b_local = Parcel.objects.filter(current_location__city__icontains=user.location.city).aggregate(Sum('price')).get('price__sum', 0.00)
    b_total = Parcel.objects.all().aggregate(Sum('price')).get('price__sum', 0.00)

    l = linegraph_warehouse(x=list(hub.keys()), y=list(hub.values()), y_title='Sum of Parcels')
    b = barchart_warehouse(x_data=['Total Revenue', 'Local Revenue'], y_data=[b_total, b_local], name='')

    if term:
        city_filtered_fetch = city.filter(current_location__city__icontains=term, status='Created')
        city_filtered_hub = city.filter(current_location__city__icontains=term, status='In Hub Outbound')
        city_filtered_deliver = city.filter(current_location__city__icontains=term, status='In Transit')
        tpia = city.filter(current_location__city__icontains=term).count()
        term = term
        context = {
            'city_fetch': city_filtered_fetch,
            'city_hub': city_filtered_hub,
            'city_deliver': city_filtered_deliver,
            'total_parcels_in_area': tpia,
            'term': term,
        }
        return render(request, template, context)
    else:
        context = {
            'office_list': office,
            'city_inbound': city_parcel_inbound,
            'city_outbound': city_parcel_outbound,
            'parcel_traffic': l,
            'parcel_fin_measures_city': b
        }
        return render(request, template, context)