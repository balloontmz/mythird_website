from rest_framework.views import APIView
from rest_framework.response import Response

from goods.models import Goods
from goods.serializers import GoodsSerializer


class GoodsListView(APIView):
    """
    List all goods, or create a new snippet.
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        goods_json = GoodsSerializer(goods, many=True)
        return Response(goods_json.data)


