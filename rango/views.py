from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserProfileForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from datetime import datetime
from search.views import searchcategory
from django.contrib.auth.models import User


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': pages_list}
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits

    response = render(request, 'rango/index.html', context_dict)

    return response


def about(request):
    visits = request.session.get('visits')
    if request.session.get('visits'):
        visits = request.session.get('visits')
    else:
        visits = 0

    return render(request, 'rango/about.html', {'chameleon':
                                                    'Chameleons are adapted for '
                                                    'climbing and visual hunting.',
                                                'visits': visits})


def category(request, category_name_slug):
    context_dict = {}
    if request.method == 'GET':
        try:
            category = Category.objects.get(slug=category_name_slug)
            context_dict['category_name'] = category.name
            pages = Page.objects.filter(category=category).order_by('-views')
            context_dict['pages'] = pages
            context_dict['category'] = category
            context_dict['category_name_slug'] = category.slug

        except Category.DoesNotExist:
            pass
        return render(request, 'rango/category.html', context_dict, )
    else:
        form = searchcategory(request)
        return render(request, 'search/search.html')


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


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()
    context_dict = {'form': form, 'category': cat}
    return render(request, 'rango/add_page.html', context_dict)


# def register(request):
#         registered = False
#         if request.method == 'POST':
#             user_form = UserForm(data=request.POST)
#             profile_form = UserProfileForm(data=request.POST)
#             if user_form.is_valid() and profile_form.is_valid():
#                 user = user_form.save()
#                 user.set_password(user_form)
#                 user.save()
#                 profile = profile_form.save(commit=False)
#                 profile.user = user
#                 if 'picture' in request.FILES:
#                     profile.picture = request.FILES['picture']
#                     profile.save()
#                     registered = True
#             else:
#                 print(user_form.errors, profile_form.errors)
#         else:
#             user_form = UserForm()
#             profile_form = UserProfileForm()
#         return render(request, 'rango/register.html',
#                       {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
#
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/rango/')
#             else:
#                 return HttpResponse('Your Rango account is disibled.')
#         else:
#             messages.add_message(request, settings.MY_SUPER_ERROR, 'Username or Password not correct')
#             return HttpResponseRedirect('/rango/login/')
#             # print("Invalid login details : {0}, {1}".format(username, password))
#             # return HttpResponse('Invalid login details supplied.')
#     else:
#         return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    context = {'message': "Since you're logged in, you can see this text!"}
    return render(request, 'rango/restricted.html', context)


# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect('/rango/')

def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)


@login_required
def profile_registration(request, id):
    profile = UserProfile.objects.get_or_create(UserProfile, user_id=id)
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()
                return render(request, 'rango/profile.html', {'profile': profile})
            profile.save()

    else:
        form = UserProfileForm()
        return render(request, 'rango/profile_registration.html')
    return render(request, 'rango/profile.html', {'profile': profile})


@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()

    return HttpResponse(likes)


