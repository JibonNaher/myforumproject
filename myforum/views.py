from django.shortcuts import render

def post_list(request):
    return render(request, 'myforum/post_list.html', {})
