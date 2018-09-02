from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

    # def post(self, request, format=None):
    #     serializer = GoodsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


