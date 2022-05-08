from bs4 import BeautifulSoup
from tools import *

DLS_DOMAINS_DICT = {'서울특별시': 'https://reading.ssem.or.kr',
                    '부산광역시': 'https://reading.pen.go.kr',
                    '대구광역시': 'https://reading.edunavi.kr',
                    '인천광역시': 'https://book.ice.go.kr',
                    '광주광역시': 'https://book.gen.go.kr',
                    '대전광역시': 'https://reading.edurang.net',
                    '울산광역시': 'https://reading.ulsanedu.kr',
                    '세종특별자치시': 'https://reading.sje.go.kr',
                    '경기도': 'https://reading.gglec.go.kr',
                    '강원도': 'https://reading.gweduone.net',
                    '충청북도': 'https://reading.cbe.go.kr',
                    '충청남도': 'https://reading.edus.or.kr',
                    '전라북도': 'https://reading.jbedu.kr',
                    '전라남도': 'https://reading.jnei.go.kr',
                    '경상북도': 'https://reading.gyo6.net',
                    '경상남도': 'https://reading.gne.go.kr',
                    '제주특별자치도': 'https://reading.jje.go.kr'}
URL_MAIN = "/r/newReading/main/main.jsp"
URL_FIND_SCHOOL = "/r/newReading/search/schoolListData.jsp"
URL_SEARCH_BOOKS = "/r/newReading/search/schoolSearchResult.jsp"
DLS_COOKIES = {
    'D_VISITOR_ID': 'df49d637-796f-09d0-932d-fd58ad5cf7f5',
    'JSESSIONID': 'euUDAtEPLQFwKixczqduPQw50Ed57a27AznTBH9VQwZqCVvA7Ca61Yuc4qgSyAbL.wasdls02_servlet_engine2'
}
DLS_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
}


def findSchool(local, school):
    domain = DLS_DOMAINS_DICT[local]
    resp = requests.post(domain + URL_FIND_SCHOOL, cookies=DLS_COOKIES, data={'txtSearchWord': "도서검색", 'schoolSearch': school}, headers=DLS_HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    school_list = soup.find_all(class_="school_name")
    if len(school_list) <= 1:
        return -1
    schoolCode = int(str(school_list[1]).strip().split("selectSchool('")[1].split("',")[0])
    return schoolCode


def searchBooks(school_name, local, query, option):
    options = {
        '전체': 'ALL',
        '자료명': 'TITL',
        '저자': 'AUTH',
        '출판사': 'PUBL',
        '주제': 'SUBJ',
        'ISBN': 'ISBN',
        'KDCN': 'KDCN'
    }
    option = options.get(option)
    if not option:
        return {
            'success': '실패',
            'reason': '검색 옵션을 선택하세요.'
        }

    if local not in LOCAL_NAME_DICT:
        return {
            'success': '실패',
            'reason': '지역을 찾을 수 없습니다.'
        }
    elif LOCAL_NAME_DICT[local] not in DLS_DOMAINS_DICT:
        return {
            'success': '실패',
            'reason': '지역을 찾을 수 없습니다.'
        }
    local = LOCAL_NAME_DICT[local]

    school_code = findSchool(local, school_name)
    domain = DLS_DOMAINS_DICT[local]
    data = {
        'currentPage': '1',
        'searchPageName': "schoolSearchForm",
        'schSchoolCode': school_code,
        'division1': option,
        'searchCon1': query,
        'connect1': 'A',
        'division2': 'TITL',
        'searchCon2': '',
        'connect2': 'A',
        'division3': 'PUBL',
        'searchCon3': '',
        'dataType': 'ALL',
        'lineSize': 50,
        'cbSort': 'STIT'
    }
    resp = requests.post(domain + URL_SEARCH_BOOKS, cookies=DLS_COOKIES, data=data, headers=DLS_HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    images = []
    for i in soup.select("div.bd_list_no > div.book_image > img"):
        src = domain + i.attrs['src']
        if 'thumbNail' not in src:
            src = None
        images.append(src)
    titles = []
    for i in soup.select("div.bd_list_title > a > span"):
        titles.append(i.text)
    authors = []
    for i in soup.select("div.bd_list_info > div.bd_list_writer > span.dd"):
        authors.append(i.text.strip().replace("\r", "").replace("\n", "").replace("\t", ""))

    publishers = []
    years = []
    for i in soup.select("div.bd_list_info > div.bd_list_company > span.dd"):
        try: publishers.append(i.text.split('(')[0].strip())
        except: publishers.append('')
        try: years.append(int(i.text.split('(')[1].split(')')[0]))
        except: years.append('')
    KDCs = []
    for i in soup.select("div.bd_list_info > div.bd_list_year > span.dd"):
        KDCs.append(i.text.strip().replace("\r", "").replace("\n", "").replace("\t", ""))
    locations = []
    for i in soup.select("div.bd_list_info > div.bd_list_location > span.dd"):
        locations.append(i.text.replace("\r", "").replace("\n", "").replace("\t", ""))
    stats = []
    for i in soup.select("div.book_save > div "):
        stats.append(i.text.split('\n')[1])

    result = {
        "success": "성공",
        "libraryName": soup.select_one("span.school_name").text,
        "local": LOCAL_NAME_DICT[local],
        "libraryCode": school_code,
        "count": len(titles),
        "books": []
    }
    for i in range(0, len(titles)):
        info = {
            "title": titles[i],
            "author": authors[i],
            "publisher": publishers[i],
            "year": years[i],
            "KDC": KDCs[i],
            "location": locations[i],
            "stat": stats[i],
            "image": images[i]
        }
        result["books"].append(info)

    return result