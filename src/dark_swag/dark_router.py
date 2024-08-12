from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .utils import render_css, load_static
from fastapi import FastAPI, APIRouter
from pathlib import Path



def get_dark_router(app: FastAPI,
                    logo: str | None = None,
                    background_text: str | None = None,
                    include_light_mode_toggle: bool = True) -> APIRouter:

    dark_router = APIRouter()
    static_dir = Path(__file__).parent / 'static'
    app.mount("/_fastapi_static", StaticFiles(directory=static_dir), name="static")

    light_toggle = ''
    dark_toggle = ''
    if include_light_mode_toggle:
        light_toggle = load_static('light_toggle.js', '')
        dark_toggle = load_static('dark_toggle.js', '')

    @dark_router.get("/docs", include_in_schema=False)
    async def dark_swag():
        swagger_html = get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title,
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/_fastapi_static/swagger-ui-bundle.js",
            swagger_css_url="/_fastapi_static/swagger-ui.css",
        )
        dark_css = render_css(logo=logo, background_text=background_text)
        swagger_html = swagger_html.body.decode()
        injection = f"<style>{dark_css}</style><script>{light_toggle}</script></head>"
        modified_html = swagger_html.replace("</head>", injection)
        return HTMLResponse(content=modified_html)

    if include_light_mode_toggle:
        @dark_router.get("/docs_light", include_in_schema=False)
        async def light_swag():
            swagger_response = get_swagger_ui_html(
                openapi_url=app.openapi_url,
                title=app.title,
                oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
                swagger_js_url="/_fastapi_static/swagger-ui-bundle.js",
                swagger_css_url="/_fastapi_static/swagger-ui.css",
            )
            light_css = render_css(logo=logo, background_text=background_text, mode='light')
            swagger_html = swagger_response.body.decode()
            injection = f"<style>{light_css}</style><script>{dark_toggle}</script></head>"
            injected_html = swagger_html.replace("</head>", injection)
            return HTMLResponse(content=injected_html)
    return dark_router
