# coding=utf-8
from __future__ import print_function

import time

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # 메인 페이지에 접속하여 파일 경로를 입력하지 않고 이를 등록하려 한다
        # 입력 상자가 비어 있는 상태에서 제출 버튼을 클릭한다
        self.browser.get(self.server_url)
        self.add_dump_file('')

        # 페이지가 새로고침되고 빈 아이템을 등록할 수 없다는
        # 에러 메시지가 표시된다
        self.browser.find_element_by_id('id_add_dump_btn').click()
        time.sleep(2)
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, 'This field cannot be blank.')
        self.browser.find_element_by_class_name('close').click()
        time.sleep(1)

        # 파일 경로를 입력하고 이번에는 정상 처리된다
        file_path = '/Users/J/Documents/ExampleImage/exam.vmem'
        self.add_dump_file(file_path)
        self.check_for_row_in_dump_list(file_path)

        # 파일 경로를 입력하면 정상 동작한다
        self.fail('write me')
