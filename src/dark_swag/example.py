from _example import example_router
from dark_swag import FastAPI


app = FastAPI(title='DarkSwag',
              description='<br>Example `/docs` using DarkSwag.',
              background_text='Swagger, but darker.',
              logo='/_fastapi_static/darkswag.svg')
app.include_router(example_router)

