from fastapi import FastAPI
import schoolmeal, dlsbook
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

