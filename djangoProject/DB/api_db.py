from datetime import  datetime
from django.db.models import Q
from DB.models import Courier, Value_coruier, Order
from orders.calc_orders import get_orders_id, cancel_orders




def toDB(couriers):
    # Courier.objects.all().delete()  ###!!!!!!!!Убрать!!!
    # Value_coruier.objects.all().delete()
    for courier in couriers:
        Courier(courier_id=courier['courier_id'],
                courier_type=courier["courier_type"],
                regions=courier['regions'],
                working_hours=courier['working_hours']).save()
        # Заполнить регионы
        for reg in courier['regions']:  # возможно есть смысл сделать внешний ключ
            Value_coruier(courier_id=courier['courier_id'], region=reg).save()
def toDBorders(orders):
    # Order.objects.all().delete()  ###!!!!!!!!Убрать!!!
    for order in orders:
        Order(order_id=order['order_id'],
              weight=order["weight"],
              region=order['region'],
              delivery_hours=order['delivery_hours']).save()


def assign_update_courier_order(el,right_orders):
    query_ords = Q()
    for ord_id in right_orders:
        query_ords.add(Q(order_id=ord_id), Q.OR)  # запрос для смены состояния у заказов (блокирока для других курьеров)
    temps = Order.objects.filter(query_ords).all()
    for temp in temps:
        temp.taken = True
        temp.save()
    el.orders = right_orders.__str__()  # ФЕЙКОВЫЙ orders, также нужно изменить состояния взятый заказов
    el.last_assign_courier_type = el.courier_type
    el.assign_time = datetime.now()
    el.last_time = datetime.now() # какой формат данных
    el.save()

def del_extra_orders(courier , orders_cor):
    query_ords = Q()
    for id in eval(orders_cor):
        query_ords.add(Q(order_id = id), Q.OR)
    orders_fields = Order.objects.filter(query_ords).all()

    a = eval(courier.orders) #массив заказов курьера

    query_ords_cancel = Q()
    for order_id_del in cancel_orders([courier.courier_id, courier.courier_type, eval(courier.regions),
                    eval(courier.working_hours)],orders_fields):#вставить метод
        a.remove(order_id_del)
        query_ords_cancel.add(Q(order_id=order_id_del),
                       Q.OR)  # запрос для смены состояния у заказов (блокирока для других курьеров
    temps = Order.objects.filter(query_ords_cancel).all()
    for temp in temps:#для отмены лишних заказов
            temp.taken = False
            temp.save()

    courier.orders = a.__str__() #сохраняем изменённый массив
    courier.save()

def assign_give_orders(el):
    query = Q()
    for reg in eval(el.regions):
        query.add(Q(region=reg, taken=False), Q.OR)  # формируем запрос по всем регионам курьера

    return get_orders_id([el.courier_id, el.courier_type, el.regions, eval(el.working_hours)],
                                 Order.objects.filter(query).all())  # el.regions не нужно


#для complete
def exist(courier_id):
    if Courier.objects.filter(courier_id=courier_id).exists():
        return True
    else:
        return False
#для complete
def hasOrder(courier_id, order_id):  # реализовать функцию декодер
    mass_orders = Courier.objects.get(courier_id=courier_id).orders
    if len(eval(mass_orders)) != 0 and order_id in eval(mass_orders):
            return True
    return False

def complete_order_update_data(dict_json, id):
    el = Courier.objects.get(courier_id=dict_json['courier_id'])  # получаем курьера для обновления last_time
    ord = Order.objects.get(order_id=id)  # чтобы узнать регион
    region = ord.region
      # удаляем выполненный заказ из бд

    # обновить среднее
    temp = Value_coruier.objects.get(courier_id=el.courier_id, region=region)

    try:
        act = datetime.strptime(dict_json['complete_time'], "%Y-%m-%dT%H:%M:%S.%fZ") #время доставки
    except ValueError:
        act = datetime.fromtimestamp(int(dict_json['complete_time']))
    last = el.last_time

    last.replace(microsecond=int(round(last.microsecond/1000000, 2)*100)) #округляем
    a = act - last

    temp.sum_time += a.total_seconds()
    temp.counts += 1
    temp.save()

    # Обновить Last_time
    el.last_time = act  # Обновить last time
    # Удалить компличенный заказ
    a = eval(el.orders)
    a.remove(id)
    el.orders = a.__str__()
    if len(a) == 0:  # ПРИ ВЫПОЛНЕНИИ РАЗВОЗА, считаем деньги
        C = {'foot': 2, 'bike': 5, 'car': 9}
        el.earnings += 500 * C[el.last_assign_courier_type]  # обнволяем деньги
    el.save()
    ord.delete()
    # ЕСЛИ ЗАВЕРШИЛИ ВСЕ ЗАКАЗЫ, ТО посчитать зп