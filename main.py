from fasthtml import common as fh

# Renders a person's details into a list item with a delete button
def render_person(person):
    pid = f'person-{person.pid}'
    delete_button = fh.A('Delete',hx_delete=f'/delete/{person.pid}',hx_swap='outerHTML',target_id=pid)

    return fh.Li(
        delete_button,
        f'[{person.pid}] Name: {person.name},Age: {person.age},Job: {person.job}',
        id=pid
    )

# Initialize the app, routing, database setup, and Person model
# 'live=True' enables live reloading
# 'db_file' specifies the SQLite DB file
# Defines model schema: pid, name, age, job with 'pid' as primary key
app ,rt, people, Person = fh.fast_app(live=True, db_file='data/people.db',
                                     pid=int, name=str,age=int,job=str,
                                     pk='pid',render=render_person)

# Home page route - shows a simple title and links
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

# Secondary page route - simple content with navigation link
@rt('/hello')
def hello():
    return fh.Div(
        fh.P('This is the hello page'),
        fh.A('Home',href='/')
    )

# Dynamic route - returns the first `n` Fibonacci numbers as a list
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
    
# GET route to display list of people and form to create a new person
@rt('/people',methods=['get'])
def list_people():
    create_form = fh.Form(
        fh.Group(
        fh.Input(placeholder="New Person Name",name='name'),
        fh.Input(placeholder="New Person Age",name='age',type='number'),
        fh.Input(placeholder="New Person Job",name='job'),
        fh.Button('Create')
        ),
        hx_post='/people',       # Submits form via POST to /people
        hx_swap='beforend',      # Appends new person to the end of the list
        target_id='people_list'  # Target list element to append into
    )
    return fh.Div(
        fh.Card(
            fh.Ul(*people(), id = 'people_list'),   # Display list of people
            header=create_form                      # Form as card header
        )
    )


# POST route - inserts new person into database and returns rendered item
@rt('/people',methods=['post'])
def create_person(person: Person):
    new_person = people.insert(person)
    return render_person(new_person)

# DELETE route - deletes a person by ID
@rt('/delete/{pid}',methods=['delete'])
def delete_person(pid: int):
    people.delete(pid)

# Starts the FastHTML server
fh.serve()
