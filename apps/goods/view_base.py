# -*- coding: utf-8 -*-#
__author__ = 'li'

from django.views.generic import View
from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        rows_p = Goods.objects.all()[:10]

        data = []
        # for row in rows_p:
        #     data.append({
        #         # "category": row.category,
        #         "name": row.name,
        #         "shop_price": row.shop_price,
        #         "add_time": row.add_time
        #     })

        # from django.forms.models import model_to_dict
        #
        # for row in rows_p:
        #     json_dict =  model_to_dict(row)
        #     data.append(json_dict)

        from django.http.response import HttpResponse,JsonResponse
        import json
        #
        # return HttpResponse(json.dumps(data),
        #                     content_type="application/json")

        from django.core import serializers

        data = serializers.serialize("json", rows_p)

        # return HttpResponse(data, content_type="application/json")
        return JsonResponse(json.loads(data), safe=False)

