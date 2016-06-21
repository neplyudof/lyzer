# Create your views here.
from os import path

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from memsis import volinterface
from memsis.models import DumpInfo

vol_init = volinterface.RunVol()
profiles = vol_init.profile_list()


def index_page(request):
    dump_list = DumpInfo.objects.all()
    if request.method == 'POST':
        file_path = request.POST['file_path']
        file_name = path.basename(file_path)
        profile = request.POST['profile']

        dump = DumpInfo(
            file_name=file_name,
            file_path=file_path,
            profile=profile,
            description=request.POST['description']
        )

        try:
            dump.full_clean()
            dump.save()
        except ValidationError:
            error = "This field cannot be blank."
            return render(request, 'index.html', {'error': error,
                                                  'dump_list': dump_list,
                                                  'profile_list': profiles})

        return redirect(dump)


    return render(request, 'index.html', {
        'dump_list': dump_list,
        'profile_list': profiles
    })


def analysis_page(request, file_name):
    return render(request, 'analysis.html')
