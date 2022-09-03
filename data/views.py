from django.shortcuts import render, redirect
from .models import Data

def redirectview(request):
    return redirect('/stevner/page=1&show=10')

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

    context = {
        'search_string': search,
        'order': order_path,
        'search': path,
        'page': page,
        'show': show,
        'data_set': idx_data,
        }
    return render(request, 'table.html', context)


