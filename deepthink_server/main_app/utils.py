import re

import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4

import spacy # pip install spacy
import json

from django.conf import settings
import os

# check if the input is url or plain text
def input_type_check(input):
    """
    function to check if the input is URL or Plain Text
    
    Args:
        input (str): string to check
    
    Returns:
        str: "URL" or "Plain Text"
    """
    
    # extension list for image and other resources
    excluded_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']

    # exclude image and other resources
    lower_input = input.strip().lower()
    for ext in excluded_extensions:
        if lower_input.endswith(ext):
            raise Exception("URL이 이미지 또는 기타 리소스 파일로 끝납니다. URL을 확인해 주세요.")
    
    # URL pattern regex (including IP-based URL, TLD required)
    url_pattern = re.compile(
        r'^(https?:\/\/)?'  # http:// or https:// (optional)
        r'('  # domain name or IP address
        r'(([\da-zA-Z-]+)\.)+'  # subdomain (optional) and domain name
        r'([a-zA-Z]{2,})'  # TLD (required)
        r'|'  # OR operator to allow IP address
        r'((\d{1,3}\.){3}\d{1,3})'  # IPv4 address pattern
        r')'
        r'(:\d{1,5})?'  # port num (optional)
        r'(\/[\/\w .-]*)*'  # path (optional)
        r'(\?[\w=&%-]*)?'  # query string (optional)
        r'(#[\w-]*)?$',  # fragment (optional)
        re.IGNORECASE
    )
    
    if url_pattern.match(input.strip()):
        return "url"
    else:
        return "plain-text"

# text extraction without whitespace from (clean ver.)
def extract_text(url):
    try:
        # get HTML content from URL
        response = requests.get(url)
        response.raise_for_status()  # check status code
        
        # HTML parsing with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # extract text
        text = soup.get_text(separator="\n")
        
        # multiple line breaks are processed into one and unnecessary spaces are removed
        text_without_line_breaks = ' '.join(text.split())
        
        return text_without_line_breaks
    except requests.exceptions.RequestException as e:
        raise Exception(f"URL 요청 중 오류 발생: {e}")

# text extraction with whitespace (original ver.)
def extract_text_with_whitespace(url):
    # get HTML content from URL
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        # HTML parsing with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # extract text
        text = soup.get_text(separator="\n")
        return text
    else:
        raise Exception(f"URL 요청 실패, 상태 코드: {response.status_code}")
    
def indexing_text(article, input_type):
    # 한국어 모델 로드
    nlp = spacy.load("ko_core_news_sm")

    # spaCy로 문장 분리
    doc = nlp(article)
    sentences = [sent.text.strip() for sent in doc.sents]

    # 문장 수가 5개 이하인지 확인
    if len(sentences) <= 5 and input_type == "url":
        raise Exception("문장 수가 5개 이하입니다. 본문 텍스트를 복사하여 붙여넣어 주세요.")

    # JSON 포맷으로 변환
    indexed_sentences = {str(i): sentence for i, sentence in enumerate(sentences)}

    # JSON 문자열로 변환 (pretty print)
    json_output = json.dumps(indexed_sentences, ensure_ascii=False, indent=4) # python dict -> json str

    # 결과 출력
    # print(json_output)

    # 파일로 저장 (선택 사항)
    output_path = os.path.join(settings.BASE_DIR, 'output', '2-indexed')
    save_unique_file(output_path, 'indexed_output.json', json_output)

    return json_output

# text extraction used in main_app/views.py
def new_extract_text(url):
    try:
        # get HTML content from URL
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # check status code
        
        # BeautifulSoup HTML parsing
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # remove unnecessary tags
        for tag in soup(["script", "style", "meta", "header", "footer", "nav", "aside"]):
            tag.decompose()
        
        # extract article
        article = soup.find("article")
        if article:
            text = article.get_text(separator="\n", strip=True)
        else:
            # if no article tag, try to find by id or class
            content_div = soup.find("div", {"id": "content"}) or soup.find("div", {"class": "post"})
            if content_div:
                text = content_div.get_text(separator="\n", strip=True)
            else:
                # 위에서 찾지 못하면 전체 텍스트 가져오기
                text = soup.get_text(separator="\n", strip=True)
        
        # multiple line breaks are processed into one and unnecessary spaces are removed
        text_without_line_breaks = ' '.join(text.split())
        
        # save to file for debugging
        output_path = os.path.join(settings.BASE_DIR, 'output', '1-raw')
        save_unique_file(output_path, 'extracted_text.txt', text_without_line_breaks)
        
        return text_without_line_breaks
    except requests.exceptions.RequestException as e:
        raise Exception(f"URL 요청 중 오류 발생: {e}")

from openai import OpenAI
from dotenv import load_dotenv
import json

# call GPT API
def call_gpt_api(json_output):
    load_dotenv()

    # OpenAI API key setting
    client = OpenAI(
        api_key =  os.getenv("OPEN_API_KEY"),  # API key

    )
    
    # read system prompt from file
    SYSTEM_PROMPT_PATH = os.path.join(settings.BASE_DIR, 'main_app', 'system_prompt', 'gpt_system_prompt.txt')
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as file:
        system_prompt = file.read()

    response = client.responses.create(
    model="gpt-4o",
    input=[
        {
        "role": "system",
        "content": [
            {
                "type": "input_text",
                "text": system_prompt,
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "input_text",
            "text": json_output
            }
        ]
        },
    ],
    text={
        "format": {
        "type": "json_object"
        }
    },
    reasoning={},
    tools=[],
    temperature=1,
    max_output_tokens=8000,
    top_p=1,
    store=True
    )

    
    # save file with unique name for debugging
    output_path = os.path.join(settings.BASE_DIR, 'output', '3-first_gpt_output')
    save_unique_file(output_path, 'first_gpt_output.json', response.output_text)
    
    json_obj = json.loads(response.output_text) # str -> json
    
    print("[COMPLETE] GPT API")
    
    return json_obj # json

# save file with unique name for dubugging
def save_unique_file(directory: str, base_filename: str, content: str) -> str:
    """
    Creates and saves a file with a non-duplicate filename in the specified directory.

    Args:
    directory (str): The path to the directory where the file should be saved.

    base_filename (str): The base name of the file (e.g., 'hello.txt').

    content (str, optional): The content to write into the file. Defaults to "Hello, World!".

    Returns:
    str: The full path of the newly created file.
    """
    
    # print(type(content))

    base_name, ext = os.path.splitext(base_filename)
    count = 0

    while True:
        if count == 0:
            filename = base_filename
        else:
            filename = f"{base_name}{count}{ext}"
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return filepath
        count += 1

# extract ambiguous sentences from gpt output
def extract_ambiguous_sentences(json_data):
    """
    주어진 JSON 데이터에서 type이 'ambiguous_sentence'인 문장만 모아 새로운 JSON 형식으로 반환합니다.
    
    Args:
        data (dict): 원본 JSON 데이터
    
    Returns:
        dict: ambiguous_sentence만 포함된 새로운 JSON
    """
    ambiguous_sentences = [
        sentence for sentence in json_data.get("sentences", [])
        if sentence.get("type") == "ambiguous_sentence"
    ]

    result = {
        "ambiguous_sentences": ambiguous_sentences,
        # "count": len(ambiguous_sentences)
    }
    
    json_to_str = json.dumps(result, ensure_ascii=False, indent=2) # python dict -> json str
    
    output_path = os.path.join(settings.BASE_DIR, 'output', '4-for_sonar')
    save_unique_file(output_path, 'for_sonar.json', json_to_str)

    return result # python dict

# call sonar api
def call_sonar_api(python_dict):
    YOUR_API_KEY = os.getenv("SONAR_API_KEY")

    SYSTEM_PROMPT_PATH = os.path.join(settings.BASE_DIR, 'main_app', 'system_prompt', 'sonar_system_prompt.txt')
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as file:
        system_prompt = file.read()
    
    user_prompt_str = json.dumps(python_dict, ensure_ascii=False, indent=2) # python dict -> json str

    messages = [
        {
            "role": "system",
            "content": (
                system_prompt
                
            ),
        },
        {
            "role": "user",
            "content": user_prompt_str
        },
    ]


    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    # print(response)

    content = response.choices[0].message.content
    final_output = json.loads(content) # str -> json
    
    
    output_file_path = os.path.join(settings.BASE_DIR, 'output', '5-sonar_output')
    save_unique_file(output_file_path, 'sonar_output.json', content)

    print("[COMPLETE] SONAR API")

    return final_output # json

from typing import Dict, Any, List

# merge gpt output and sonar output
def merge_gpt_sonar(gpt_json: Dict[str, Any], sonar_json: List[Dict[str, Any]]) -> Dict[str, Any]:
    # convert sonar_json to dict for fast lookup by index
    sonar_dict = {item["index"]: item["results"] for item in sonar_json}

    for sentence in gpt_json["sentences"]:
        idx = sentence["index"]
        if idx in sonar_dict:
            sentence["references"] = sonar_dict[idx]
        else:
            sentence["references"] = []  

    # save file for debugging
    output_path = os.path.join(settings.BASE_DIR, 'output', '6-merge_gpt_sonar')
    save_unique_file(output_path, 'merged_output.json', json.dumps(gpt_json, ensure_ascii=False, indent=2))
    
    return gpt_json



import time

# timer thread for debugging
def timer_thread(start_time, stop_event):
    elapsed = 0
    while not stop_event.is_set():
        time.sleep(1)
        elapsed += 1
        print(f"[TIMER] Wait for {elapsed} seconds...")
