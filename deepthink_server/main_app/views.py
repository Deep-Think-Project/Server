from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
# @method_decorator(csrf_exempt, name='dispatch')
class TempClassView(APIView):
    # permission_classes = [AllowAny]
    
    def get(self, request):
        print(request.data)
        return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)