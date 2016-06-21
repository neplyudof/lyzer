# Create your views here.
from os import path

from django.shortcuts import render, redirect

from memsis import volinterface
from memsis.models import DumpInfo


def index_page(request):
    vol_init = None

    if request.method == 'POST':
        file_path = request.POST['file_path']
        file_name = path.basename(file_path)
        profile = request.POST['profile']
        if profile == 'AutoDetect':
            vol_init = volinterface.RunVol(mem_path=file_path)
            profile = vol_init.auto_detect_profile()

        DumpInfo.objects.create(
            file_name=file_name,
            file_path=file_path,
            profile=profile,
            description=request.POST['description']
        )

        return redirect('/')

    vol_init = volinterface.RunVol()
    profiles = vol_init.profile_list()
    dump_list = DumpInfo.objects.all()

    return render(request, 'index.html', {
        'dump_list': dump_list,
        'profile_list': profiles
    })


def analysis_page(request, file_name):
    return render(request, 'analysis.html')
