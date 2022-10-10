import base64

import requests
import re
import json
from urllib import parse

comcigan_url = 'http://comci.kr:4082'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def get_code():
    resp = requests.get(comcigan_url+'/st', headers=headers).text.decode('euc-kr').encode('utf-8')
    print(resp)
    comcigan_code = re.compile('\\./[0-9]+\\?[0-9]+l').match(resp)[0][1:]
    code1 = re.compile('성명=자료.자료[0-9]+').match(resp)[0][8:]
    code2 = re.compile('자료.자료[0-9]+[sb]').match(resp)[0][5:-4]
    code3 = re.compile('=H시간표.자료[0-9]+').match(resp)[0][8:]
    code4 = re.compile('일일자료=자료.자료[0-9]+').match(resp)[0][10:]
    code5 = re.compile('원자료=자료.자료[0-9]+').match(resp)[0][9:]
    return comcigan_code, code1, code2, code3, code4, code5


def get_school_code(school_name, local_code, school_code, comcigan_code):
    resp = json.loads(str(requests.get(comcigan_url + comcigan_code + parse.urlencode(school_name, encoding='euc-kr'))))
    if len(resp["학교검색"]) == 0:
        return {
            'success': False,
            'reason': '학교를 찾을 수 없습니다.'
        }
    elif len(resp["학교검색"]) > 1:
        if (school_code):
            for data in resp["학교검색"]:
                if data[3] == school_code:
                    return data[0], data[3]
        if (local_code):
            for data in resp["학교검색"]:
                if data[0] == local_code:
                    return data[0], data[3]
        return -1, resp

    return resp[0][0], resp[0][3]


def getTimeTable(school_name, local_code, school_code, next_week):
    if next_week != "0" and next_week != "1":
        return {
            'success': False,
            'reason': 'next_week는 0또는 1의 값을 가져야 합니다.'
        }
    try:
        local_code = int(local_code)
        school_code = int(school_code)
    except Exception:
        return {
            'success': False,
            'reason': 'local_code와 school_code는 정수여야 합니다.'
        }

    comcigan_code, code1, code2, code3, code4, code5 = get_code()

    local_code, school_code = get_school_code(school_name, local_code, school_code, comcigan_code)
    if local_code == -1:
        return {
            "success": False,
            "reason": "2개 이상의 학교가 검색됩니다.",
            "data": school_code["학교검색"]
        }

    sc = base64.b64encode(f"{str(local_code)}_{school_code}_0_{str(int(next_week) + 1)}".encode('utf-8'))
    resp = json.loads(str(requests.get(f'{comcigan_url}{comcigan_code[:8]}{sc}')).replace("\n", " "))
    result = {
        "success": True,
        "학교명": resp["학교명"],
        "지역명": resp["지역명"],
        "학년도": resp["학년도"],
        "시작일": resp["시작일"],
        "일과시간": resp["일과시간"],
        "갱신일시": resp["자료" + code3],
        "data": []
    }

    teacher_list = resp["자료" + code1]
    sub_list = resp["자료" + code2]
    subject_list = resp["긴자료" + code2]
    original_timetable = resp["자료" + code5]

    grade = 0
    for i in resp["자료" + code4]:
        cls = 0
        if grade == 0:
            result["data"][0] = ""
            grade += 1
            continue
        for j in i:
            if cls == 0:
                result["data"][grade] = [{}]
                cls += 1
                continue
            result["data"][grade].append({
                "grade": grade,
                "class": cls,
                "timetable": [[]]
            })
            for day in range(1, 7):
                result["data"][grade][cls]["timetable"].append([[]])
                original_period = original_timetable[grade][cls][day][period]
                for period in range(1, 9):
                    period_data = {
                        "period": period,
                        "teacher": teacher_list[period // 100],
                        "sub": sub_list[period % 100],
                        "subject": subject_list[period % 100],
                        "room": "강의실",
                        "replaced": period == original_period,
                        "original": {
                            "teacher": teacher_list[original_period // 100],
                            "sub": sub_list[original_period % 100],
                            "subject": subject_list[original_period % 100],
                            "room": "원래 강의실"
                        }
                    }
                    result["data"][grade][cls]["timetable"][day].append(period_data)
            cls += 1
    return result
