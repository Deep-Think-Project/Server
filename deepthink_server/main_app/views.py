from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .utils import input_type_check

@api_view(['POST'])
def home_view(request):
    if request.method == 'POST':
        request_data = request.data
        
        input_type = input_type_check(request_data.get('input'))
        
        # print(f'input type: {input_type}')

        response_data = {
            "input": request_data.get('input'),
            "type": input_type
        }
        
        return Response(response_data, status=status.HTTP_200_OK) 