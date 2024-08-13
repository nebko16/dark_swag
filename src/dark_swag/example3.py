from dark_swag import get_dark_swagger_html
from fastapi import FastAPI



app = FastAPI(docs_url=None)


@app.get('/docs', include_in_schema=False)
async def dark_swagger():
    return get_dark_swagger_html(app,
                                 '/_fastapi_static/your_logo.svg',
                                 'Example 3',
                                 include_toggle=True)


@app.get('/docs_light', include_in_schema=False)
async def dark_swagger():
    return get_dark_swagger_html(app,
                                 '/_fastapi_static/your_logo.svg',
                                 'Example 3',
                                 include_toggle=True,
                                 mode='light')


@app.get('/test', tags=['default section'])
async def test():
    return {'hello': 'world'}


