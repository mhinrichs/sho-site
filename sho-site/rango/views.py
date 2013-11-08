from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, redirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.bing_search import run_query
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

def query_visits(request):
    if request.session.get('visits'):
        visits = request.session.get('visits')
    if request.session.get('last_visit'):
        last_visit = request.session['last_visit']
        if last_visit < (datetime.now() - timedelta(1)):
           request.session['visits'] += 1
    else:
        request.session['last_visit'] = datetime.now()
        request.session['visits'] = 1
    results = {}
    results['visits'] = request.session['visits']
    results['last_visit'] = request.session['last_visit']
    request.session['last_visit'] = datetime.now()

    return results

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': pages_list, }
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    context_dict.update(query_visits(request))
    return render(request, 'rango/index.html', context_dict)

@login_required
def user_logout(request):
    logout(request)
    return redirect(index)

def about(request):
    context_dict = {}
    context_dict.update(query_visits(request))
    return render(request, 'rango/about.html', context_dict)

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

@login_required
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

@login_required
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
            user = user_form.save()
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

def user_login(request):
    context_dict = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', context_dict)

def search(request):
    result_list = []
    context_dict = {}

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            print(result_list)
            context_dict['result_list'] = result_list

    return render(request, 'rango/search.html', context_dict)

