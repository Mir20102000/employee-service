from fastapi import FastAPI, APIRouter

app = FastAPI(openapi_url="/api/v1/employees/openapi.json", docs_url="/api/v1/employees/docs")

employees_router = APIRouter()

employees = [
    {'companies_id': 1, 'name': 'Mbappe',
     'field': 'France',
     'salary': '50', 'work_experience': '34'},
    {'clubs_id': 2, 'name': 'Ronaldo',
     'field': 'Portugal',
     'salary': '5', 'work_experience': '26'},
    {'clubs_id': 3, 'name': 'Akinfeev',
     'field': 'Russia',
     'salary': '90', 'work_experience': '47'}
]


@employees_router.get("/")
async def read_employees():
    return employees

@employees_router.get("/{companies_id}")
async def read_employee(companies_id: int):
    for employee in employees:
        if employee['companies_id'] == companies_id:
            return employee
    return None

app.include_router(employees_router, prefix='/api/v1/employees', tags=['employees'])

if __name__ == '__main__':
    import uvicorn
    import os
    try:
        PORT = int(os.environ['PORT'])
    except KeyError as keyerr:
        PORT = 80
    uvicorn.run(app, host='0.0.0.0', port=PORT)