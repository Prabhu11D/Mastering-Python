from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import datetime
import json
from .utils import cookieCart, cartData, guestOrder


def store(request):
    data = cartData(request)
    cart_items = data["cart_items"]

    products = Product.objects.all()
    context = {"products": products, 'cart_items': cart_items}
    return render(request, "store/store.html", context)


def cart(request):
    data = cartData(request)

    cart_items = data["cart_items"]
    items = data["items"]
    order = data["order"]

    context = {"items": items, "order": order, 'cart_items': cart_items}
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cartData(request)
    cart_items = data["cart_items"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, 'cart_items': cart_items}
    return render(request, "store/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    product_id = data["productId"]
    action = data["action"]
    print(f"Product ID {product_id}\nAction {action}")

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == "add":
        order_item.quantity += 1
    elif action == "remove":
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse("Item was added", safe=False)


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True

    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment Submitted', safe=False)
