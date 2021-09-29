# -*- coding: utf-8 -*-

from django.contrib.admin.templatetags.admin_list import *

# @register.inclusion_tag("admin/change_list_results.html")
# def result_list(cl):
#     """
#     Display the headers and data list together.
#     """
#     headers = list(result_headers(cl))
#     #--------------------
#     # etiquetas = cl.model_admin.list_etiquetas
#     if hasattr(cl, 'list_etiquetas'):
#         if cl.list_etiquetas:
#             etiquetas = cl.list_etiquetas
#             for i, campo in enumerate(cl.list_display):
#                 if campo in etiquetas.keys():
#                     headers[i]['text'] = etiquetas[campo]
#     #-------------------------------        
#     num_sorted_fields = 0
#     for h in headers:
#         if h['sortable'] and h['sorted']:
#             num_sorted_fields += 1
#     return {'cl': cl,
#             'result_hidden_fields': list(result_hidden_fields(cl)),
#             'result_headers': headers,
#             'num_sorted_fields': num_sorted_fields,
#             'results': list(results(cl))}


def result_list(cl):
    """
    Display the headers and data list together.
    """
    headers = list(result_headers(cl))
    #--------------------
    # etiquetas = cl.model_admin.list_etiquetas
    if hasattr(cl, 'list_etiquetas'):
        if cl.list_etiquetas:
            etiquetas = cl.list_etiquetas
            for i, campo in enumerate(cl.list_display):
                if campo in etiquetas.keys():
                    headers[i]['text'] = etiquetas[campo]
    #-------------------------------        
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {
        'cl': cl,
        'result_hidden_fields': list(result_hidden_fields(cl)),
        'result_headers': headers,
        'num_sorted_fields': num_sorted_fields,
        'results': list(results(cl)),
    }