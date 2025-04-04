from django.shortcuts import render
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .utils import input_type_check, indexing_text, new_extract_text, call_gpt_api, extract_ambiguous_sentences, call_sonar_api, merge_gpt_sonar, timer_thread

import os

import time
import threading

'''
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
            first_gpt_output = call_gpt_api(json_output) # gpt api 호출
            output_for_sonar = extract_ambiguous_sentences(first_gpt_output) # first_gpt_output  = python dict
            sonar_output = call_sonar_api(output_for_sonar)
            final_output = merge_gpt_sonar(first_gpt_output, sonar_output)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            "type": input_type,
            "output": final_output
        }
        
        return Response(response_data, status=status.HTTP_200_OK) 
'''  
    
@api_view(['POST'])
def home_view(request):
    start_time = time.time()
    stop_event = threading.Event()

    # 타이머 쓰레드 시작
    t = threading.Thread(target=timer_thread, args=(start_time, stop_event))
    t.start()

    try:
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
                first_gpt_output = call_gpt_api(json_output) # gpt api 호출
                output_for_sonar = extract_ambiguous_sentences(first_gpt_output) # first_gpt_output  = python dict
                sonar_output = call_sonar_api(output_for_sonar)
                final_output = merge_gpt_sonar(first_gpt_output, sonar_output)
                
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
            return Response(final_output, status=status.HTTP_200_OK)
    
    finally:
        # 타이머 종료 및 총 소요 시간 출력
        stop_event.set()
        t.join()
        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        print(f"[DONE] 걸린시간: {total_time}초")
    
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