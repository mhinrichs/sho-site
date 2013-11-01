from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': pages_list, }

    for category in category_list:
        category.url = category.name.replace(' ', '_')
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return HttpResponse("Rango says: Here is the about page. <a href='/rango'>Index</a>")

def category(request, category_name_url):
    category_name_url = category_name_url
    category_name = category_name_url.replace('_', ' ')
    context_dict = {}
    context_dict['category_name'] = category_name
    context_dict['category_name_url'] = category_name_url
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category = category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    print(context_dict)
    return render(request, 'rango/category.html', context_dict)

def add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_url):
    category_name = category_name_url
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            cat = Category.objects.get(name = category_name_url.replace('_', ' '))
            page.category = cat
            page.save()
            return category(request, category_name)
        else:
            print(form.errors)

    else:
        form = PageForm()
        context_dict = {'category_name_url': category_name_url,
                    'category_name': category_name,
                    'form': form}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registered = False
    if request.method=='POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered=True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    #set up the context dict!
    context_dict = {}
    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['registered'] = registered

    return render(request, 'rango/register.html', context_dict)
