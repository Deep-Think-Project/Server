import re

from bs4 import BeautifulSoup # pip install beautifulsoup4

import json

from copy import deepcopy

# html 형태에서 본문 텍스트 추출
def extract_article_content(html):
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('article')
    
    # article 내의 직접적인 텍스트 노드만 추출
    text_nodes = []
    for node in article.contents:
        # 텍스트 노드이고 내용이 있는 경우
        if node.name is None and node.strip():  
            text_nodes.append(node.strip())

    # text_nodes를 문자열로 합치기
    text = ' '.join(text_nodes)

    # 텍스트 노드 결합 및 정리
    text = text.replace('\xa0', ' ').replace('&nbsp;', ' ')
    text = re.sub(r'\s+', ' ', text.replace('\n', ' '))
    text = text.strip()
    
    return text

# 기존 html 형태에서 영어 span 없애고 앞 뒤랑 합치기
def remove_english_spans(html):
    soup = BeautifulSoup(html, 'html.parser')
    for span in soup.find_all('span', {'data-type': 'ore', 'data-lang': 'en'}):
        text = span.get_text()
        span.replace_with(text)
    return str(soup)

# 최종 데이터를 html 형태로 가공
def make_final_output(article_html, final_ouput):
    # 데이터 준비
    sentences = deepcopy(final_ouput['sentences'])
    summary = final_ouput['results']['summary']
    author_intent = final_ouput['results']['author_intent']

    output_html = article_html

    for s in sentences:
        sentence_text = s['sentence'].strip()
        # 각 문장을 span으로 감싸는 태그 생성
        if s['type'] == 'clear_sentence':
            tag = f'<span class="deepthink-hl deepthink-type-claer" data-reason="{s["reason"]}">{sentence_text}</span>'
        else:
            tag = f'<span class="deepthink-hl deepthink-type-ambiguous" data-reason="{s["reason"]}"'
            if "other_interpretations" in s:
                tag += f' data-other_interp="{"||".join(s["other_interpretations"])}"'
            if "references" in s:
                tag += f" data-references='{json.dumps(s['references'], ensure_ascii=False)}'"
            tag += f'>{sentence_text}</span>'
        # 본문에서 해당 문장을 첫 번째로 만나는 부분만 span으로 치환
        output_html = output_html.replace(sentence_text, tag, 1)


    return {
        "article_html": output_html,
        "summary": summary,
        "author_intent": author_intent
    }