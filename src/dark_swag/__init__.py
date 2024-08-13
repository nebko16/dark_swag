from fastapi import FastAPI as OriginalFastAPI, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .utils import render_css, load_static
from .dark_router import get_dark_router
from pathlib import Path



dark_router = APIRouter()



class FastAPI(OriginalFastAPI):
    def __init__(self,
                 logo: str | None = None,
                 background_text: str | None = None,
                 logo_height: int = 60,
                 *args,
                 **kwargs):

        kwargs['docs_url'] = None
        super().__init__(*args, **kwargs)
        static_dir = Path(__file__).parent / 'static'
        self.mount("/_fastapi_static", StaticFiles(directory=static_dir), name="static")
        self.logo: str | None = logo
        self.logo_height: int = logo_height
        self.background_text: str | None = background_text
        self.add_api_route(
            '/docs',
            self.dark_swagger_html,
            methods=['GET'],
            include_in_schema=False)
        self.add_api_route(
            '/docs_light',
            self.default_swagger_html,
            methods=['GET'],
            include_in_schema=False)

    async def dark_swagger_html(self) -> HTMLResponse:
        swagger_response: HTMLResponse = get_swagger_ui_html(
            openapi_url=self.openapi_url,
            title=self.title,
            oauth2_redirect_url=self.swagger_ui_oauth2_redirect_url,
            swagger_js_url='/_fastapi_static/swagger-ui-bundle.js',
            swagger_css_url='/_fastapi_static/swagger-ui.css'
        )
        dark_css = render_css(logo=self.logo,
                              logo_height=self.logo_height,
                              background_text=self.background_text)
        swagger_html = swagger_response.body.decode()
        script: str = load_static('light_toggle.js', '')
        injection = f"<style>{dark_css}</style><script>{script}</script></head>"
        injected_html = swagger_html.replace("</head>", injection)
        return HTMLResponse(content=injected_html)

    async def default_swagger_html(self) -> HTMLResponse:
        swagger_response: HTMLResponse = get_swagger_ui_html(
            openapi_url=self.openapi_url,
            title=self.title,
            oauth2_redirect_url=self.swagger_ui_oauth2_redirect_url,
            swagger_js_url='/_fastapi_static/swagger-ui-bundle.js',
            swagger_css_url='/_fastapi_static/swagger-ui.css'
        )
        light_css = render_css(logo=self.logo,
                               logo_height=self.logo_height,
                               background_text=self.background_text,
                               mode='light')
        swagger_html = swagger_response.body.decode()

        script: str = load_static('dark_toggle.js', '')
        injection = f"<style>{light_css}</style><script>{script}</script></head>"
        injected_html = swagger_html.replace("</head>", injection)
        return HTMLResponse(content=injected_html)
        # return swagger_html


def get_dark_swagger_html(app: FastAPI,
                          logo: str | None = None,
                          background_text: str | None = None,
                          include_toggle: bool = False,
                          mode: str = 'dark',
                          logo_height: int = 60) -> HTMLResponse:

    static_dir = Path(__file__).parent / 'static'
    app.mount("/_fastapi_static", StaticFiles(directory=static_dir), name="static")
    swagger_response: HTMLResponse = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url='/_fastapi_static/swagger-ui-bundle.js',
        swagger_css_url='/_fastapi_static/swagger-ui.css'
    )
    if include_toggle:
        if mode == 'dark':
            script: str = load_static('light_toggle.js', '')
        else:
            script: str = load_static('dark_toggle.js', '')

    dark_css = render_css(logo=logo,
                          logo_height=logo_height,
                          background_text=background_text,
                          mode=mode)
    swagger_html = swagger_response.body.decode()
    injection = f"<style>{dark_css}</style><script>{script}</script></head>"
    injected_html = swagger_html.replace("</head>", injection)
    return HTMLResponse(content=injected_html)
