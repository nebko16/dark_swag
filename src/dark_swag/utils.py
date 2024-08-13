from jinja2 import Environment, FileSystemLoader
import importlib.resources



def render_css(logo: str | None = None,
               background_text: str | None = None,
               mode: str = 'dark',
               logo_height: int = 60) -> str:

    with importlib.resources.path('dark_swag', 'static') as static_path:
        template_loader = FileSystemLoader(static_path)
        j2 = Environment(loader=template_loader)

        if mode == 'dark':
            root_template = j2.get_template('dark.css.jinja2')
            fill_color = 'white'
        else:
            root_template = j2.get_template('light.css.jinja2')
            fill_color = 'black'

        logo_css: str = ''
        if logo:
            logo_template = j2.get_template('logo.css.jinja2')
            logo_css = logo_template.render({
                'logo': logo,
                'logo_height': logo_height
            })

        bg_text_css: str = ''
        if background_text:
            bg_text_template = j2.get_template('background_text.css.jinja2')
            bg_text_css = bg_text_template.render({
                'background_text': background_text,
                'fill_color': fill_color
            })

        dark_css: str = root_template.render({
            'logo': logo_css,
            'background_text': bg_text_css
        })
        return dark_css


def load_static(filename: str, default: str = '') -> str:
    try:
        with importlib.resources.open_text('dark_swag.static', filename, encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return default
