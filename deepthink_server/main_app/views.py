from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .utils import input_type_check, new_extract_text
from common.utils import indexing_text, call_gpt_api, extract_ambiguous_sentences, call_sonar_api, merge_gpt_sonar, timer_thread, call_gemini_api

import time
import threading
    
@api_view(['POST'])
def home_view(request):
    start_time = time.time()
    stop_event = threading.Event()

    # Start timer thread for debugging
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
                input_type = input_type_check(request_data.get('input')) # Check the input type

                # print(f'input type: {input_type}') # Debugging
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
            if input_type == 'url':
                extracted_text = new_extract_text(request_data.get('input')) # extract text from url
                # print(f'extracted text: {extracted_text}')
                
                input_text = extracted_text

            try:
                json_output = indexing_text(input_text) # change to JSON format
                first_gpt_output = call_gpt_api(json_output) # call gpt api
                output_for_sonar = extract_ambiguous_sentences(first_gpt_output) # extract ambiguous sentences from gpt output
                sonar_output = call_sonar_api(output_for_sonar) # call sonar api
                final_output = merge_gpt_sonar(first_gpt_output, sonar_output) # merge gpt and sonar output
                
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
            return Response(final_output, status=status.HTTP_200_OK)
    
    finally:
        # timer end & print total time
        stop_event.set()
        t.join()
        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        print(f"[DONE] Total time: {total_time}seconds")
    
@api_view(['POST'])
def gemini_view(request):
    start_time = time.time()
    stop_event = threading.Event()

    # Start timer thread for debugging
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
                input_type = input_type_check(request_data.get('input')) # Check the input type

                # print(f'input type: {input_type}') # Debugging
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
            if input_type == 'url':
                extracted_text = new_extract_text(request_data.get('input')) # extract text from url
                # print(f'extracted text: {extracted_text}')
                
                input_text = extracted_text

            try:
                json_output = indexing_text(input_text) # change to JSON format
                llm_output = call_gemini_api(json_output) # call gpt api
                output_for_sonar = extract_ambiguous_sentences(llm_output) # extract ambiguous sentences from gpt output
                return Response(output_for_sonar, status=status.HTTP_200_OK)
                sonar_output = call_sonar_api(output_for_sonar) # call sonar api
                final_output = merge_gpt_sonar(first_gpt_output, sonar_output) # merge gpt and sonar output
                
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
            return Response(final_output, status=status.HTTP_200_OK)
    
    finally:
        # timer end & print total time
        stop_event.set()
        t.join()
        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        print(f"[DONE] Total time: {total_time}seconds")