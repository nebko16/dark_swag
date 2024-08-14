from _example import example_router
from dark_swag import FastAPI
from fastapi import Depends


description = '''
<br>
*Example* `/docs` using <u>DarkSwag</u>.

# h1 markdown

## h2 markdown

### h3 markdown

#### h4 markdown

**example things:**
- thing 1
- thing 2
- thing 3

```python
print('hello world!')
```

[source](https://github.com/nebko16/dark_swag)

<s>light mode</s>

'''

config = {
    'title': 'YourAppName',
    'description': description,
    'background_text': 'Your app, branded!',
    'logo': '/_fastapi_static/your_logo.svg',
    'logo_height': 70
}

app = FastAPI(**config)




app.include_router(example_router)

