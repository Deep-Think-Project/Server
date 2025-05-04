import json
test = """
```json
[
  {
    "index": 3,
    "results": [
      {
        "source_title": "식물 키우는 것을 좋아하는 이유, 좋아하지 않는 이유를 챗GPT에 물었다. - 네이버 블로그",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAItQ_IzqEvTmfN1R9Qosxp9GkeBGDN0req32qAh3sz-P4KQtBIwV0DhuJeW3iZFCaz1lO9-7kTYEIzel2UgD8ziXPmyAxIfd4HMCfeAa84EM8Yb9jZEGvrDtQehoo6ziB9bYulyDA=="
      },
      {
        "source_title": "반려식물과 함께하는 특별한 성장 경험해볼까 - 한겨레",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAIwVsOVtGXW5Qj3WoErm898vPhS6lvxF-iRuvYJICUBtLF1O14vwTPTZPPU7eY6-W_t5_4G99l4BglhY_WFUw2DH7EQ5ZXz7L4ysIFzb2p7GVY3m0516ymF00_xiYFJSjxUak7PyE19dIBp1FBGOw=="
      },
      {
        "source_title": "올리야드 소개",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAL2Q0WussQwEMykDtPxPrkIvbvMUY1wzw16ohCEkOcW7_D23w1ces00YXVeNXeVPuw2J9ERFbuWBj3CelQ3xfSpes6YD7Yh-v5N6k39qdsGIHuBH9VAM3wk"
      },
      {
        "source_title": "식물생활 참고서적 및 자료 - 브런치스토리",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAKGh0_fuei2fg2JE_oVcBasvmTq7ZytlsJI2BEm5D5islktK_MXkAZZJJzxUlM_pfO2ooU0GdOBgXxQJLNlqa9EVmXKYy2iWa8ueqM3zGhbzneAk6C3"
      }
    ]
  },
  {
    "index": 5,
    "results": [
      {
        "source_title": "차세대 식물생산 방식 '수직농장'...기자재·제어관리 기술과 동반성장 - 영농자재신문",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAKeZbdKkuqm4_vw7HzSTa8UrGIF03SbHJbZqTzm8LWERfmjJYJN5AMjllTFWfJJoqQstOUQuRnbeLucVU5cMQoqg6icjMi7-KIhJpZ0Q77E6OxJ8Qm5PlAU9B6LZORk2C3v6leY"
      },
      {
        "source_title": "탄소중립 시대 도시농업 정책 동향 및 국내·외 사례 분석 | 보도자료 - 국토연구원",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqALKHM8YlUHcRfx2o60hAE6czpr5GNtlXjAS3iCVJkC3xlNLSTjSaS_rJBUwjTMD6u_Hu2zIbfGDe0zm0JNoa7kIvZ6TNn3pTuz-55QDl0pzQpVlQ9EnjWHmTfbiBIqWZx4T2VzHXmap-HfsddqN-yknxRamYOTLhHNpl33nqWV47LjJv2HBw1-Y"
      },
      {
        "source_title": "수직 농업: 도시 농업의 미래 - Editverse",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAKpMlvTyVCl5EML3gCta_zS_oa68WICYZIuK3j6GcjwqSlBlw4Yyf_nb68KNAmWfRLVDQEHxzO8nxwg3GaXJ2UDHwlQ7Q35QpG6iGInWTg8IA-rpfA7wwv8LgW2wvEetlgp-lOvMtAeMwJWVlpBTQC0GiCJpip4dqvTK_oC7IXMK5tkb9MxKkKFlKkzW473QKq5ZA4dmq7b7Nl4CivisSxDosoM4l0C0S61OctkSLsk_fKR-XFdIymc_0l6M8Q=="
      },
      {
        "source_title": "도시농업의 트렌드 변화와 서울시의 전략",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAJC5tZZtABdn-oYJyYZHkHQ1LzeYntSpHtcvx7d3mhQtDgR82JudOt--uOcwVjj3K6bQwD3w66HelHqdGn-CxhqhVi1XmhgUeYgTUsZIBlXeKtwSieIiDrYTjLAXXWjITDTjoLdLMI8LGckeB-6YJLGvITlm8rGmxybVNqkc-xHLpN8I3SVilUWgJwrL0UgfwX9DnOBohSC3_8pqpSmWOC4hTc4SawHyxCUJigOA34PEQFMqQ_RSZIK"
      }
    ]
  },
  {
    "index": 9,
    "results": [
      {
        "source_title": "도시농업, 경제ㆍ사회ㆍ환경적 가치 5조 넘는다 - 식품저널 foodnews",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAI2D0rwHh5EaBhKHZUduMExMq4l22R9HtIX0qOwubDX92UE5-mJycX1QUW7X1GgVpWf3kt94jK0OvMVPH0radqfF5b483oHnAzizN53ErYytUssk86CyVVM6TpCPxpqjAc3-0ptaN-Dw5vkWeS6qiOnQg9w"
      },
      {
        "source_title": "도시농부 200만 명 넘었다, 도시농업 가치 금액으로 환산하면 '5조' - 비즈니스포스트",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAIPGnVMatZV9V5HF5ebSEZFC3Urr5C5rIQ5II774NJ7iKI6PW_Jf_ZkEv4eNVmWqgAoCbp361gOgN73E49foY0M0Jo2rv3PGtJ62_vej1KfHGAABuxLiBe3GzH6T9K_J-37lG4vINGe0fIrdUNFrozPOlIbhjvY4Q=="
      },
      {
        "source_title": "도시농업 경제가치 '5조원' 훌쩍 넘어",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqALgeM90h54LUhzbgB_zE4r8240gqIzv67lFQrTol0HplQcDOIaGtBBf_mPeKUfT7LtatO7dhmtULOvJlglmaTx7JUMME09qHx2tPLyfz02rSo-5epyFHo_QWkaRxp5R9ioRlugg"
      }
    ]
  },
  {
    "index": 14,
    "results": [
      {
        "source_title": "도시 농업을 통한 일자리 창출 – 새로운 직업과 비즈니스 모델",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAI2D_v01upTCtpriG4vkB2onfjMVXIRz0T2vdFwJAH8qjrHVFY6Jl-yKpv8XQqSzlSE1AQoLuRblfzK9Z0_MzdQhpIzQc18NTGu3WFQdaWmVqAJYDgkDg=="
      },
      {
        "source_title": "스마트팜, 도시를 살리다 - 대학생신재생에너지기자단",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAL-ocJJd8OHfGOoYtow6uUXzgjdUNpRIhF9vy-iKDcyLEzC1YL1BndDXPP0P0qvW5i69NUyFdU9MClOFwXt4ZKRhkFkPgFvKZF-h7a3RNYUczjn3A4EzQo3R-toSsdC_Q=="
      },
      {
        "source_title": "스마트팜 혁신: 데이터 기반 농업의 미래와 성공 전략 - Goover",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAKk9nNZ0xsV0oWoLiu34DZ_nFTTyUTZmYBOH9fQBiguxjkLimc_oX5xD9oVbq-adnyG4ZiyguvAeIm_48kSWjmq4N0XvJEZ2_lia-fTERz7Re9sVHZMQ6g2Ll_xsvCeiK7T4f6wSXksi0ddoUAmmnTQ8-Tk1igvV3bVk3kSJlKLJIuAgNJSR-9fbJysJtovLzoqgu6-lj435LOMhQ=="
      }
    ]
  },
  {
    "index": 15,
    "results": [
      {
        "source_title": "지속가능한 도시발전과 기업의 역할 - 3",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAJ_3mNq79XfVwX9gUAZa4FcSrszaFwEGuxAtEZ10qBdDtDlmv20BCjH5PS_dNR0RlkCTweZNTT8vuD7rT_DUHfsVKJClFv6w4DwLgAFKUerNl_0jd0DkxBLQ2Wfxci1fICHmlH3vi8g-2K1NCZN9LxZRpvTuWZVur4B"
      },
      {
        "source_title": "도시농업의 바람직한 미래상:도농 상생의 길 - 한국농촌경제연구원",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAJyzlNa-SmofPgvsu9RXIgUAvkZaMfoEFOlYae5Bz-vCsItsZSw4WPbWfesF4x9F0SGF6F6MTD7CVfPjZ61JdIA8patW6nLdJQcEJzLHA0aslgzqXd8Y2mZlpc69A6CAMTdFI8yQQ3SKQCAI6_7cuK8GvwnlGl8kPIK"
      },
      {
        "source_title": "농업과 환경의 가치, 도시농업에서 찾다",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqALiH8dBZ4732J9gAjq72I1x7-8mjvZmCF5C7BrHL5NrJoP09rTnsBN0KB-RpUTMyitMSNLi3eDDRh5sORhG2GELIQhwwoPJrH-Xrmkn2fR7ybEIM1ka08CPC1--z0HEcZ9m8IGi74b3Cum6ZZzZ"
      }
    ]
  },
  {
    "index": 16,
    "results": [
      {
        "source_title": "'지속가능성' 눈 뜬 아시아…“기대치 커졌지만 기업 준비 부족” - 데이터넷",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAKjjE6tWdSoKasahpDJ1n3-u0Uh0u4tMXtuzI3B4Ai3XzJUN_cNmT40qKDhezbATFvdLNuCkbZgUBXuVnlZN9tDUvCmy_j1SAsB_KBvdRaj0YIHZG-u4rrexfPcwohMVUH3Xs-xvsBa5Q3ah5EAZpNUSGs="
      },
      {
        "source_title": "“정부와 기업, 주민공동체가 함께 협력해야” - 전북도민일보",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAJogkYJXGkXC4BqEDq5v3ywvi8fLMU4N_JCpANAEy_miP_WaiQ8S_PppaonMI0NlNRSHgmLFBhzTa0Pb6mrsvE-TGQHGRSCy19vtLH-xKTQAgkxWmDb_I3yhJvPA7WwxN1-Br34SlmFVp_KmYTEVKZK7w=="
      },
      {
        "source_title": "지속가능한 도시발전의 거버넌스 체계 구축",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqALQDS9lCXCkRm0P3oWFbkDEi06uVIHb7RTBBBdL0tLpeoZ9ZKOe0e3KH2a1nEsgaAFQ6ttBRe7i32yr1bAqku33AeyOTnU6-6JYTU3m01aKG6SQVztAx12z2VXs65y78ANHlzJ6EMaY3UV9FgI43XCI8sJfvJtYUUrWs6GfODqYf31C4LKJcnvtxHI="
      }
    ]
  },
  {
    "index": 22,
    "results": [
      {
        "source_title": "도시농업의 경제·사회·환경 가치는 5조 원 이상",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAKYA6wQuK277wihuioO2rIZKYLBe3EwJUHV7GBIZstshylPpXYHrJZ8-DaiBtZlWDxW-EjG0JnR-Ct9fCjVafszwNxRlkzf9WbXGZUMkujVDNOQiLsH9I9MdvcNbpYajge37h-puv3pImreegjrZsERNiqHKEEK"
      },
      {
        "source_title": "도시농업을 통한 친환경 도시공동체 만들어가기",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqALsavUrW5Ms63-ivr4x7FbTBgGWc1f2ESDSWUFQt_UprFNKaOtz2RPxUDat6fX5fLGJUhItoDT603NlTzyoo-21_czGDAvBDHHcg6nuvWONMOU71DguECf5nEkmtg0yFB6M1Zm-r7nxLvhUxE8MnB0tww=="
      },
      {
        "source_title": "도시 농업 프로젝트로 지역 경제를 살리는 방법",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAJ699wF5gSbLO68i9DIAQg9FZiR9mtWmklt4XlNGahB_3J6uckft0mUeZAvNjgGmHLPsTzAZ70a0DnVqtYNxryCtK_1feVSMyc3lbdMuECO57rW21cAsWUKOLlhZhrMtpP-4iJNBeWDp6omZZUoCdnpS6FIaOyDOaUw9BpINxs4ufo1OXoZ2kIOALgtD0eoJ2ykm1QzPIYsdURzJKKV2Af7APZIvboDBgdgk1H9WPbFwmO580UBlZFagnBnDEevAZyOTyX-5JiIPVJTBZ9LNFFeQ6MbG5YfoIeOLQh3WKOQi4Sd7lvxKaaZQu7h0Nrv1fpGqFNU5PeBlK5yoOHMdmvhKvjc9Kh"
      }
    ]
  },
  {
    "index": 23,
    "results": [
      {
        "source_title": "'도시에서 귀농합니다!' - 서울시를 중심으로 한 국내 도시농업의 흐름과 전망 - 이로운넷",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAKquehG_4C-UjyRVFH01st7y22RqG6YwTnjDImtn4VZzQKrTCa2ySx1UOFikesWURb3byhr5FQyKN28Z9XBlT59BJiC2acMnZ1iljnq1dh2bDg0IB_N0dOTZYQYGMidJAXRWijQ9sqAqlSSsgU="
      },
      {
        "source_title": "도시직장인과 귀농귀촌인의 삶의 질 만족도와 농촌 생활에 대한 인식 차이 분석: 청년층을 중심 - 빈곤문제국제개발연구원",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAKe5-jXtZYbknCZAxM3tyCWQDwjaEt78o5BM4L2so1OJqvffo9BrfCF8wi4Sj9AwqEnmK--7rjL66T2VQHogux52ANC-MG5iynXdWg61R3X4w7C2vbvQ2v4e4o4SzosNHUqGgzPiBNp6WdPtp98h-Ra9ULsi6PF1HEOkXjM768wMpl2X1lDMHqFAWXleYAkBySPxy2y"
      },
      {
        "source_title": "2023 국민정책디자인 우수사례 - '태어난 김에,도시농부' -초보 도시농부 육성프로젝트",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAJbjgYLqMzPKO2bwGeG98hSZYwqvInzZa_e4AUDWYjPib_wneBMfF-ujSDhaBv2731kOG5ZRLG7m8ZyUSLvG-HOUDp5KVirLGpMRr131QBoMbaBFRUSATFFB-49LBsirXNRWoCJcjBxVqHBhaLmt38nCIrw2A6A-w8jyLMU4YU4ojJSdnu0wX9OF5EQR3RvGKmaghMs0u9bRY_qGMHeNueTAkLnHOJUUbv8f8XPaziuiTbcRnqfXLzG1lVf30f7iSGc-CKJ2pH8yIyNbhEzWNPtpuyW-Ma_KLHB5Iw-UcCKg=="
      }
    ]
  },
  {
    "index": 24,
    "results": [
      {
        "source_title": "스마트시티의 미래: 문제 진단과 해결 방안 제시 - Goover",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAJ_rXq60-Wh5n1lVQxZivxxv6OdVnUMxh7JlwAw_b25yn5oq4oEkUHofxkNbtZjGfOOk5kO2JNSrJYSR1jMDyNTaQbhbkpWczezTKnJZicaH1NdOJHFg9T_xxDViY2arzIKBktrae8hi2rhVdmVJA5otFhti6hOcghwrWIEquuxp8CZaDwBDKkx7x_Fuhk2S_kAhUMztGoNFrDlZw=="
      },
      {
        "source_title": "지속가능한 도시발전의 거버넌스 체계 구축",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqALQDS9lCXCkRm0P3oWFbkDEi06uVIHb7RTBBBdL0tLpeoZ9ZKOe0e3KH2a1nEsgaAFQ6ttBRe7i32yr1bAqku33AeyOTnU6-6JYTU3m01aKG6SQVztAx12z2VXs65y78ANHlzJ6EMaY3UV9FgI43XCI8sJfvJtYUUrWs6GfODqYf31C4LKJcnvtxHI="
      },
      {
        "source_title": "미래 도시의 진화하는 도시, 인간은 어떤 미래에서 살게 될 것인가 - 나비스(NABIS) 균형발전종합정보시스템",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAL54DSolyLJ_2BXu3GnU6C7ab8lWWEvUUTC80T_RJfB9WW24puG0kmGfH6bO560YhdDfS9Gk2kR9Z9Q6eVXE36gQ7i4NtqZseDSfUZu7w8Fnf-aHaXhm0vBj3mG8hI9jhD7zPzuYiDSE9mpP-z5B75H_CnS_yCUxQPLWeq27jrG0iXELBzK0GqQFl7H7B9t4keTfZVoh7lX_jM_vOcrUuYtkQY29KhBeAvmF-oOtQbwcpL3vhV7rOx8RDEjLt0XvXD8QVXeJJokiThS_WwuKMSWw=="
      }
    ]
  },
  {
    "index": 26,
    "results": [
      {
        "source_title": "도시농업을 통한 친환경 도시공동체 만들어가기",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqALsavUrW5Ms63-ivr4x7FbTBgGWc1f2ESDSWUFQt_UprFNKaOtz2RPxUDat6fX5fLGJUhItoDT603NlTzyoo-21_czGDAvBDHHcg6nuvWONMOU71DguECf5nEkmtg0yFB6M1Zm-r7nxLvhUxE8MnB0tww=="
      },
      {
        "source_title": "농업과 환경의 가치, 도시농업에서 찾다",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqALiH8dBZ4732J9gAjq72I1x7-8mjvZmCF5C7BrHL5NrJoP09rTnsBN0KB-RpUTMyitMSNLi3eDDRh5sORhG2GELIQhwwoPJrH-Xrmkn2fR7ybEIM1ka08CPC1--z0HEcZ9m8IGi74b3Cum6ZZzZ"
      },
      {
        "source_title": "올리야드 소개",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAL2Q0WussQwEMykDtPxPrkIvbvMUY1wzw16ohCEkOcW7_D23w1ces00YXVeNXeVPuw2J9ERFbuWBj3CelQ3xfSpes6YD7Yh-v5N6k39qdsGIHuBH9VAM3wk"
      }
    ]
  },
  {
    "index": 27,
    "results": [
      {
        "source_title": "[인터뷰] 이진관 김포시농업기술센터 소장 - 에너지경제신문",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAJkvFc61xq3vM-mOmLgabcUFE9TQmsqLEe3gA-SgVmhoK804o41UE4LbY7RTPgczRmVo5QAkdFe5Lam77Ap4PLnGsEobo5_H3tgqvC4BM3SsteSXd7uXq4TTxD6RO_wme5uN2Dy3A=="
      },
      {
        "source_title": "전문가들이 보는 2050 농업·농촌의 미래 - KREI Repository",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAK8dOJkQym7pu_pr22SRI0OO5MkxjODAI0_TAqmpUPMJnBhS3rkTu8w4am_kzXFjmClGORizGaz0L71I3OMOC1CjWeoKLGd0RckZRyxZQzCa-0B71SWQNueCY0B4zk9y4mGM2V9aRdtIWaIEsFT1eG42M3YMFcx_q63trXEhpobCzSewq4OhMIP8fKkwVUmigNliDnchbNq-wx2hRaWYNGuNYfLqXavKxJow7-6b0zhpUf_ycx6qGZej2fGqGAO5UblrHSxBqX_9gu8HRX55-qyF8QlZ0_4eI_kEobxGgnxJSE27IXESr0yRf8iC5R-y16p7FuksgrpZwDaPtHx0qzxK6RliAGVzC4="
      },
      {
        "source_title": "도시직장인과 귀농귀촌인의 삶의 질 만족도와 농촌 생활에 대한 인식 차이 분석: 청년층을 중심 - 빈곤문제국제개발연구원",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAKe5-jXtZYbknCZAxM3tyCWQDwjaEt78o5BM4L2so1OJqvffo9BrfCF8wi4Sj9AwqEnmK--7rjL66T2VQHogux52ANC-MG5iynXdWg61R3X4w7C2vbvQ2v4e4o4SzosNHUqGgzPiBNp6WdPtp98h-Ra9ULsi6PF1HEOkXjM768wMpl2X1lDMHqFAWXleYAkBySPxy2y"
      },
      {
        "source_title": "2023 국민정책디자인 우수사례 - '태어난 김에,도시농부' -초보 도시농부 육성프로젝트",
        "url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWQVqAJbjgYLqMzPKO2bwGeG98hSZYwqvInzZa_e4AUDWYjPib_wneBMfF-ujSDhaBv2731kOG5ZRLG7m8ZyUSLvG-HOUDp5KVirLGpMRr131QBoMbaBFRUSATFFB-49LBsirXNRWoCJcjBxVqHBhaLmt38nCIrw2A6A-w8jyLMU4YU4ojJSdnu0wX9OF5EQR3RvGKmaghMs0u9bRY_qGMHeNueTAkLnHOJUUbv8f8XPaziuiTbcRnqfXLzG1lVf30f7iSGc-CKJ2pH8yIyNbhEzWNPtpuyW-Ma_KLHB5Iw-UcCKg=="
      }
    ]
  }
]
```
"""

cleaned = test.strip().removeprefix("```json").removesuffix("```").strip()
parsed = json.loads(cleaned)
trimmed = parsed[1:-1]
result_str = json.dumps(trimmed, indent=2, ensure_ascii=False)
print(result_str)