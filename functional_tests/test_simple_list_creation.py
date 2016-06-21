# coding=utf-8
from __future__ import print_function

from os import path
from urlparse import urlparse

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_visit_index_page(self):
        # memsys를 처음 사용하는 사용자가 메인 페이지를 방문한다
        self.browser.get(self.server_url)

        # 웹 페이지 타이틀과 헤더에 'Lyzer'를 표시하고 있다
        self.assertIn(u'Lyzer', self.browser.title)
        # header_text = self.browser.find_element_by_class_name('navbar-brand')
        # self.assertIn('Lyzer', header_text)

        # 분석할 덤프파일을 2회 추가한다
        # 입력내용
        #   메모리 덤프파일 로컬 경로
        #   운영체제 프로파일 정보
        #   덤프파일 설명
        for dump in self.dump_lists:
            # 덤프 파일을 저장한다
            self.add_dump_file(dump[0], dump[1], dump[2])

        # 테이블에서 입력된 덤프 파일을 확인한다
        self.check_for_row_in_dump_list()

        # 테이블에 입력된 정보가 있는지 확인한다
        table = self.browser.find_element_by_id('id_dump_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(len(rows) == len(self.dump_lists) + 1)

        # 테이블에 입력된 항목을 클릭하면 메모리 덤프를 분석할 수 있는
        # 새로운 URL로 바뀐다
        # 첫 번째 항목을 선택한다
        link_text = path.basename(self.dump_lists[1][0])
        link = self.browser.find_element_by_link_text(link_text)
        link.click()
        self.assertRegexpMatches(urlparse(self.browser.current_url).path, '/analysis/' + link_text)

        # 새로운 기능 테스트 추가하기
        self.fail('Finish the test!')
