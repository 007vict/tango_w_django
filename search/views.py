from django.shortcuts import render
from django.db.models import Q
from rango.models import Category, Page


def searchposts(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(name__icontains=query)
            lookups1 = Q(title__icontains=query)

            results = Category.objects.filter(lookups).distinct()
            results1 = Page.objects.filter(lookups1).distinct()

            context = {'results': results,
                       'results1': results1,
                       'submitbutton': submitbutton,
                       }

            return render(request, 'search/search.html', context,)
        else:
            return render(request, 'search/search.html')

    else:
        return render(request, 'search/search.html')

def searchcategory(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(name__icontains=query)

            results = Category.objects.filter(lookups).distinct()

            context = {'results': results,
                       'submitbutton': submitbutton,
                       }

            return render(request, 'search/search.html', context,)
        else:
            return render(request, 'search/search.html')

    else:
        return render(request, 'search/search.html')







