import re

import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4

import spacy # pip install spacy
import json

from django.conf import settings
import os

def input_type_check(input):
    """
    입력된 문자열이 URL인지 Plain Text인지 판별하는 함수
    
    Args:
        input (str): 검사할 입력 문자열
    
    Returns:
        str: "URL" 또는 "Plain Text"
    """
    
    # URL 패턴 정규표현식 (IP 기반 URL 포함, TLD 필수)
    url_pattern = re.compile(
        r'^(https?:\/\/)?'  # http:// 또는 https:// (선택적)
        r'('  # 도메인 또는 IP 주소
        r'(([\da-zA-Z-]+)\.)+'  # 서브도메인 + 도메인 이름
        r'([a-zA-Z]{2,})'  # 최상위 도메인 (TLD: com, net, org 등 필수)
        r'|'  # OR 연산자로 IP 주소 허용
        r'((\d{1,3}\.){3}\d{1,3})'  # IPv4 주소 패턴
        r')'
        r'(:\d{1,5})?'  # 포트 번호 (선택적)
        r'(\/[\/\w .-]*)*'  # 경로 (선택적)
        r'(\?[\w=&%-]*)?'  # 쿼리 문자열 (선택적)
        r'(#[\w-]*)?$',  # 프래그먼트 (선택적)
        re.IGNORECASE
    )
    
    if url_pattern.match(input.strip()):
        return "url"
    else:
        return "plain-text"

# text extraction without whitespace from (clean ver.)
def extract_text(url):
    try:
        # URL로부터 HTML 콘텐츠 가져오기
        response = requests.get(url)
        response.raise_for_status()  # 상태 코드가 200이 아닐 경우 예외 발생
        
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 전체 텍스트 추출
        text = soup.get_text(separator="\n")
        
        # 여러 줄 바꿈을 하나로 처리하고 불필요한 공백을 제거
        text_without_line_breaks = ' '.join(text.split())
        
        return text_without_line_breaks
    except requests.exceptions.RequestException as e:
        raise Exception(f"URL 요청 중 오류 발생: {e}")

#text extraction with whitespace (original ver.)
def extract_text_with_whitespace(url):
    # URL로부터 HTML 콘텐츠 가져오기
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        # BeautifulSoup을 사용하여 HTML 문서를 파싱
        soup = BeautifulSoup(html_content, 'html.parser')
        # 전체 텍스트를 추출
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
    json_output = json.dumps(indexed_sentences, ensure_ascii=False, indent=4)

    # 결과 출력
    # print(json_output)

    # 파일로 저장 (선택 사항)
    output_path = os.path.join(settings.BASE_DIR, 'output', '2-indexed')
    save_unique_file(output_path, 'indexed_output.json', json_output)

    return json_output

# text extraction from @hanwooo  
def new_extract_text(url):
    try:
        # URL로부터 HTML 가져오기
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # 상태 코드 확인
        
        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 불필요한 태그 제거
        for tag in soup(["script", "style", "meta", "header", "footer", "nav", "aside"]):
            tag.decompose()
        
        # 본문 추출 (article 태그 우선)
        article = soup.find("article")
        if article:
            text = article.get_text(separator="\n", strip=True)
        else:
            # article이 없으면 id 또는 class를 기반으로 본문 탐색
            content_div = soup.find("div", {"id": "content"}) or soup.find("div", {"class": "post"})
            if content_div:
                text = content_div.get_text(separator="\n", strip=True)
            else:
                # 위에서 찾지 못하면 전체 텍스트 가져오기
                text = soup.get_text(separator="\n", strip=True)
        
        # 여러 줄 바꿈을 하나로 처리하고 불필요한 공백 제거
        text_without_line_breaks = ' '.join(text.split())
        
        # 결과 파일 저장
        output_path = os.path.join(settings.BASE_DIR, 'output', '1-raw')
        save_unique_file(output_path, 'extracted_text.txt', text_without_line_breaks)
        
        return text_without_line_breaks
    except requests.exceptions.RequestException as e:
        raise Exception(f"URL 요청 중 오류 발생: {e}")

from openai import OpenAI
from dotenv import load_dotenv
import json

def call_gpt_api(json_output):
    load_dotenv()

    # OpenAI API 키 설정
    client = OpenAI(
        # This is the default and can be omitted
        api_key =  os.getenv("OPEN_API_KEY"),  # 여기에 실제 API 키를 입력하세요

    )

    response = client.responses.create(
    model="gpt-4o",
    input=[
        {
        "role": "system",
        "content": [
            {
            "type": "input_text",
            "text": "Analyze each sentence according to the provided criteria to classify sentences as \"clear_sentence\" or \"ambiguous_sentence.\" Summarize the input text and determine the author's intent. If the input sentence is in Korean, provide both in Korean.\n\n# Sentence Judgment Rules\n\n## clear_sentence:\n- Based on verifiable evidence.\n- Free from emotional, figurative, or ambiguous language.\n- Logically sound and contextually appropriate.\n- Distinguishes clearly between facts and opinions.\n\n→ If a sentence meets all the above criteria, classify it as `clear_sentence`.\n\n## ambiguous_sentence:\nClassify as `ambiguous_sentence` if any of the following are detected:\n\n- Hidden motives or socio-political bias.\n- Metaphor, implication, or vague expressions.\n- Exaggeration or understatement.\n- Mixing facts with subjective opinions.\n- Emotional tone or ideological slant.\n- Omissions or selective presentations.\n- Multiple interpretations or logical fallacies.\n- Context mismatch or inconsistency.\n\n→ For `ambiguous_sentence`, include:\n- `\"reason\"`: Explain why it's classified this way, using a variety of creative, non-repetitive expressions, focusing on **Sentence Judgment Rules**.\n- `\"other_interpretations\"`: Suggest in Korean how this could be differently interpreted based on ideological perspective, interests, or contextual criticism, inducing critical thinking.\n\n→ Remove sentences that are not part of the news body text, such as those containing \"(사진=AP, ~~ 뉴스).\"\n\n# Steps\n\n1. Analyze each sentence using the criteria above.\n2. Classify sentences as \"clear_sentence\" or \"ambiguous_sentence.\"\n3. For \"ambiguous_sentence,\" provide reasons and other interpretations, ensuring Korean translations if applicable.\n4. Count the total of each type.\n5. Summarize the entire input text in 4-5 lines, focusing on core keywords.\n6. Analyze the author's intent, distinguishing between the main and subarguments. Ensure Korean translations if applicable.\n7. Remove sentences not considered as part of the news body if they match specific patterns like \"(사진=AP, ~~ 뉴스).\"\n\n# Output Format\n\nGenerate a JSON object with:\n\n- A list of sentence objects with `index`, `sentence`, `type`, and for ambiguous sentences, additional `reason` and `other_interpretations`.\n- A results object with totals, a summary, and author's intent.\n\n# Examples\n\n**Example Start**\n\n**Input JSON:**\n```json\n{\n \"0\": \"나는 매일 아침 7시에 일어난다.\",\n \"1\": \"그는 빛을 보았다.\",\n \"2\": \"이 정책은 경제 성장에 기여할 것이다.\"\n}\n```\n\n**Output JSON:**\n```json\n{\n  \"sentences\": [\n    {\n      \"index\": 0,\n      \"sentence\": \"나는 매일 아침 7시에 일어난다.\",\n      \"type\": \"clear_sentence\"\n    },\n    {\n      \"index\": 1,\n      \"sentence\": \"그는 빛을 보았다.\",\n      \"type\": \"ambiguous_sentence\",\n      \"reason\": \"단어 '빛'은 빛 또는 통찰력으로 해석될 수 있습니다.\",\n      \"other_interpretations\": [\"빛을 실제로 보았다\", \"통찰력을 얻었다\"]\n    },\n    {\n      \"index\": 2,\n      \"sentence\": \"이 정책은 경제 성장에 기여할 것이다.\",\n      \"type\": \"ambiguous_sentence\",\n      \"reason\": \"정책의 구체적인 내용이 명확하지 않아 다양한 해석이 가능합니다.\",\n      \"other_interpretations\": [\"경제 성장에 기여하지 않을 수 있음\"]\n    }\n  ],\n  \"results\": {\n    \"clear_sentence\": 1,\n    \"ambiguous_sentence\": 2,\n    \"summary\": \"텍스트는 일상적인 아침 루틴, 통찰의 가능성이 있는 시각적 경험, 그리고 경제 성장에 영향을 미칠 정책을 논의합니다.\",\n    \"author_intent\": \"저자는 일상을 설명하고, 경험을 전달하며, 경제적 함의를 제시하려고 합니다.\"\n  }\n}\n```\n\n**Example End**\n\n# Notes\n\n- Assume JSON formatted inputs.\n- Follow the output JSON structure exactly."
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
    max_output_tokens=5000,
    top_p=1,
    store=True
    )

    # print(response.output_text)
    
    # save file
    output_path = os.path.join(settings.BASE_DIR, 'output', '3-final_output')
    save_unique_file(output_path, 'final_output.json', response.output_text)
    
    json_obj = json.loads(response.output_text)
    
    return json_obj

def save_unique_file(directory: str, base_filename: str, content: str) -> str:
    """
    주어진 디렉토리에 중복되지 않는 파일명을 생성하여 저장한다.
    예: base_filename='hello.txt' -> hello.txt, hello1.txt, hello2.txt ...

    Parameters:
        directory (str): 파일을 저장할 디렉토리 경로
        base_filename (str): 기본 파일 이름 (예: 'hello.txt')
        content (str): 파일에 저장할 내용. 기본값은 "Hello, World!"

    Returns:
        str: 생성된 파일의 전체 경로
    """

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

