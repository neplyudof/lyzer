# coding=utf-8
import StringIO
import copy
import json
import logging
import os
import sys

# Volatility Import

import volatility.conf as conf
import volatility.obj as obj
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace
import volatility.constants as constants
import volatility.debug as debug

# Need to do this before importing volatility

volrc_file = os.path.join(os.path.expanduser('~'), ".volatilityrc")
# noinspection PyUnresolvedReferences
plugin_dir = os.path.join(os.path.realpath(__file__), "../plugins")

# Platform PATH seperator
seperator = ':'
if sys.platform.startswith('win'):
    seperator = ':'

# Volatility 설정 파일
if os.path.exists(volrc_file):
    with open(volrc_file, 'ab+') as out:
        if plugin_dir not in out.read():
            output = '{0}{1}'.format(seperator, plugin_dir)
            out.write(output)
else:
    # Create new file
    with open(volrc_file, 'w') as out:
        output = '[DEFAULT]\nPLUGINS = {0}'.format(plugin_dir)
        out.write(output)

# import volatility.utils as utils

# 로거 설정
logger = logging.getLogger(__name__)


# Volatility debug 설정 변경
# Volatility 기본 설정으로 에러 발생시 sys.exit(1) 호출로 프로세스 종료
def new_error(msg):
    raise Exception(msg)


debug.error = new_error

# Volatility 버전 정보
vol_version = constants.VERSION


# Volatility 명령 수행 클래스
class RunVol:
    def __init__(self, profile='WinXPSP2x86', mem_path=''):
        """
        Volatility 기본 설정  초기화
        :param profile:
        :param mem_path:
        """

        # Volatility 디버그 모듈 설정
        debug.setup()
        # 사용 가능한 플러그인 모듈 임포트
        registry.PluginImporter()

        self.memdump = mem_path
        self.osprofile = profile
        self.config = None
        self.addr_space = None
        self.plugins = None
        self.plugin_list = []

        self.init_config()

    def init_config(self):
        """
        Volatility 설정 초기화
        :return:
        """

        if self.config is not None and self.addr_space is not None:
            return self.config

        self.config = conf.ConfObject()
        self.config.optparser.set_conflict_handler("resolve")

        registry.register_global_options(self.config, commands.Command)
        registry.register_global_options(self.config, addrspace.BaseAddressSpace)

        base_conf = {
            "profile": "WinXPSP2x86",
            "use_old_as": None,
            "kdbg": None,
            "help": False,
            "kpcr": None,
            "tz": None,
            "pid": None,
            "output_file": None,
            "physical_offset": None,
            "conf_file": None,
            "dtb": None,
            "output": None,
            "info": None,
            "location": "file://" + self.memdump,
            "plugins": 'plugins',
            "debug": 4,
            "filename": None,
            "cache_directory": None,
            "verbose": None,
            "write": False
        }

        if self.osprofile:
            base_conf["profile"] = self.osprofile

        for key, value in base_conf.items():
            self.config.update(key, value)

        # 사용가능한 플러그인 목록 저장
        # self.plugins = Dictionary
        #   key: 플러그인 클래스 이름
        #   value: 플러그인 클래스 인스턴스
        self.plugins = registry.get_plugin_classes(commands.Command, lower=True)

        profs = registry.get_plugin_classes(obj.Profile)
        profile = profs[self.config.PROFILE]()

        # self.plugins에서 플러그인 리스트 추출
        for cmd_name, command in self.plugins.items():
            if command.is_valid_profile(profile):
                self.plugin_list.append(cmd_name)

        return self.config

    def profile_list(self):
        """
        사용가능한 프로파일 리스트를 정렬 후 반환
        :return: sorted profile list
        """

        prof_list = ['AutoDetect']
        profs = registry.get_plugin_classes(obj.Profile)
        for profile in profs.iterkeys():
            prof_list.append(profile)

        return sorted(prof_list)

    def run_plugin(self, plugin_name, dump_dir=None, pid=None,
                   plugin_options=None, output_style="json"):

        """
        Volatility 명령 수행
        :param pid: 프로세스 ID
        :param plugin_name: 수행할 명령어
        :param dump_dir: 덤프 관련 명령어 수행 후 덤프 파일 저장 경로
        :param plugin_options: 명령어 옵션(Dictionary)
        :param output_style: 명령 수행 결과 출력 형식
        :return:
        """
        # Todo: json 외 명령 결과 출력 형식 구현

        if plugin_name in self.plugin_list:
            # commnad: Plugin Class
            command = self.plugins[plugin_name]

            # Set Config options
            self.config.PID = pid
            self.config.DUMP_DIR = dump_dir
            if plugin_options:
                for option, value in plugin_options.iteritems():
                    logger.debug('Setting Config {0} to {1}'.format(option, value))
                    self.config.update(option, value)

            if output_style == 'json':
                return self._get_json(command)

    def _get_json(self, plugin_class):
        """
        Return json output for a plugin
        :param plugin_class: Plugin Class
        :return: Json 포맷의 명령어 수행 결과
        """

        strio = StringIO.StringIO()
        plugin = plugin_class(copy.deepcopy(self.config))
        plugin.render_json(strio, plugin.calculate())

        return json.loads(strio.getvalue())

    def auto_detect_profile(self):
        json = self.run_plugin('imageinfo')

        print json

        return 'AutoDetect'


def profile_list():
    """
    사용가능한 프로파일 리스트를 정렬 후 반환
    :return: sorted profile list
    """

    vol_init = RunVol()

    return vol_init.profile_list()