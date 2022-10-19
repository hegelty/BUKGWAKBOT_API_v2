from fastapi import FastAPI
import schoolmeal, dlsbook, timetable
import tools

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/schoolmeal")
async def showSchoolMeal(date: int, school_name: str = "", school_code: str = "", goe_code: str = "", local: str = "",
                         reload: bool = False):
    return schoolmeal.getMeal(meal_date=date, school_name=school_name, school_code=school_code, goe_code=goe_code,
                              local=local, reload=reload)


@app.get("/searchbook")
async def searchDLSBooks(school_name: str, local: str, query: str, option: str):
    return dlsbook.searchBooks(school_name=school_name, local=local, query=query, option=option)


@app.get("/schoolinfo")
async def showSchoolInfo(school_name: str, local_name: str):
    return tools.getSchoolInfo(school_name=school_name, local_name=local_name)


@app.get("/timetable")
async def showTimeTable(school_name: str, local_code: int = 0, school_code: int = 0, next_week: str = "0"):
    return timetable.getTimeTable(school_name=school_name, local_code=local_code, school_code=school_code, next_week=next_week)