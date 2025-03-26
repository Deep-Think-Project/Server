import re

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