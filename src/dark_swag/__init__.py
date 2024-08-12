from fastapi import FastAPI as OriginalFastAPI, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from jinja2 import FileSystemLoader
import jinja2


dark_router = APIRouter()




class FastAPI(OriginalFastAPI):
    def __init__(self,
                 logo: str | None = None,
                 background_text: str | None = None,
                 *args,
                 **kwargs):

        kwargs['docs_url'] = None
        super().__init__(*args, **kwargs)
        self.mount("/_fastapi_static", StaticFiles(directory="static"), name="static")
        self.logo: str | None = logo
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
        dark_css = render_css(logo=self.logo, background_text=self.background_text)
        swagger_html = swagger_response.body.decode()
        injection = f"<style>{dark_css}</style><script>{load_static('light_toggle.js', '')}</script></head>"
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
                               background_text=self.background_text,
                               mode='light')
        swagger_html = swagger_response.body.decode()
        injection = f"<style>{light_css}</style><script>{load_static('dark_toggle.js', '')}</script></head>"
        injected_html = swagger_html.replace("</head>", injection)
        return HTMLResponse(content=injected_html)
        # return swagger_html


def render_css(logo: str | None = None,
               background_text: str | None = None,
               mode: str = 'dark') -> str:
    j2: jinja2.Environment = jinja2.Environment(loader=FileSystemLoader('.'))
    if mode == 'dark':
        root_template = j2.get_template('static/dark.css.jinja2')
        fill_color = 'white'
    else:
        root_template = j2.get_template('static/light.css.jinja2')
        fill_color = 'black'

    logo_css: str = ''
    if logo:
        logo_template = j2.get_template('static/logo.css.jinja2')
        logo_css = logo_template.render({'logo': logo})

    bg_text_css: str = ''
    if background_text:
        bg_text_template = j2.get_template('static/background_text.css.jinja2')
        bg_text_css = bg_text_template.render({
            'background_text': background_text,
            'fill_color': fill_color
        })

    dark_css: str = root_template.render({
        'logo': logo_css,
        'background_text': bg_text_css
    })
    return dark_css


def get_dark_swagger_html(app: FastAPI,
                          logo: str | None = None,
                          background_text: str | None = None,
                          include_toggle: bool = False,
                          mode: str = 'dark') -> HTMLResponse:

    app.mount("/_fastapi_static", StaticFiles(directory="static"), name="static")
    swagger_response: HTMLResponse = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url='/_fastapi_static/swagger-ui-bundle.js',
        swagger_css_url='/_fastapi_static/swagger-ui.css'
    )
    if include_toggle:
        if mode == 'dark':
            toggle_js = load_static('light_toggle.js', '')
        else:
            toggle_js = load_static('dark_toggle.js', '')
    dark_css = render_css(logo=logo, background_text=background_text, mode=mode)
    swagger_html = swagger_response.body.decode()
    injection = f"<style>{dark_css}</style><script>{toggle_js}</script></head>"
    injected_html = swagger_html.replace("</head>", injection)
    return HTMLResponse(content=injected_html)


def load_static(filename: str, default: str = '') -> str:
    with open(f"static/{filename}", 'r', encoding='utf-8') as file:
        static = file.read()
    if not static:
        return default
    return static
