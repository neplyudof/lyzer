# coding=utf-8
from __future__ import print_function

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # 메인 페이지에 접속하여 파일 경로를 입력하지 않고 이를 등록하려 한다
        # 입력 상자가 비어 있는 상태에서 제출 버튼을 클릭한다

        # 페이지가 새로고침되고 빈 아이템을 등록할 수 없다는
        # Todo: 폼 제출을 Ajax로 변경 후 모달창에 에러 메시지 출력하기!
        # 에러 메시지가 표시된다

        # 파일 경로를 입력하고 이번에는 정상 처리된다

        # 다시 의도적으로 파일 경로를 입력하지 않고 제출 버튼을 클릭한다

        # 다시 메인 페이지에 에러 메시지가 출력된다.

        # 파일 경로를 입력하면 정상 동작한다
        self.fail('write me')
