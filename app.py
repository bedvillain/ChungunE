import streamlit as st
import openai
import json
import sqlite3
from datetime import datetime
from crawler.school_crawler import get_school_meals

# OpenAI API 키 설정
openai.api_key = "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" 

# 오늘의 날짜 구하기
today_date = datetime.today().strftime('%Y-%m-%d')

# 데이터베이스에서 학교 정보와 행사 정보를 가져오는 함수들
def get_school_info():
    conn = sqlite3.connect('data/school_info.db')
    cursor = conn.cursor()
    
    # schools 테이블에서 학교 기본 정보 가져오기
    cursor.execute("SELECT name, address, principal, vice_principal, kind FROM schools WHERE id = 1")
    school_info = cursor.fetchone()
    conn.close()
    return school_info

# 행사 정보를 가져오는 함수
def get_events():
    conn = sqlite3.connect('data/school_info.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT date, event FROM events WHERE date >= ?", (today_date,))
    events = cursor.fetchall()
    conn.close()
    return events

def get_grade_2_info():
    conn = sqlite3.connect('data/school_info.db')
    cursor = conn.cursor()

    # grade_2 테이블에서 학급 정보 가져오기
    cursor.execute("SELECT class, teacher, T_subject, T_description FROM grade_2")
    grade_2_info = cursor.fetchall()
    conn.close()
    return grade_2_info

# 데이터 포맷팅 함수들
def format_school_info(school_info):
    if school_info:
        return f"**학교 이름**: {school_info[0]}\n\n**주소**: {school_info[1]}\n\n**교장 선생님**: {school_info[2]}\n\n**교감 선생님**: {school_info[3]}\n\n**유형**: {school_info[4]}"
    return "학교 정보가 없습니다."

# 행사 정보를 가져오는 함수
def format_events(events):
    if events:
        formatted_events = "다가오는 행사:\n"
        for event_date, event in events:
            formatted_events += f"- {event_date}: {event}\n"
        return formatted_events
    return "다가오는 학교 행사가 없습니다."

def format_grade_2_info(grade_2_info):
    if grade_2_info:
        formatted_info = "2학년 담임 선생님 정보:\n"
        for class_info in grade_2_info:
            formatted_info += f"- 학급: {class_info[0]}, 담임 선생님: {class_info[1]}, 과목: {class_info[2]}, 설명: {class_info[3]}\n"
        return formatted_info
    return "2학년 담임 선생님 정보가 없습니다."

def format_meal_info(breakfast, lunch, dinner):
    formatted_meals = f"오늘의 급식 정보 ({today_date}):\n\n"
    formatted_meals += "**조식**:\n" + ("\n".join(breakfast) if breakfast else "조식 정보가 없습니다.") + "\n\n"
    formatted_meals += "**중식**:\n" + ("\n".join(lunch) if lunch else "중식 정보가 없습니다.") + "\n\n"
    formatted_meals += "**석식**:\n" + ("\n".join(dinner) if dinner else "석식 정보가 없습니다.")
    return formatted_meals

# 각 정보 불러오기
school_info_text = format_school_info(get_school_info())
events_info_text = format_events(get_events())
grade_2_info_text = format_grade_2_info(get_grade_2_info())
breakfast_menu, lunch_menu, dinner_menu = get_school_meals()
meal_info_text = format_meal_info(breakfast_menu, lunch_menu, dinner_menu)

# 전체 정보를 하나의 메시지로 구성
system_content = f"{school_info_text}\n\n{events_info_text}\n\n{grade_2_info_text}\n\n{meal_info_text}"

# 사이드바 메뉴 설정
st.sidebar.title("현대청운고 정보")
menu = st.sidebar.radio("메뉴 선택", ["청운이와 대화하기", "학교 기본 정보", "행사 정보", "급식 정보"])

# 대화 기록을 위한 session_state 초기화
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# 각 메뉴에 따라 다른 정보 표시
if menu == "청운이와 대화하기":
    st.header("현대청운고 정보 챗봇 청운이")

    # 사용자 입력 받기
    prompt = st.chat_input("메세지를 입력하세요.")
    
    if prompt:
        # 사용자 메시지 추가
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # OpenAI API 호출을 위한 메시지 구성
        messages = [{"role": "system", "content": f"너는 학교 정보를 제공하는 어시스턴트 청운이입니다. 다음은 학교에 대한 정보입니다:\n\n{system_content}"}]
        messages.extend(st.session_state.chat_history)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )

        # 챗봇 응답 저장 및 기록에 추가
        assistant_response = response['choices'][0]['message']['content']
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # 대화 기록을 화면에 출력
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])

elif menu == "학교 기본 정보":
    st.header("학교 기본 정보")
    st.write(school_info_text)

elif menu == "행사 정보":
    st.header("다가오는 학교 행사")
    st.write(events_info_text)

elif menu == "급식 정보":
    # 실시간 급식 정보 크롤링
    breakfast_menu, lunch_menu, dinner_menu = get_school_meals()
    today = datetime.today().strftime('%Y-%m-%d')

    st.header(f"오늘의 급식 정보 ({today})")

    st.subheader("조식")
    if breakfast_menu:
        for item in breakfast_menu:
            st.write(item)
    else:
        st.write("조식 정보가 없습니다.")

    st.subheader("중식")
    if lunch_menu:
        for item in lunch_menu:
            st.write(item) 
    else:
        st.write("중식 정보가 없습니다.")

    st.subheader("석식")
    if dinner_menu:
        for item in dinner_menu:
            st.write(item)
    else:
        st.write("석식 정보가 없습니다.")
