import re

import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4

from django.conf import settings
import os

from common.utils import save_unique_file

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