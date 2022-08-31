from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirectview),
    path('stevner/page=<int:page>&show=<int:show>', views.table, name='index'),
    path('stevner/page=<int:page>&show=<int:show>/search=<search>', views.table, name='search'),
    path('stevner/page=<int:page>&show=<int:show>/order_by=<order>', views.table, name='search'),
    path('stevner/page=<int:page>&show=<int:show>/search=<search>/order_by=<order>', views.table, name='search'),
]
