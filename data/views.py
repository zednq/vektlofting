from django.shortcuts import render, redirect
from .check_duplicates import run_check
from .models import Data
import plotly.express as px
from plotly.offline import plot
import pandas as pd
from datetime import datetime

def redirectview(request):
    return redirect('/stevner/page=1&show=10')

def lifter(request, navn):
    data = Data.objects.filter(lofter__icontains=navn)


    fodt = data[0].fodt if data[0].fodt != 0 else 'ukjent'
    fornavn = navn.split(' ')[0]
    mx_yr = max([x.aar for x in data])
    mx_mn = max([x.mnd for x in data.filter(aar=mx_yr)])
    mx_dg = max([x.dag for x in data.filter(aar=mx_yr).filter(mnd=mx_mn)])
    
    sist_stevne = data.filter(aar=mx_yr, mnd=mx_mn, dag=mx_dg)[0].stevne
    sist_stevne_klubb = data.filter(aar=mx_yr, mnd=mx_mn, dag=mx_dg)[0].klubb
    sist_stevne_dato = f'{mx_dg}/{mx_mn}/{mx_yr}'
    
    poeng_aar = data.filter(sinclair=max(data.values_list('sinclair'))[0])[0].aar
    poeng_mnd = data.filter(sinclair=max(data.values_list('sinclair'))[0])[0].mnd
    poeng_dag = data.filter(sinclair=max(data.values_list('sinclair'))[0])[0].dag

    poeng_dato = f'{poeng_dag}/{poeng_mnd}/{poeng_aar}'

    sml_vekt = round(data.filter(sml=max(data.values_list('sml'))[0])[0].vekt, 1)


    with open('data/files/rankfile.txt', encoding='utf-8') as f:
        for each in f:
            if data[0].lofter == each.strip().split(',')[1]:
                rank = each.strip().split(',')[0]
                break

    person = {
        'stevne': sist_stevne,
        'stevnedato': sist_stevne_dato,
        'stevneklubb': sist_stevne_klubb,
        'fodt': fodt,
        'fornavn':fornavn,
        'vekt': sml_vekt,
        'poeng_dato':poeng_dato,
        'rank':rank,
        }

    beste = {
        'rykk': max(data.values_list('rykk'))[0],
        'stot': max(data.values_list('stot'))[0],
        'sml': max(data.values_list('sml'))[0],
        'sinclair': max(data.values_list('sinclair'))[0]
        }

    def tot_graph(data):

        # get dates
        dates = []
        dates_raw = []
        for each in data:
            d = f'{each.dag}/{each.mnd}/{each.aar}'
            dates_raw.append((each.aar, each.mnd, each.dag))
            date = datetime.strptime(d, '%d/%m/%Y')
            dates.append(date)

        dates.sort()
        dates_raw.sort()

        # get sml
        sml = []
        for dr in dates_raw:
            sml.append(data.filter(aar=dr[0], mnd=dr[1], dag=dr[2])[0].sml)
        
        fig = px.line(x=dates, y=sml, labels={'x': 'dato', 'y': 'sammenalgt'}, title='Sammenlagt over tid')
        return plot(fig, output_type='div')


    def sammensetning(data):

        # get dates
        dates = []
        dates_raw = []
        dates_test = []
        for each in data:
            d = f'{each.dag}/{each.mnd}/{each.aar}'
            dates_test.append(d)
            dates_raw.append((each.aar, each.mnd, each.dag))
            date = datetime.strptime(d, '%d/%m/%Y')
            dates.append(date)

        dates.sort()
        dates_raw.sort()

        # get rykk, stot
        rykk = []
        stot = []
        for dr in dates_raw:
            rykk.append(data.filter(aar=dr[0], mnd=dr[1], dag=dr[2])[0].rykk)
            stot.append(data.filter(aar=dr[0], mnd=dr[1], dag=dr[2])[0].stot)

        stats = [x for x in zip(dates_test, rykk, stot)]

        df = pd.DataFrame(stats, columns=['dato', 'rykk', 'stot'])

        fig = px.bar(df, 
                     x='dato', 
                     y=['rykk', 'stot'], 
                     labels={'value':'kg', 'variable':'ovelse'}, 
                     title='Sammensetning',
            )

        return plot(fig, output_type='div')



    context = {
        'beste': beste,
        'navn': navn,
        'data_set': data,
        'person': person,
        'graph': tot_graph(data),
        'graph1': sammensetning(data),
        }
    return render(request, 'lifter.html', context)

def table(request, page=1, show=25, search='', order='lofter'):

    path = ''
    def get_data_range(page, show, search, order):
        entries = show
        page_range = page - 1
        start = page_range * entries
        end = (page_range * entries) + entries

        if len(search) < 1:
            if order == 'fodt':
                data = Data.objects.filter(fodt__gte=1000).order_by(order)[start:end]
            else:
                data = Data.objects.all().order_by(order)[start:end]
        else:
            data = Data.objects.filter(lofter__icontains=search).order_by(order)[start:end]
        return data

    if page > 0:
        idx_data = get_data_range(page, show, search, order)
        if search != '':
            path = f'/search={search}'
        if order != 'lofter':
            order_path = f'/order_by={order}'
        if order == 'lofter':
            order_path = ''
    else:
        return redirect('/stevner/page=1&show=10')

    sort_dict = {
        "idx":'index',
        "lofter":'navn',
        "aar":'stevnedato (tidlig)',
        "-aar":'stevnedato (sent)',
        "fodt":'fodselsaar (tidlig)',
        "-fodt":'fodselsaar (sent)',
        "-rykk":'rykk (mest)',
        "rykk":'rykk (minst)',
        "-stot":'stot (mest)',
        "stot":'stot (minst)',
        "-sml":'sammenlagt (mest)',
        "sml":'sammenlagt (minst)',
        "-sinclair":'sinclair (mest)',
        "sinclair":'sinclair (minst)',
    }
    sort_string = sort_dict[order]

    context = {
        'sort_string':sort_string,
        'search_string': search,
        'order': order_path,
        'search': path,
        'page': page,
        'show': show,
        'data_set': idx_data,
        }
    return render(request, 'table.html', context)


