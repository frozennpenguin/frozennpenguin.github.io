import os
from pathlib import Path
from markdown2 import markdown
from jinja2 import Environment, PackageLoader

def get_files(page):
    content = {}
    for md in os.listdir(f'content/{page}'):
        file_path = os.path.join(f'content/{page}', md)
        with open(file_path, 'r') as file:
            content[md] = markdown(file.read(), extras=['metadata'])
    return content

def load_temp():
    env = Environment(loader=PackageLoader('main', 'templates'))
    page_template = env.get_template('page.html')
    return page_template

#TODO make better
def render_jinja(template, content):
    data = [{'content':content[i], 'title':content[i].metadata['title']} for i in content]
    page_html = template.render(posts=data)
    return page_html

def make_page(page):
    content = get_files(page)
    template = load_temp()
    html = render_jinja(template, content)
    if not os.path.exists('output'):
        os.makedirs('output')
    with open(f'output/{page}.html', 'w') as file:
        file.write(html)

def build_site():
    for page in os.listdir(f'content'):
        make_page(page)

build_site()