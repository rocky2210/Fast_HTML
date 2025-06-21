from fasthtml import common as fh

# App ,route
app, rt = fh.fast_app(live=True)

# Simple Hello world
# @rt('/')
# def index():
#     return fh.P('Hello World')

@rt('/')
def index():
    return fh.Titled(
        'My title',
        fh.Div(
            fh.P('Hello World!')
        ),
        fh.A('Rocky',href="https://example.com"),
        fh.A('Hello',href="/hello")
    )

@rt('/hello')
def hello():
    return fh.Div(
        fh.P('This is the hello page'),
        fh.A('Home',href='/')
    )

# Passing variables
@rt('/fibonacci/{n}')
def fibonacci(n:int):
    numbers = []
    
    a,b = 0,1
    for _ in range(n):
        numbers.append(a)
        b , a = a , a+ b
        
    return fh.Titled(
        'fibonacci numbers',
        fh.Ul(*[fh.Li(num) for num in numbers])
        )



fh.serve()
