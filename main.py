import os
from markdown2 import markdown_path
from shutil import rmtree
from jinja2 import Environment, PackageLoader

def read_file(page):
    return markdown_path(f'content/{page}.md', extras=['markdown-in-html', 'metadata'])

def write_file(page, html):
    with open(f'public/{page}.html', 'w') as file:
        file.write(html)

def render_jinja(temp_name, html):
    #load template
    env = Environment(loader=PackageLoader('main', 'templates'))
    template = env.get_template(f'{temp_name}.html')

    return template.render(content=html, meta=html.metadata)

def make_page(page):
    content_html = read_file(page)
    page_html = render_jinja('default', content_html)
    write_file(page, page_html)


pages = [{'name': os.path.splitext(page)[0]} for page in os.listdir('content')]
env = Environment(loader=PackageLoader('main', 'templates'))
template = env.get_template('nav_temp.html')
nav = template.render(pages=pages)
with open(f'templates/nav.html', 'w') as file:
    file.write(nav)

if os.path.exists('public'):
    rmtree('public', ignore_errors=True)
os.makedirs('public')

for page in os.listdir('content'):
    page = os.path.splitext(page)[0]
    make_page(page)