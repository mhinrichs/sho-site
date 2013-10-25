import os
import sys

def populate():
    python_cat = add_cat('Python', 128, 64)

    add_page(cat=python_cat,
             title="Official Python Tutorial",
             url="http://docs.python.org/2/tutorial/")

    add_page(cat=python_cat,
             title="How to Think like a Computer Scientist",
             url="http://www.greenteapress.com/thinkpython/")

    django_cat = add_cat("Django", 64, 32)

    add_page(cat=django_cat,
             title="Official Django Docs",
             url="http://docs.djangoproject.com/")

    frame_cat = add_cat("Other Frameworks", 32, 16)

    add_page(cat=frame_cat,
             title="Bottle",
             url="http://bottlepy.org")

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    return c

if __name__ == '__main__':
    print("Starting Rango Population Script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sho.settings')
    from rango.models import Category, Page
    populate()


