import datetime


class Courier:
    courier_id = 0
    courier_type = "foot"
    regions = []
    working_hours = []
    load_copacity = 0

    def __init__(self, courier_id, courier_type, regions, working_hours):
        self.courier_id = courier_id
        self.regions = regions
        self.working_hours = working_hours
        self.courier_type = courier_type
        if courier_type == "foot":
            self.load_copacity = 10
        elif courier_type == "bike":
            self.load_copacity = 15
        else:
            self.load_copacity = 50

    # def assign(self):


class Orders:
    order_id = 0
    weight = 0
    region = 0
    delivery_hours = []

    def __init__(self, order_id, weight, region, delivery_hours):
        self.order_id = order_id
        self.weight = weight
        self.region = region
        self.delivery_hours = delivery_hours

    def __str__(self):
        return "Order_id:" + str(self.order_id) + " " + "Weight:" + str(self.weight)


def intersecting(working_hour, delivery_hour):
    interval_1 = working_hour.split("-")
    interval_2 = delivery_hour.split("-")

    # print(inter)
    # print(inter1)

    cour_start = datetime.datetime.strptime(interval_1[0], '%H:%M')
    cour_end = datetime.datetime.strptime(interval_1[1], '%H:%M')

    delivery_start = datetime.datetime.strptime(interval_2[0], '%H:%M')
    delivery_end = datetime.datetime.strptime(interval_2[1], '%H:%M')

    if (cour_start <= delivery_end <= cour_end) or (cour_start <= delivery_start <= cour_end) or (
            cour_start >= delivery_start and cour_end <= delivery_end):
        return True

    return False


def sort_order(o):
    return o.weight


def order_selection(courier, ordersList):  # ??
    orders_id = []

    for order in ordersList:
        for delivery_hour in order.delivery_hours:
            for working_hour in courier.working_hours:
                if intersecting(working_hour, delivery_hour):
                    if order not in orders_id:
                        orders_id.append(order)

    return sorted(orders_id, key=sort_order)


def assign(courier, order_list):
    order_list = order_selection(courier, order_list)

    orders_id = []
    summ = 0
    for order in order_list:

        if summ + order.weight <= courier.load_copacity:
            orders_id.append(order.order_id)
            summ += order.weight
    return orders_id


def get_orders_id(courier_fields, order_list_fields):
    courier = Courier(courier_fields[0], courier_fields[1], courier_fields[2], courier_fields[3])  # создаём курьера
    orders = []
    for order_fields in order_list_fields:
        # print(order_fields.order_id,order_fields.weight, order_fields.region,order_fields.delivery_hours)
        orders.append(
            Orders(order_fields.order_id, order_fields.weight, order_fields.region, eval(order_fields.delivery_hours)))
    return assign(courier, orders)


def orders_not_region(courier, orderList):
    orders_id = []
    for order in orderList:
        if order.region not in courier.regions:
            orders_id.append(order.order_id)
    return orders_id


def del_orders_not_region(courier_region, orderList):
    orders_id = orders_not_region(courier_region, orderList)
    orders = [x for x in orderList]
    for i in range(0, len(orders)):
        if orders[i].order_id in orders_id:
            orderList.remove(orders[i])
    return orders_id


def order_not_selection(courier, ordersList):  # ??
    orders_id = del_orders_not_region(courier, ordersList)
    order_id_norm = []
    for order in ordersList:
        for delivery_hour in order.delivery_hours:
            for working_hour in courier.working_hours:
                if intersecting(working_hour, delivery_hour):
                    if order not in order_id_norm:
                        order_id_norm.append(order.order_id)

    for order in ordersList:
        if order.order_id not in order_id_norm:
            if order.order_id not in orders_id:
                orders_id.append(order.order_id)

    return orders_id  # sorted(orders_id, key=sort_order)


def order_not_in_working_hour(courier, orderList):
    order_id = order_not_selection(courier, orderList)
    return order_id


def order_over_weight(courier, orderList):
    orders_id = order_not_in_working_hour(courier, orderList)
    summ = 0
    for order in orderList:
        if summ + order.weight > courier.load_copacity:
            orders_id.append(order.order_id)
        summ += order.weight
    return orders_id


def cancel_orders(courier_fields, order_list_fields):
    courier = Courier(courier_fields[0], courier_fields[1], courier_fields[2], courier_fields[3])  # создаём курьера
    orders = []
    print('cour_works:', courier.working_hours)
    for order_fields in order_list_fields:
        # print(order_fields.order_id,order_fields.weight, order_fields.region,order_fields.delivery_hours)
        orders.append(
            Orders(order_fields.order_id, order_fields.weight, order_fields.region, eval(order_fields.delivery_hours)))
    print('order 0', orders[0])
    return order_over_weight(courier, orders)

# print(assign(Courier(1, "foot", 1, ["11:00-13:00", "14:30-14:40", "21:00-22:00"]), orders))
