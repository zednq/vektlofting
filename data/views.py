from django.shortcuts import render, redirect
from .models import Data

def redirectview(request):
    return redirect('/stevner/page=1&show=10')

def table(request, page=1, show=25, search='', order='lofter'):
    
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


