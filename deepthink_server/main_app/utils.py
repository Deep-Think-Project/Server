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
    print(json_output)

    output_path = os.path.join(settings.BASE_DIR, 'output', 'indexed', 'indexed_output.json')
    # 파일로 저장 (선택 사항)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_output)
    
    return json_output
        

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
        
        return text_without_line_breaks
    except requests.exceptions.RequestException as e:
        raise Exception(f"URL 요청 중 오류 발생: {e}")

def call_gpt_api(text):
    pass


        