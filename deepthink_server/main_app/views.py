from django.shortcuts import render
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .utils import input_type_check, indexing_text, new_extract_text, call_gpt_api

import os


@api_view(['POST'])
def home_view(request):
    if request.method == 'POST':
        """
        {
            "input": "sentence" or "url"
        }
        """
        request_data = request.data
        
        input_text = request_data.get('input')
        
        try:
            input_type = input_type_check(request_data.get('input')) # Use input_type_check function to check the input type

            # print(f'input type: {input_type}') # Debugging
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if input_type == 'url':
            extracted_text = new_extract_text(request_data.get('input')) # url 에서 text 추출
            # print(f'extracted text: {extracted_text}')
            
            input_text = extracted_text

        try:
            json_output = indexing_text(input_text, input_type) # JSON 포맷 으로 변환
            final_output = call_gpt_api(json_output) # gpt api 호출
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            "type": input_type,
            "output": final_output
        }
        
        return Response(response_data, status=status.HTTP_200_OK) 
    
    
async def home_view_async(request):
    if request.method == 'POST':
        request_data = request.data
        
        input_type = input_type_check(request_data.get('input'))
        
        # print(f'input type: {input_type}')
        # gpt api
        
        response_data = {
            "input": request_data.get('input'),
            "type": input_type
        }
        
        return Response(response_data, status=status.HTTP_200_OK)