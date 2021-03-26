import json
from cerberus import Validator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist, Q

from DB.models import Courier, Value_coruier, Order
from DB.api_db import toDB, del_extra_orders

from .models import CouriersPostRequest, CourierItem, CourierUpdateRequest




@csrf_exempt
def index(request):
    # if request.method == 'GET':
    #     temp = CouriersPostRequest([CourierItem(1, 'foot', [1, 2, 3], ['hey1', 'hey2', 'hey3']), CourierItem(2, 'car', [3, 2, 1], ['hey4', 'hey5', 'hey6'])])
    #     return JsonResponse(CouriersPostRequest.Schema().dump(temp))

    if request.method == 'POST':

        validator = Validator()
        if validator.validate(json.loads(request.body), CouriersPostRequest):
            dict_json = json.loads(request.body)
            order_val = True  # для отображение ошибок ввода json
            err = {}  # для вывода ошибов при валидации конкретных позиций
            for courier in dict_json['data']:
                if not validator.validate(courier, CourierItem):
                    err[courier['courier_id']] = validator.errors
                    order_val = False
                elif Courier.objects.filter(courier_id=courier['courier_id']).exists(): #существует уже в БД
                    err[courier['courier_id']] = "already exists"
                    order_val = False
            if order_val:
                id_for_json = [{"id": x['courier_id']} for x in dict_json['data']]

                toDB(dict_json['data'])

                # print(CouriersIdsAP.Schema().dumps(CouriersIdsAP({'couriers':[{'id':3,'additionalProp1':{}}],'additionalProp1':{}})))

                return JsonResponse({"couriers": id_for_json}, status=201)

            else:
                return JsonResponse(
                    {"validation_error": {"couriers": [{"id": order, "error": err[order]} for order in err], }},
                    status=400)
        else:
            return JsonResponse({"validation_error": {"couriers": [{"id": 0}], "errors": {"error": validator.errors}}},
                                # cмысл выводить курьеров
                                status=400)



@csrf_exempt
def getCourier(request, id):
    if request.method == 'GET':
        try:
            el = Courier.objects.get(courier_id=id)  # 404

            # el['rating'] = 0  # расчитать
            # el['earnings'] = 0  # расчитать
            ###
            ###

            earnings = el.earnings

            jsn = {'courier_id': el.courier_id, 'courier_type': el.courier_type, 'regions': el.regions, #для вывода
                   'working_hours': el.working_hours,
                   'earnings': earnings
                   }

            ###
            temp = Value_coruier.objects.filter(courier_id=id).all() #извлекаем стат. данные
            if el.earnings!=0: #это значит, что выполнен хотя бы один заказ
                print("value",[i.sum_time/i.counts for i in temp if i.counts != 0])
                jsn['rating'] = (60*60 - min(min([i.sum_time/i.counts for i in temp if i.counts != 0]), 60*60))/(60*60)*5 #среднее значение по регионам
           #Какое среднее значение если в регионе не выполнено заказов

             #хранить в качестве столбца деньги
            #ЕСЛИ НЕТ РЕЙТИНГА, ТО ВЫВОДИТЬ НЕ НУЖНО

            return JsonResponse(jsn)
        except ObjectDoesNotExist:
            return JsonResponse("", status=404, safe=False)

    if request.method == 'PATCH':  # validator
        try:
            temp = json.loads(request.body)
            if Validator().validate(temp, CourierUpdateRequest):
                el = Courier.objects.get(courier_id=id)  # ищем по id. Исключение, если нет курьера
                if 'courier_type' in temp:
                    el.courier_type = temp['courier_type']
                if 'regions' in temp:
                    el.regions = temp['regions'].__str__()
                if 'working_hours' in temp:
                    el.working_hours = temp['working_hours'].__str__()
                #orders = update_orders()
                #extra_orders =
                if len(eval(el.orders))!=0:
                    del_extra_orders(el, el.orders)
                # ОБНОВИТЬ ЗАКАЗЫ
                # Обновить регионы в Value_courier

                el.save()
                return JsonResponse({'courier_id': el.courier_id})
            else:
                return JsonResponse("", status=400, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse("", status=404, safe=False)
