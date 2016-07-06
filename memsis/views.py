# coding=utf-8
# Create your views here.
import json
import os
import requests
from os import path

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render

from memsis.forms import DumpInfoForm
from memsis.models import DumpInfo, ImageInfo
from memsis.task import auto_detect_profile, get_plugin_list, update_config, tempdir
from memsis.volinterface import RunVol

# POST 요청
REST_CREATE_FILE = 'http://127.0.0.1/cuckoo/tasks/create/file'

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

            prof, image_info = auto_detect_profile(file_path)
            if profile == 'AutoDetect':
                dump.profile = prof

            dump.save()
            image_info.dump_info = dump
            image_info.save()
        except ValidationError:
            return HttpResponse(
                json.dumps({
                    "isSuccess": False,
                    "error_message": "Form Validation Error"
                })
            )

        return HttpResponse(
            json.dumps({
                "location": '/analysis/{0}'.format(dump.id),
                "isSuccess": True}),
            content_type='application/json'
        )

    return render(request, 'index.html', {
        'dump_list': dump_list,
        'form': modal_form
    })


def analysis_page(request, dump_id):
    dump = DumpInfo.objects.get(pk=dump_id)
    image_info = ImageInfo.objects.get(dump_info_id=dump_id)

    update_config({
        'location': str('file//' + dump.file_path),
        'profile': str(dump.profile)
    })

    return render(request,
                  'dump_information.html',
                  {
                      'dump': dump,
                      'image_info': image_info,
                      'plugin_list': get_plugin_list()
                  })


def run_plugin(request, dump_id, cmd):
    plugin_name = str(cmd)
    dump = DumpInfo.objects.get(pk=dump_id)

    init_vol = RunVol(profile=dump.profile, mem_path=dump.file_path)

    if 'procdump' == plugin_name:
        pid = request.GET['pid']
        print pid

        with tempdir() as dirpath:
            init_vol.run_plugin(plugin_name, pid=pid, dump_dir=dirpath)
            proc_dump = os.listdir(dirpath)[0]
            proc_path = os.path.abspath(os.path.join(dirpath, proc_dump))

            with open(proc_path, 'rb') as exe_file:
                multipart_file = {"file": ("temp_file_name", exe_file)}
                req = requests.post(REST_CREATE_FILE, files=multipart_file)
                json_decoder = json.JSONDecoder()
                result = json_decoder.decode(req.text)['task_id']

    else:
        result = init_vol.run_plugin(plugin_name)

    return HttpResponse(
        json.dumps({
            'result': result
        }),
        content_type='applicattion/json'
    )
