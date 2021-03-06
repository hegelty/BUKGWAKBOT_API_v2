# 북곽봇 API서버 V2
-----------
## 개요
북곽봇(https://github.com/Iroom-gbs/BUKGWAKBOT) 프로젝트에서 사용되는 API서버 V2<br>
Python FastAPI을 기반으로 개발 중
V1: https://github.com/hegelty/BUKGWAKBOT_API
## 기능
### 급식
요청 URL: /schoolmeal
|인자|분류|설명|예시|
|:---:|:---:|:---:|:---:|
|date|필수|급식 날짜(8자리 숫자)|20220425|
|school_name|선택|학교 이름|경기북과학고|
|school_code|선택|NIES 표준학교코드|9296071|
|goe_code|선택|NIES 교육청코드|J10|
|local|선택|지역|경기|
|reload|선택|급식 리로드|False|

#### 출력
성공시
```json
{
  "success": "성공",
  "count": count,
  "data": [
    {
      "type": 급식 종류,
      "menu": 메뉴,
      "allergy": 알레르기 정보,
      "nutrition": 영양 정보,
      "origin": 원산지 정보,
      "cal": 열량
    }
  ]
}
```
예시
```json
{
  "success": "성공",
  "count": 3,
  "data": [
    {
      "type": "조식",
      "menu": "혼합잡곡밥  \n근대된장국  \n시금치무침  \n모둠완자(고기/해물)  \n배추김치  \n우유  \n시리얼-후르츠링",
      "allergy": "지원 예정",
      "nutrition": "탄수화물(g) : 73.1\n단백질(g) : 21.3\n지방(g) : 19.3\n비타민A(R.E) : 383.9\n티아민(mg) : 0.7\n리보플라빈(mg) : 1.0\n비타민C(mg) : 40.3\n칼슘(mg) : 309.1\n철분(mg) : 5.8",
      "origin": "쌀 : 국내산\n김치류 : 국내산\n고춧가루(김치류) : 국내산\n쇠고기(종류) : 국내산(한우)\n돼지고기 : 국내산\n닭고기 : 국내산\n오리고기 : 국내산\n쇠고기 식육가공품 : 국내산\n돼지고기 식육가공품 : 국내산\n닭고기 식육가공품 : 국내산\n오리고기 가공품 : 국내산\n낙지 : 국내산\n고등어 : 국내산\n갈치 : 국내산\n오징어 : 국내산\n꽃게 : 국내산\n참조기 : 국내산\n콩 : 국내산",
      "cal": "553.2 Kcal"
    },
    {
      "type": "중식",
      "menu": "율무밥  \n청국장찌개  \n베이컨감자채볶음  \n연어스테이크  \n배추김치  \n과일-파인애플",
      "allergy": "지원 예정",
      "nutrition": "탄수화물(g) : 105.5\n단백질(g) : 28.6\n지방(g) : 23.3\n비타민A(R.E) : 152.9\n티아민(mg) : 0.6\n리보플라빈(mg) : 0.4\n비타민C(mg) : 54.2\n칼슘(mg) : 165.2\n철분(mg) : 4.6",
      "origin": "쌀 : 국내산\n김치류 : 국내산\n고춧가루(김치류) : 국내산\n쇠고기(종류) : 국내산(한우)\n돼지고기 : 국내산\n닭고기 : 국내산\n오리고기 : 국내산\n쇠고기 식육가공품 : 국내산\n돼지고기 식육가공품 : 국내산\n닭고기 식육가공품 : 국내산\n오리고기 가공품 : 국내산\n낙지 : 국내산\n고등어 : 국내산\n갈치 : 국내산\n오징어 : 국내산\n꽃게 : 국내산\n참조기 : 국내산\n콩 : 국내산",
      "cal": "730.1 Kcal"
    },
    {
      "type": "석식",
      "menu": "후리카케볶음밥  \n실파계란국  \n로제떡볶이  \n모둠튀김(채소/김말이)  \n꼬들단무지 과  \n포도폴라포아이스크림",
      "allergy": "지원 예정",
      "nutrition": "탄수화물(g) : 178.8\n단백질(g) : 30.9\n지방(g) : 38.8\n비타민A(R.E) : 488.6\n티아민(mg) : 0.5\n리보플라빈(mg) : 0.8\n비타민C(mg) : 42.0\n칼슘(mg) : 188.1\n철분(mg) : 12.2",
      "origin": "쌀 : 국내산\n김치류 : 국내산\n고춧가루(김치류) : 국내산\n쇠고기(종류) : 국내산(한우)\n돼지고기 : 국내산\n닭고기 : 국내산\n오리고기 : 국내산\n쇠고기 식육가공품 : 국내산\n돼지고기 식육가공품 : 국내산\n닭고기 식육가공품 : 국내산\n오리고기 가공품 : 국내산\n낙지 : 국내산\n고등어 : 국내산\n갈치 : 국내산\n오징어 : 국내산\n꽃게 : 국내산\n참조기 : 국내산\n콩 : 국내산",
      "cal": "1159.7 Kcal"
    }
  ]
}
```
#### 실패시
```json
{
  "success": "실패",
  "reason": 이유
}
```
예시
```json
{
  "success": "실패",
  "reason": "학교를 찾을 수 없습니다."
}
```

## 개발예정
- [ ] 시간표(컴시간/나이스)
- [ ] 학교 정보
- [x] 도서검색(DLS)
- [ ] 멜론 노래 검색, 가사
- [ ] 멜론 차트