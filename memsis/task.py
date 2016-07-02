import json

from memsis.models import ImageInfo
from memsis.volinterface import RunVol


def auto_detect_profile(file_path):
    init_vol = RunVol(mem_path=file_path)
    image_json = init_vol.run_plugin('imageinfo')

    parsed_json = json.loads(image_json)

    imageInfo = ImageInfo()

    for key, value in zip(parsed_json['columns'], parsed_json['rows'][0]):
        key = key.lower().replace(' ', '_')
        if '(' in key:
            key = key[:key.find('(')]
        if key.endswith('_'):
            key = key[:len(key) - 1]

        imageInfo.update_key(key, value)

    return imageInfo.suggested_profile[0], imageInfo