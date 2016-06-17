# Create your views here.
from django.shortcuts import render


def index_page(request):
    if request.method == 'POST':
        file_path = request.POST.get('file_path')
        profile = request.POST.get('profile')
        description = request.POST.get('description')
        return render(request, 'index.html', {
            'file_path': file_path,
            'profile': profile,
            'description': description
        })

    return render(request, 'index.html')
