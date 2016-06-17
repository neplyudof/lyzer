# Create your views here.
from django.shortcuts import render, redirect

from memsis.models import DumpInfo


def index_page(request):
    if request.method == 'POST':
        DumpInfo.objects.create(
            file_path=request.POST['file_path'],
            profile=request.POST['profile'],
            description=request.POST['description']
        )

        return redirect('/')

    dump_list = DumpInfo.objects.all()

    return render(request, 'index.html', {
        'dump_list': dump_list
    })
