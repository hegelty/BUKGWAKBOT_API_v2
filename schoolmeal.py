import sqlite3

from tools import *

conn = sqlite3.connect("./MealDate.db")
curs = conn.cursor()


curs.execute(
    "CREATE TABLE IF NOT EXISTS meals(schoolname TEXT, schoolcode TEXT, date INTEGER , type TEXT, menu TEXT, allergy TEXT, nutrition TEXT, origin TEXT, cal INTEGER)")


def getMeal(meal_date, school_name="", school_code="", goe_code="", local="", reload=False):
    if not school_code:
        if not school_name:
            return {
                'success': "실패",
                'reason': "학교명 또는 학교 코드를 입력하세요."
            }
        school_code = getSchoolInfo(school_name=school_name, local_name=local)
        if school_code["success"] == "실패":
            return {
                'success': "실패",
                'reason': "학교를 찾을 수 없습니다."
            }
        goe_code = school_code["data"][0]["ATPT_OFCDC_SC_CODE"]
        school_code = school_code["data"][0]["SD_SCHUL_CODE"]
    else:
        school_name = getSchoolInfo(school_code=school_code)
        if school_name["success"] == "실패":
            return {
                'success': "실패",
                'reason': "학교를 찾을 수 없습니다."
            }
        school_name = school_name["data"][0]["SCHUL_NM"]

    if reload:
        addMealData(meal_date, school_code, school_name, goe_code)
    else:
        curs.execute("SELECT * FROM meals where schoolcode=? and date=?", (school_code, meal_date))
        data = curs.fetchone()
        if not data:
            addMealData(meal_date, school_code, school_name, goe_code)

    curs.execute("SELECT * FROM meals where schoolcode=? and date=?", (school_code, meal_date))
    data = curs.fetchall()
    result = {
        'success': "성공",
        'count': len(data),
        'school': school_name,
        'data': []
    }
    for i in data:
        result['data'].append({
            'type': i[3],
            'menu': i[4],
            'allergy': json.loads(i[5]),
            'nutrition': i[6],
            'origin': i[7],
            'cal': i[8]
        })

    return result


def addMealData(meal_date, school_code, school_name, goe_code):
    params = {
        'KEY': NIES_API_KEY,
        'SD_SCHUL_CODE': school_code,
        'ATPT_OFCDC_SC_CODE': goe_code,
        'MLSV_YMD': meal_date,
        'type': 'json'
    }

    meal_data = json.loads(requests.get("https://open.neis.go.kr/hub/mealServiceDietInfo", params=params).text)
    if "RESULT" in meal_data:
        return {
            'success': "실패",
            'reason': nies_result_code_dict[meal_data["RESULT"]["CODE"]]
        }

    curs.execute("DELETE FROM meals WHERE schoolcode=? and date=?", (school_code, meal_date))
    for data in meal_data["mealServiceDietInfo"][1]["row"]:
        curs.execute("INSERT INTO meals VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            school_name, school_code, meal_date, data['MMEAL_SC_NM'],
            reformatMeal(data['DDISH_NM'].replace("<br/>", "\n")),
            json.dumps(getAllergyInfo(reformatMeal(data['DDISH_NM'].replace("<br/>", "\n")), data['DDISH_NM'].replace("<br/>", "\n"))), data['NTR_INFO'].replace("<br/>", "\n"),
            data['ORPLC_INFO'].replace("<br/>", "\n"), data['CAL_INFO']))
    conn.commit()


def reformatMeal(meal_str) -> str:
    for i in range(0, 10):
        meal_str = meal_str.replace(str(i), "")
    string_to_remove = ["*", "$", ".", " 발", " 과", "뽱", "컁", "꿜", "(조)", "(조/과)", "(조과)", "(과)", "(조식)", "(석/과)", "(옥정)", "(완)", "(고)", "(과석)"
                        "CB", "()"]
    for i in string_to_remove:
        meal_str = meal_str.replace(i, "")
    meal_str = '\n'.join(map(lambda x: x.strip(), meal_str.replace("발\n", "\n").replace("과\n", "\n").split("\n")))
    return meal_str


def getAllergyInfo(menu_str, original_str):
    menus = menu_str.split("\n")
    result = {}
    for i, menu in enumerate(original_str.split("\n")):
        alg = menu.split("(")[-1].split(")")[0]
        result[menus[i]] = alg
    return result
