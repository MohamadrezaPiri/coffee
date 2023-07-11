from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.db.models import Count
from .models import Category, Items,Order, OrderDetail, Table
from .forms import OrderForm, OrderDetailForm

# Create your views here.

def menu(request):
    queryset = Category.objects.all()

    context = {
        'queryset': queryset
    }

    return TemplateResponse(request, 'shop/menu.html', context)


def order(request):
    if request.method == "POST":
      
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success')
    else:
        form = OrderForm()

    context = {
        "form": form
    }    

    return render(request, "shop/order.html", context)
    

def order_detail(request):
    queryset = Items.objects.all()
    orders = Order.objects.all()
    tables = Table.objects.all()
    free_tables = Table.objects.filter(is_free=True)

    if request.method == 'POST':
        data = request.POST.dict()
        table = request.POST.get('table')

        for item in queryset:
            order_key = 'order'
            quantity_key = 'quantity_' + str(item.id)

            order = data.get(order_key)
            quantity = int(data.get(quantity_key, 0))
            selected_table = Table.objects.get(name=table)

            if quantity > 0:
                (current_order, created) = Order.objects.get_or_create(table=selected_table,orderid=order)
                order_detail = OrderDetail.objects.create(quantity=quantity, order=current_order, item=item)
                selected_table.is_free = False
                selected_table.save()
                order_detail.save()
            else:
                continue

    return render(request, "shop/order_detail.html", {'queryset': queryset, 'orders': orders, 'tables': tables, 'free_tables': free_tables})
    

def open_orders(request):
    orders = Order.objects.all()
    order_details = OrderDetail.objects.all()
    items = Items.objects.all()

    context = {
        'orders': orders,
        'details': order_details,
        'items': items
    }

    return render(request, "shop/open_orders.html", context)


def open_order_detail(request, id):
    items = Items.objects.all()
    order = Order.objects.get(orderid = id)
    detailitems=Items.objects.filter(orderdetail__order=order)
    orderdetails = OrderDetail.objects.filter(order = order)

    if request.method == 'POST':
        data = request.POST.dict()

        for item in items:
            quantity_key = 'quantity_' + str(item.id)
            quantity = int(data.get(quantity_key, 0))

            if quantity > 0:
                new_order_detail = OrderDetail.objects.create(quantity=quantity, order=order, item=item)
                new_order_detail.save()
            else:
                continue    
            
    return render(request, "shop/open_order_detail.html", {'items': items, 'order': order, 'details': orderdetails, 'detailitems': detailitems})

