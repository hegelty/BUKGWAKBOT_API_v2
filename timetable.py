import base64
import requests
import re
import json
from urllib import parse

comcigan_url = 'http://comci.net:4082'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def get_code():
    resp = requests.get(comcigan_url + '/st', headers=headers)
    resp.encoding = 'euc-kr'
    resp = resp.text
    comcigan_code = re.findall('\\.\\/[0-9]+\\?[0-9]+l', resp)[0][1:]
    code0 = re.findall('sc_data\(\'[0-9]+_', resp)[0][9:-1]
    code1 = re.findall('성명=자료.자료[0-9]+', resp)[0][8:]
    code2 = re.findall('자료.자료[0-9]+\\[sb\\]', resp)[0][5:-4]
    code3 = re.findall('=H시간표.자료[0-9]+', resp)[0][8:]
    code4 = re.findall('일일자료=Q자료\\(자료\\.자료[0-9]+', resp)[0][14:]
    code5 = re.findall('원자료=Q자료\\(자료\\.자료[0-9]+', resp)[0][13:]
    return comcigan_code, code0, code1, code2, code3, code4, code5


def get_school_code(school_name, local_code, school_code, comcigan_code):
    resp = requests.get(comcigan_url + comcigan_code + parse.quote(school_name, encoding='euc-kr'))
    resp.encoding = 'UTF-8'
    resp = json.loads(resp.text.strip(chr(0)))
    print(resp["학교검색"])
    if len(resp["학교검색"]) == 0:
        return -2, resp
    elif len(resp["학교검색"]) > 1: #2개 이상이 검색될
        if (school_code):
            for data in resp["학교검색"]:
                if data[3] == school_code:
                    return data[0], data[3]
        if (local_code):
            for data in resp["학교검색"]:
                if data[0] == local_code:
                    return data[0], data[3]
        return -1, resp
    return resp['학교검색'][0][0], resp['학교검색'][0][3]


def getTimeTable(school_name, local_code, school_code, next_week, simple):
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

    comcigan_code, code0, code1, code2, code3, code4, code5 = get_code()

    local_code, school_code = get_school_code(school_name, local_code, school_code, comcigan_code)
    if local_code == -1:
        return {
            "success": False,
            "reason": "2개 이상의 학교가 검색됩니다.",
            "data": school_code["학교검색"]
        }
    elif local_code == -2:
        return {
            "success": False,
            "reason": "학교를 찾을 수 없습니다"
        }

    sc = base64.b64encode(f"{str(code0)}_{school_code}_0_{str(int(next_week) + 1)}".encode('utf-8'))
    resp = requests.get(f'{comcigan_url}{comcigan_code[:7]}{str(sc)[2:-1]}', headers=headers)
    resp.encoding = 'UTF-8'
    resp = resp.text.split('\n')[0]
    resp = json.loads(resp)
    print(resp)

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
            result["data"].append("")
            grade += 1
            continue
        for j in i:
            if cls == 0:
                result["data"].append([{}])
                cls += 1
                continue
            result["data"][grade].append({
                "grade": grade,
                "class": cls,
                "timetable": [[]]
            })

            for day in range(1, 7):
                result["data"][grade][cls]["timetable"].append([{}])
                for period in range(1, 9):
                    original_period = original_timetable[grade][cls][day][period]
                    period_num = j[day][period]
                    if simple == 1:
                        period_data = {
                            "period": period,
                            "teacher": teacher_list[period_num // 100],
                            "sub": sub_list[period_num % 100],
                            "subject": subject_list[period_num % 100],
                            "replaced": period_num != original_period
                        }
                    else:
                        period_data = {
                            "period": period,
                            "teacher": teacher_list[period_num // 100],
                            "sub": sub_list[period_num % 100],
                            "subject": subject_list[period_num % 100],
                            "room": "강의실",
                            "replaced": period_num != original_period,
                            "original": {
                                "teacher": teacher_list[original_period // 100],
                                "sub": sub_list[original_period % 100],
                                "subject": subject_list[original_period % 100],
                                "room": "원래 강의실"
                            }
                        }
                    result["data"][grade][cls]["timetable"][day].append(period_data)
            cls += 1
        grade += 1
    return result


