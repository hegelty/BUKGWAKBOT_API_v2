from fastapi import FastAPI
import schoolmeal

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/schoolmeal")
async def showSchoolMeal(date: int, school_name: str = "", school_code: str = "", goe_code: str = "", local: str = "",
                         reload: bool = False):
    return schoolmeal.getMeal(meal_date=date, school_name=school_name, school_code=school_code, goe_code=goe_code,
                              local=local, reload=reload)
