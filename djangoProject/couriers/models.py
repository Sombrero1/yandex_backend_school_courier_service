CourierItem = {
    'courier_id': {'type': 'integer',
                   'required': True,
                   'min' : 1
                   },
    'courier_type': {'type': 'string',
                     'required': True,
                     'allowed':['foot','bike','car']
                     },
    'regions': {'type': 'list',
                'schema': {'type': 'integer',
                           'required': True
                           },
                'required': True,
                'min' : 1
                },

    'working_hours': {'type': 'list',
                      'schema': {'type': 'string',  # datetime, проверка
                                 'regex': '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]',
                                 'required': True
                                 },

                      'required': True
                      }
}

CouriersPostRequest = {
    'data': {
        'type': 'list',
        'required': True
    },
}

CourierUpdateRequest = {
    'courier_type': {'type': 'string',
                     'allowed':['foot','bike','car']
                     },
    'regions': {'type': 'list',
                'schema': {'type': 'integer',
                           'required': True
                           },
                },

    'working_hours': {'type': 'list',
                      'schema': {'type': 'string',  # datetime, проверка
                                 'regex': '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]',
                                 'required': True
                                 },
                      }
}
# OrdersAssignPostRequest = {
#     'courier_id': {
#         'type':'integer',
#         'required': True
#     }
# }
#
#
# OrdersCompletePostRequest = {
#     'courier_id': {
#         'type':'integer'
#     },
#     'order_id': {
#         'type': 'integer'
#     },
#     'complete_time': {
#         'type': 'datetime'
#     },
#
# }


# @dataclass()
# class idtest:
#     id : int
#
# @dataclass()
# class CourierItem:
#     courier_id: int
#     courier_type: str
#     regions: List [int]
#     working_hours: List [str]
#
# @dataclass()
# class CouriersPostRequest:
#     data: List[CourierItem]
#
#     def encode(z):
#         if isinstance(z, {}):
#             return (z.real, z.imag)
#         else:
#             type_name = z.__class__.__name__
#             raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

#
# @dataclass()
# class CourierUpdateRequest:
#     courier_type: str
#     regions: List[int]
#     working_hours: List[str]
#
#
# # @dataclass()
# # class CouriersIds:
# #     couriers: List [idtest]#исправить
# #
#
#
# ##########
# @dataclass()
# class dict_for_dict_for_valid:
#     id: int
#     additionalProp1: dict
#
#
# @dataclass()
# class dict_for_valid:
#     couriers: List[dict_for_dict_for_valid]
#     additionalProp1: dict
#
#
# @dataclass()
# class CouriersIdsAP:
#     validation_error: dict_for_valid


##############

