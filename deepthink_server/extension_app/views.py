from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .utils import extract_article_content, remove_english_spans, make_final_output
from common.utils import indexing_text, call_gpt_api, extract_ambiguous_sentences, call_sonar_api, merge_gpt_sonar, timer_thread, call_gemini_api

import time
import threading

@api_view(['POST'])
def extension_view(request):
    start_time = time.time()
    stop_event = threading.Event()

    # Start timer thread for debugging
    t = threading.Thread(target=timer_thread, args=(start_time, stop_event))
    t.start()

    try:
        if request.method == 'POST':
            """
            {
                "html": 
                    <article id="dic_area" ...>
                        <!-- 실제 html 코드 전체가 여기 -->
                    </article>
            }
            """
            
            try:
                article_html = remove_english_spans(request.data.get('html')) # remove english span from html
                extracted_text = extract_article_content(article_html) # extract article content text from html
                json_output = indexing_text(extracted_text) # change to JSON format
                first_gpt_output = call_gpt_api(json_output) # call gpt api
                output_for_sonar = extract_ambiguous_sentences(first_gpt_output) # extract ambiguous sentences from gpt output
                sonar_output = call_sonar_api(output_for_sonar) # call sonar api
                final_output = merge_gpt_sonar(first_gpt_output, sonar_output) # merge gpt and sonar output
                result = make_final_output(article_html, final_output) # change to HTML format
                
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
            return Response(result, status=status.HTTP_200_OK)
    
    finally:
        # timer end & print total time
        stop_event.set()
        t.join()
        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        print(f"[DONE] Total time: {total_time}seconds")
    