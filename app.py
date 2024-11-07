import streamlit as st
import openai
import json
from datetime import datetime
from crawler.school_crawler import get_school_meals

# OpenAI API 키 설정
openai.api_key = "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"

# 학교 정보 JSON 파일 로드
with open('data/school_info.json', 'r', encoding='utf-8') as f:
    school_info = json.load(f)

# 앱 제목 설정
st.title(f"현대청운고 청운이")

# OpenAI 모델 요청
if prompt := st.text_input("메세지를 입력하세요."):
    messages = [
        {"role": "system", "content": "You are an assistant named 청운이 that provides information about the school."},
        {"role": "user", "content": prompt}
    ]

    # API 호출
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )

    # 응답 출력
    st.write(response['choices'][0]['message']['content'])

# 실시간 급식 정보 크롤링
breakfast_menu, lunch_menu, dinner_menu = get_school_meals()

# 오늘의 날짜 구하기
today = datetime.today().strftime('%Y-%m-%d')

# 조식 출력
st.subheader(f"오늘의 조식 ({today})")
if breakfast_menu:
    for item in breakfast_menu:
        st.write(item)
else:
    st.write("조식 정보가 없습니다.")

# 중식 출력
st.subheader(f"오늘의 중식 ({today})")
if lunch_menu:
    for item in lunch_menu:
        st.write(item) 
else:
    st.write("중식 정보가 없습니다.")

# 석식 출력 
st.subheader(f"오늘의 석식 ({today})")
if dinner_menu:
    for item in dinner_menu:
        st.write(item)
else:
    st.write("석식 정보가 없습니다.")

# 학교 행사 정보 출력
st.subheader("다가오는 학교 행사")
for event in school_info['events']:
    st.write(f"{event['date']}: {event['event']}")
