# coding=utf-8
from __future__ import print_function

import sys
import time
from os import path

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):
    server_url = None

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return

        super(FunctionalTest, cls).setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(FunctionalTest, cls).tearDownClass()

    def setUp(self):
        self.dump = ['/Users/J/Documents/ExampleImage/1.vmem', 'AutoDetect', 'test1']

        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_dump_list(self, file_path):
        file_name = path.basename(file_path)

        # 테이블에서 입력된 덤프파일 정보를 확인한다.
        # 파일 이름과 파일 경로만 확인
        table = self.browser.find_element_by_id('id_dump_list')
        # 테이블 항목 검증
        rows = table.find_elements_by_tag_name('tr')

        for cnt in range(0, len(rows)):
            if cnt == 0:
                self.assertTrue(u'#' in rows[cnt].text)
                self.assertTrue(u'파일 이름' in rows[cnt].text)
                self.assertTrue(u'파일 경로' in rows[cnt].text)
                self.assertTrue(u'프로파일' in rows[cnt].text)
                self.assertTrue(u'설명' in rows[cnt].text)
                continue

            tds = rows[cnt].find_elements_by_tag_name('td')
            self.assertEqual(cnt, int(tds[0].text))
            self.assertEqual(file_name, tds[1].text)
            self.assertEqual(file_path, tds[2].text)

    def add_dump_file(self, file_path, profile='AutoDetect', description='test'):
        # 메모리 덤프를 추가하기위해 Add 버튼을 클릭한다
        add_modal = self.browser.find_element_by_id('id_add_dump_btn')
        add_modal.click()

        # 모달 다이얼로그의 로딩을 잠시 기다림
        time.sleep(1)

        inputbox = self.browser.find_element_by_id('id_file_path')
        self.assertEqual(inputbox.get_attribute('placeholder'), u'메모리 덤프파일 절대 경로 입력')
        # 로컬 메모리 덤프파일 경로를 입력한다
        inputbox.send_keys(file_path)
        # 운영체제 프로파일을 선택한다
        selectbox = self.browser.find_element_by_id('id_profile')
        select_option = selectbox.find_element_by_tag_name('option')
        self.assertEqual(select_option.text, profile)
        # 덤프파일 설명 입력
        textarea = self.browser.find_element_by_id('id_description')
        self.assertEqual(textarea.get_attribute('name'), 'description')
        textarea.send_keys(description)
        # 제출 버튼 클릭으로 페이지가 갱신되며 메모리 덤프 목록에 추가된다
        # 제출 후 추가된 덤프파일 정보를 테이블에서 확인할 수 있다
        submit = self.browser.find_element_by_id('id_dump_submit')
        self.assertEqual(submit.get_attribute('type'), u'submit')
        submit.click()
        time.sleep(2)
