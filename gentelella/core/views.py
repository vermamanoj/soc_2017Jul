import json
import os
from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.plotting import figure
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from . import qradar_auth
from django import forms
from django.utils import timezone
from gentelella.core.forms import CustomerInfoForm


#@login_required(login_url='/login/')

def customerinfo(request):
    if request.method == "POST":
        form = CustomerInfoForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')

    else:

        form = CustomerInfoForm()
        return render(request, "customer_onboard.html", {'form': form})

def index(request):
    print(request)
    return render(request, 'c3_dashboard.html')

def qo(request, *arg):
    if arg:
        response = qradar_auth.q_auth(arg[0])
        data = response
        return render(request, 'qradar_offense_details.html', {'data1': data})
    else:
        response = qradar_auth.q_auth()
        print(response)
        if response == "qradar_config_does_not_exists":
            return redirect('/qradar_connect/')
        data = response
        return render(request, 'qradar_offense.html', {'data': data})

def qradar_offesnes(request):
    response = qradar_auth.qradar_offense_summary()
    print("QRadar_Offense_summary")
    #response = {"open":10,"close":5}
    print(response)
    #return render(request, 'qradar_dashboard.html',{'qradar_offense': response} )
    return JsonResponse({'qradar_offense':response})

def qradar_dashboard(request):
    response = qradar_auth.qradar_offense_summary()
    print("QRadar_Offense_summary")
    #response = {"open":10,"close":5}
    print(response)
    return render(request, 'qradar_dashboard.html',{'qradar_offense': response} )
    #return HttpResponse({'qradar_offense':response},content_type='text/html')

def plugins(request):
    response = ''

    return render(request, 'plugins.html', {'qradar_offense': response})

def qradar_connect(request):
    qradar_config_exists = 0
    if os.path.exists(r'config/config.ini'):
        with open(r'config/config.ini') as f:
            config = f.read()
            if len(config) > 0:
                qradar_config = json.loads(config)
                if 'qradar' in qradar_config.keys():
                    d1 = qradar_config['qradar']
                    qradar_config_exists = 1
                    return render(request, 'qradar/qradar_connector.html', {"data": d1})
    if qradar_config_exists==0:
        if request.POST:
            qradar_config = {"qradar":{
                     "host":request.POST['host'],
                    "username":request.POST['username'],
                    "password":request.POST['password']
                    }
                }
            with open(r'./config/config.ini', 'w') as f:
                f.write(json.dumps(qradar_config,indent=4))
            return redirect('/qradar_connect')
        return render(request, 'qradar/qradar_connector.html')





def c3_dashboard(request):
    print(request)
    return render(request, 'c3_dashboard.html')

def ir_playbook_1(request):
    return render(request, 'IR_playbook_1.htm')


def ir_playbook_2(request):
    return render(request, 'ir_playbook_2.html')

def qradar(request):
    return render(request, 'qradar.html' )

def bokeh(request):
    x = [1, 3, 5, 7, 9, 11, 13]
    y = [1, 10, 3, -6, 5, 6, 7]
    title = 'y = f(x)'

    hover = HoverTool(tooltips=[
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("title", "@title"),
    ])

    plot = figure(title=title,
                  x_axis_label='X-Axis',
                  y_axis_label='Y-Axis',
                  plot_width=400,
                  plot_height=400,
                  tools=[hover])

    plot.line(x, y, legend='f(x)', line_width=2)
    plot.toolbar_location=None
    # Store components
    script, div = components(plot)
    print(script)
    print(div)

    # Feed them to the Django template.

    # return render_to_response('bokeh_chart.html', {'script': script, 'div': div} )
    return render(request, 'bokeh_chart2.html')


def bokeh_json(request):
    from bokeh.plotting import figure
    from bokeh.embed import components

    plot = figure()
    plot.circle([1, 2], [3, 4])

    script, div = components(plot)
    result = {
        "outcome": "success",
        "success": {
            "div": div,
            "script": script,
        }
    }
    return JsonResponse(result)

def customer_setting(request):
    response = ''
    return render(request, 'customer_setting.html')

# Cookie test
def cookies_test(request):
    print(request.session.get('has_commented'))
    #if request.session.get('has_commented', False):
    #   return HttpResponse("You've already commented.")

    request.session['has_commented'] = True
    print(request.session.get('value'))
    request.session['value'] = request.session.get('value',98765432100)/10

    return JsonResponse({"data":request.session['value']})