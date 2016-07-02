# Create your views here.
import json
from os import path

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render

from memsis.forms import DumpInfoForm
from memsis.models import DumpInfo
from memsis.task import auto_detect_profile


def index_page(request):
    dump_list = DumpInfo.objects.all()
    modal_form = DumpInfoForm()

    if request.method == 'POST':
        file_path = request.POST['file_path']
        file_name = path.basename(file_path)
        profile = request.POST['profile']

        try:
            dump = DumpInfo(
                file_name=file_name,
                file_path=file_path,
                profile=profile,
                description=request.POST['description']
            )
            dump.full_clean()

            if profile == 'AutoDetect':
                prof, imageInfo = auto_detect_profile(file_path)
                dump.profile = prof
                imageInfo.dump_info = dump
                imageInfo.save()

            dump.save()
        except ValidationError:
            return HttpResponse(
                json.dumps({
                    "isSuccess": False,
                    "error_message": "Form Validation Error"
                })
            )

        return HttpResponse(
            json.dumps({
                "location": reverse('memsis:home'),
                "isSuccess": True}),
            content_type='application/json'
        )

    return render(request, 'index.html', {
        'dump_list': dump_list,
        'form': modal_form
    })


def analysis_page(request, file_name):
    return render(request, 'analysis.html')
