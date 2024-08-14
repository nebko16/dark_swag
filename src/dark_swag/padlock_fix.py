"""
Due to CSS SVG support being REALLY weak, especially Safari, using CSS to override an SVG path using the `d` attribute
isn't a reliable option, so the best alternative i could come up with was either swap the values in the source files,
or use CSS pseudoclasses to overlay the (IMO) incorrect icon states with the correct ones.

FastAPI's document on OpenAPI and Redoc assets:
  - https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/

At the time of writing this, the source files are here served from this CDN:
  - swagger_js_url = "https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"
  - swagger_css_url = "https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"

"""

import os

# todo: maybe create a build process to pull the originals down from the CDN
#       and process them to make this automated and repeatable


locked = "M15.8 8H14V5.6C14 2.703 12.665 1 10 1 7.334 1 6 2.703 6 5.6V6h2v-.801C8 3.754 8.797 3 10 3c1.203 0 2 .754 2 2.199V8H4c-.553 0-1 .646-1 1.199V17c0 .549.428 1.139.951 1.307l1.197.387C5.672 18.861 6.55 19 7.1 19h5.8c.549 0 1.428-.139 1.951-.307l1.196-.387c.524-.167.953-.757.953-1.306V9.199C17 8.646 16.352 8 15.8 8z"
unlocked = "M15.8 8H14V5.6C14 2.703 12.665 1 10 1 7.334 1 6 2.703 6 5.6V8H4c-.553 0-1 .646-1 1.199V17c0 .549.428 1.139.951 1.307l1.197.387C5.672 18.861 6.55 19 7.1 19h5.8c.549 0 1.428-.139 1.951-.307l1.196-.387c.524-.167.953-.757.953-1.306V9.199C17 8.646 16.352 8 15.8 8zM12 8H8V5.199C8 3.754 8.797 3 10 3c1.203 0 2 .754 2 2.199V8z"
placeholder = '__________placeholder__________'
filepaths = [
    'static/swagger-ui.js',
    'static/swagger-ui.js.map',
    'static/swagger-ui-bundle.js'
]


def swap_padlocks(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as fh:
            original_contents = fh.read()
            contents = original_contents
            contents = contents.replace(locked, placeholder)
            contents = contents.replace(unlocked, locked)
            contents = contents.replace(placeholder, unlocked)
        if contents and original_contents and contents != original_contents:
            with open('static/swagger-ui-bundle-fixed.js.map', 'w', encoding='utf-8') as fh2:
                fh2.write(contents)
    else:
        print(f"path doesn't exist: {filepath}")


if __name__ == '__main__':
    for _filepath in filepaths:
        swap_padlocks(_filepath)
