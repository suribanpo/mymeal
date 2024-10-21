import streamlit as st

# 학교 조회하는 함수/ 합수 입력 > 라디오버튼 선택하게
@st.cache_data
def find_my_school(school_name, url):
    params={
        'KEY':st.secrets['neis']['key'],
        'Type':'json',
        'pIndex' :1,
        'pSize' : 100,
        'SCHUL_NM' : school_name
        }

    response = requests.get(url, params=params)
    contents = response.text
    # JSON 문자열을 Python 딕셔너리로 파싱
    data = json.loads(contents)
    # st.write(data)

    schools_by_district = {}
    for item in data["schoolInfo"][1]["row"]:
        district = item["ATPT_OFCDC_SC_NM"]
        district_code = item['ATPT_OFCDC_SC_CODE']
        school_name = item["SCHUL_NM"]
        school_code = item['SD_SCHUL_CODE']
        schools_by_district.setdefault(district, []).append(school_name)
        schools_by_district.setdefault(district, []).append(school_code)
        schools_by_district.setdefault(district, []).append(district_code)
    return schools_by_district

@st.cache_data
def give_me_meal(district_code, school_code, date):
    mealurl = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
    params={
        'KEY':st.secrets['neis']['key'],
        'Type':'json',
        'pIndex' :1,
        'pSize' : 100,
        'ATPT_OFCDC_SC_CODE' : district_code,
        'SD_SCHUL_CODE' : school_code,
        'MLSV_YMD' : date
        }

    response = requests.get(mealurl, params=params)
    contents = response.text
    # JSON 문자열을 Python 딕셔너리로 파싱
    data = json.loads(contents)
    # st.write(data)
    try:
        menu = data["mealServiceDietInfo"][1]['row'][0]['DDISH_NM'].split('<br/>')
    except:
        st.error("정보를 불러올 수 없습니다. 날짜를 다시 확인해주세요! 급식이 없던 날 같아요. ")
        menu = []
    # st.write(data)
    return menu