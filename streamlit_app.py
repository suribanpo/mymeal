import streamlit as st
import requests
import json
import datetime
import pandas as pd
from mymodule.module1 import find_my_school, give_me_meal

# 알레르기 정보 매핑
allergy_info = {
    "1": "난류", "2": "우유", "3": "메밀", "4": "땅콩", "5": "대두", "6": "밀", "7": "고등어", "8": "게", "9": "새우",
    "10": "돼지고기", "11": "복숭아", "12": "토마토", "13": "아황산류", "14": "호두", "15": "닭고기", "16": "쇠고기",
    "17": "오징어", "18": "조개류", "19": "잣"
}

# 알레르기 번호를 재료명으로 변환하는 함수
def extract_allergy_info(menu_item):
    if '(' in menu_item and ')' in menu_item:  # 알레르기 정보가 있는 경우
        text_part = menu_item.split('(')[0].strip()
        number_part = menu_item.split('(')[1].split(')')[0]
        allergies = ', '.join([allergy_info.get(num, num) for num in number_part.split('.') if num])
        return text_part, allergies
    else:
        return menu_item, None

# 페이지 기본 설정
st.set_page_config(
    page_title="급식타임 🍽️",
    page_icon="🍱",
    layout="centered"
)

# 타이틀 설정
st.title("🍽️ **급식타임**")

# API 키와 기본 URL 설정
neiskey = st.secrets['neis']['key']
url = "https://open.neis.go.kr/hub/schoolInfo"

# 학교 조회
st.subheader("🏫 학교 조회")
school_input = st.text_input("학교이름을 입력해주세요.", "반포고등학교")

# 학교 정보 조회 및 오류 처리
try:
    schools_by_district = find_my_school(school_input, url)
except Exception as e:
    st.error(f"학교 정보를 가져오는 데 문제가 발생했습니다: {e}")
    schools_by_district = {}

if schools_by_district:
    # 학교 소속된 교육청 선택
    district = st.radio("이름이 비슷한 학교가 많네요. 아래에서 학교가 소속된 교육청을 선택해주세요", options=schools_by_district)
    school_name = schools_by_district[district][0]
    school_code = schools_by_district[district][1]
    district_code = schools_by_district[district][2]

    # 급식 조회
    st.subheader(f"🍴 {school_name}의 급식을 찾아볼게요!")
    date = st.date_input("조회할 날짜를 입력해주세요:", datetime.datetime.now()).strftime("%Y%m%d")

    # 급식 정보 조회 및 오류 처리
    try:
        menu = give_me_meal(district_code, school_code, date)
    except Exception as e:
        st.error(f"급식 정보를 가져오는 데 문제가 발생했습니다: {e}")
        menu = []

    # 알레르기 주의사항 정보 - 작은 글씨로 표시
    st.markdown("""
        <style>
        .small-text {
            font-size: 12px;
            color: #666;
        }
        </style>
        <div class="small-text">
        ⚠️ *알레르기 주의사항*
        개인적으로 특정한 식품에 알레르기가 있는 학생인 경우 식단과 알레르기 표시를 보시고 해당되는 음식은 피해 주시기 바랍니다.            
        식단은 학교 사정과 물가 변동 및 시장 사정에 의해 변경될 수 있습니다.
        </div>
        """, unsafe_allow_html=True)

    formatted_date = datetime.datetime.strptime(date, "%Y%m%d").strftime("%m월 %d일")

    # 급식 정보가 없을 때 처리
    if not menu:
        st.warning("해당 날짜의 급식 정보가 없습니다.")
    else:
        st.success(f"🍽️ {formatted_date}자 급식 정보입니다. 즐거운 점심!")
        # 체크박스: 알레르기 정보를 표시할지 여부 선택
        show_allergy_info = st.checkbox("알레르기 정보를 표시할까요?", value=False)

        # 메뉴를 하나씩 처리하고 체크박스를 통해 알레르기 정보 표시
        for menu_item in menu:
            # 메뉴 아이템에서 알레르기 정보를 분리
            item_text, allergy_info_text = extract_allergy_info(menu_item)

            # 체크박스 상태에 따라 알레르기 정보를 help 옵션에 표시
            if show_allergy_info and allergy_info_text:
                st.markdown(f"#### {item_text}", help=allergy_info_text)  # help 옵션으로 알레르기 정보 표시
            else:
                st.markdown(f"#### {menu_item}")  # 알레르기 정보 없이 메뉴만 표시


# 푸터 추가
st.markdown("---")
st.caption("© 2024 급식타임 | Powered by NEIS API, made by 황수빈T")
