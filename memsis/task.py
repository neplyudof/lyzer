from memsis.models import ImageInfo
from memsis.volinterface import RunVol

init_vol = RunVol()


def auto_detect_profile(file_path):
    update_config({'location': str('file://' + file_path)})
    image_json = init_vol.run_plugin(str('imageinfo'))

    image_info = ImageInfo()

    columns = image_json.get('columns')
    rows = image_json.get('rows')[0]

    for key, value in zip(columns, rows):
        key = key.lower().replace(' ', '_')

        if '(' in key:
            key = key[:key.find('(')]
        if key.endswith('_'):
            key = key[:len(key) - 1]

        image_info.update_key(key, value)

    return image_info.suggested_profile.split(', ')[0], image_info


def update_config(config):
    init_vol.update_config(config)


def get_plugin_list():
    plugins = [plugin for plugin in init_vol.plugins.keys()
               if not plugin.startswith('mac') and not plugin.startswith('linux')]
    return sorted(plugins)
