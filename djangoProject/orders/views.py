import json
from django.http import JsonResponse
from cerberus import Validator
from django.views.decorators.csrf import csrf_exempt

from DB.api_db import assign_give_orders, complete_order_update_data, exist, hasOrder, \
    assign_update_courier_order, toDBorders
from DB.models import Courier, Order
from orders.models import OrdersPostRequest, OrderItemSchema, OrdersAssignPostRequest, \
    OrdersCompletePostRequest


@csrf_exempt
def index(request):  # починить вывод ошибок
    if request.method == 'POST':
        validator = Validator()
        if validator.validate(json.loads(request.body), OrdersPostRequest):  # Обработать ошибку ввода неверного списка
            print(json.loads(request.body)['data'][0])

            order_val = True
            err = {}
            for order in json.loads(request.body)['data']:
                if not validator.validate(order, OrderItemSchema):
                    err[order['order_id']] = validator.errors
                    order_val = False
                elif Order.objects.filter(order_id=order['order_id']).exists(): #существует уже в БД
                    err[order['order_id']] = "already exists"
                    order_val = False

            if order_val:
                toDBorders(json.loads(request.body)['data'])

                id_for_json = [{"id": x['order_id']} for x in json.loads(request.body)['data']]
                return JsonResponse({'orders': id_for_json}, status=201)
            else:
                print([{"id": order, "additionalProp1": err[order]} for order in err])
                return JsonResponse(
                    {"validation_error": {"orders": [{"id": order, "error": err[order]} for order in err], }},
                    status=400)
        else:
            return JsonResponse(
                {"validation_error": {"orders": [{"id": 0}], "additionalProp1": {"error": validator.errors}}},
                status=400)  # ТОЧНО ЛИ НУЖНО ПРОВЕРЯТЬ DATA
    return


@csrf_exempt
def assign(request):
    if request.method == 'POST':
        validator = Validator()
        dict_json = json.loads(request.body)
        if validator.validate(dict_json, OrdersAssignPostRequest) and exist(
                dict_json['courier_id']):  # ИДЕМПОТЕНТНОСТЬ!
            id_for_json = []

            el = Courier.objects.get(
                courier_id=dict_json['courier_id'])  # ЕСЛИ ЕСТЬ  ORDERS - возвращаем одно, нет - создаём
            # mass_orders = el.orders  # ЕСЛИ ЕСТЬ  ORDERS - возвращаем одно, нет - создаём
            # ЕСЛИ ЕСТЬ  ORDERS - возвращаем одно, нет - создаём
            if len(eval(el.orders)) == 0:  # нет заказов - даём задания

                right_orders = assign_give_orders(el)  # назначить курьеру заказы

                if len(right_orders) != 0:  # если нашли заказы
                    assign_update_courier_order(el, right_orders)  # меняем состояния заказов, добавляем курьеру и т.д.
                else:
                    return JsonResponse({'orders': [{"id": id} for id in
                                                    id_for_json]})  # если не нашлось заказа, то просто пустой order
            id_for_json = eval(el.orders)
            assign_time = el.assign_time

            # ЕСЛИ НЕ НАШЛОСЬ ЗАКАЗОВ, ТО assign_time не возвращать

            return JsonResponse({'orders': [{"id": id} for id in id_for_json],
                                 'assign_time': assign_time.
                                strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4] + 'Z'})
    return JsonResponse("", status=400, safe=False)


@csrf_exempt
def complete(request):
    if request.method == 'POST':
        validator = Validator()
        dict_json = json.loads(request.body)
        id = dict_json['order_id']
        if validator.validate(dict_json, OrdersCompletePostRequest) and exist(dict_json['courier_id']) \
                and hasOrder(dict_json['courier_id'], dict_json['order_id']):
            # Если есть заказ - возвращаем предыдущий ответ
            # КУРЬЕР МОЖЕТ ЗАВЕРШИТЬ НЕ СВОЙ ЗАКАЗ
            complete_order_update_data(dict_json, id)

            return JsonResponse({"order_id": id})
        else:
            return JsonResponse("", status=400, safe=False)
    return
