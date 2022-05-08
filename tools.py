import json
import requests

keysFile = open("keys.json", "r")
keys = json.loads(keysFile.read())
NIES_API_KEY = keys["NIES_API_KEY"]
GOE_NAME_DICT = {
    "서울교육청": "서울특별시교육청", "서울시교육청": "서울특별시교육청", "서울특별시교육청": "서울특별시교육청",
    "부산교육청": "부산광역시교육청", "부산시교육청": "부산광역시교육청", "부산광역시교육청": "부산광역시교육청",
    "인천교육청": "인천광역시교육청", "인천시교육청": "인천광역시교육청", "인천광역시교육청": "인천광역시교육청",
    "대구교육청": "대구광역시교육청", "대구시교육청": "대구광역시교육청", "대구광역시교육청": "대구광역시교육청",
    "광주교육청": "광주광역시교육청", "광주시교육청": "광주광역시교육청", "광주광역시교육청": "광주광역시교육청",
    "대전교육청": "대전광역시교육청", "대전시교육청": "대전광역시교육청", "대전광역시교육청": "대전광역시교육청",
    "울산교육청": "울산광역시교육청", "울산시교육청": "울산광역시교육청", "울산광역시교육청": "울산광역시교육청",
    "세종교육청": "세종특별자치시교육청", "세종시교육청": "세종특별자치시교육청", "세종특별자치시교육청": "세종특별자치시교육청",
    "경기교육청": "경기도교육청", "경기도교육청": "경기도교육청",
    "강원교육청": "강원도교육청", "강원도교육청": "강원도교육청",
    "충북교육청": "충청북도교육청", "충청북도교육청": "충청북도교육청",
    "충남교육청": "충청남도교육청", "충청남도교육청": "충청남도교육청",
    "전북교육청": "전라북도교육청", "전라북도교육청": "전라북도교육청",
    "전남교육청": "전라남도교육청", "전라남도교육청": "전라남도교육청",
    "경북교육청": "경상북도교육청", "경상북도교육청": "경상북도교육청",
    "경남교육청": "경상남도교육청", "경상남도교육청": "경상남도교육청",
    "재외교육청": "재외한국학교교육청", "한국학교교육청": "재외한국학교교육청", "재외한국교육청": "재외한국학교교육청", "재외한국학교교육청": "재외한국학교교육청"
}
LOCAL_NAME_DICT = {
    "서울": "서울특별시", "서울시": "서울특별시", "서울특별시": "서울특별시",
    "부산": "부산광역시", "부산시": "부산광역시", "부산광역시": "부산광역시",
    "인천": "인천광역시", "인천시": "인천광역시", "인천광역시": "인천광역시",
    "대구": "대구광역시", "대구시": "대구광역시", "대구광역시": "대구광역시",
    "광주": "광주광역시", "광주시": "광주광역시", "광주광역시": "광주광역시",
    "대전": "대전광역시", "대전시": "대전광역시", "대전광역시": "대전광역시",
    "울산": "울산광역시", "울산시": "울산광역시", "울산광역시": "울산광역시",
    "세종": "세종특별자치시", "세종시": "세종특별자치시", "세종특별자치시": "세종특별자치시",
    "경기": "경기도", "경기도": "경기도",
    "강원": "강원도", "강원도": "강원도",
    "충북": "충청북도", "충청북도": "충청북도",
    "충남": "충청남도", "충청남도": "충청남도",
    "전북": "전라북도", "전라북도": "전라북도",
    "전남": "전라남도", "전라남도": "전라남도",
    "경북": "경상북도", "경상북도": "경상북도",
    "경남": "경상남도", "경상남도": "경상남도",
    "해외": "국외", "국외": "국외"
}
SCHOOL_TYPE_DICT = {
    "초": "초등학교", "초등": "초등학교", "초등학교": "초등학교",
    "중": "중등학교", "중등": "중등학교", "중등학교": "초등학교",
    "고": "고등학교", "고등": "고등학교", "고등학교": "초등학교",
    "외국인": "외국인학교", "외국인학교": "외국인학교"
}
nies_result_code_dict = {
    "ERROR-300": "필수 값이 누락되어 있습니다. 요청인자를 참고 하십시오.",
    "ERROR-290": "인증키가 유효하지 않습니다. 인증키가 없는 경우, 홈페이지에서 인증키를 신청하십시오.",
    "ERROR-310": "해당하는 서비스를 찾을 수 없습니다. 요청인자 중 SERVICE를 확인하십시오.",
    "ERROR-333": "요청위치 값의 타입이 유효하지 않습니다.요청위치 값은 정수를 입력하세요.",
    "ERROR-336": "데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다.",
    "ERROR-337": "일별 트래픽 제한을 넘은 호출입니다. 오늘은 더이상 호출할 수 없습니다.",
    "ERROR-500": "서버 오류입니다. 지속적으로 발생시 홈페이지로 문의(Q&A) 바랍니다.",
    "ERROR-600": "데이터베이스 연결 오류입니다. 지속적으로 발생시 홈페이지로 문의(Q&A) 바랍니다.",
    "ERROR-601": "SQL 문장 오류 입니다. 지속적으로 발생시 홈페이지로 문의(Q&A) 바랍니다.",
    "INFO-000": "정상 처리되었습니다.",
    "INFO-300": "관리자에 의해 인증키 사용이 제한되었습니다.",
    "INFO-200": "해당하는 데이터가 없습니다."
}


def getSchoolInfo(school_name="", school_name_eng="", school_code="", goe_code="", goe_name="", local_name="",
                  school_type=""):

    if goe_name and goe_name not in GOE_NAME_DICT:
        return {
            'success': "실패",
            'reason': "잘못된 교육청 이름입니다."
        }
    if local_name and local_name not in LOCAL_NAME_DICT:
        return {
            'success': "실패",
            'reason': "잘못된 지역 이름입니다."
        }
    if school_type and school_type not in SCHOOL_TYPE_DICT:
        return {
            'success': "실패",
            'reason': "잘못된 학교 중류입니다."
        }

    params = {
        'KEY': NIES_API_KEY,
        'type': 'json',
        "pSize": 10
    }
    if school_name: params["SCHUL_NM"] = school_name
    if school_name_eng: params["ENG_SCHUL_NM"] = school_name_eng
    if school_code: params["SD_SCHUL_CODE"] = school_code
    if goe_code: params["ATPT_OFCDC_SC_CODE"] = goe_code
    if goe_name: params["ATPT_OFCDC_SC_NM"] = GOE_NAME_DICT[goe_name]
    if local_name: params["LCTN_SC_NM"] = LOCAL_NAME_DICT[local_name]
    if school_type: params["SCHUL_KND_SC_MN"] = SCHOOL_TYPE_DICT[school_type]

    school_data = json.loads(requests.get("https://open.neis.go.kr/hub/schoolInfo", params=params).text)
    if "RESULT" in school_data:
        return {
            'success': "실패",
            'reason': nies_result_code_dict[school_data["RESULT"]["CODE"]]
        }

    school_count = school_data["schoolInfo"][0]["head"][0]["list_total_count"]
    school_data_list = school_data["schoolInfo"][1]["row"]

    return {
        'success': "성공",
        'count': school_count,
        'data': school_data_list
    }