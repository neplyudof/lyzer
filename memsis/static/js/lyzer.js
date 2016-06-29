$(function () {

    // Data to Json
    $.fn.serializeObject = function () {
        var o = {};
        var a = this.serializeArray();

        $.each(a, function () {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });

        return o;
    };

    $('#id-add-modal-form').submit(function (event) {
        // 이벤트에 의해 기본 동작이 수행되는 일을 방지할 수 있다
        // 일반적인 form 제출 방지
        event.preventDefault();

        var formValues = $(this).serializeObject();

        $.ajax({
            url: '/',
            type: 'POST',
            data: formValues,

            success: function (response) {
                var result = JSON.parse(response);

                if (result['isSuccess']) {
                    window.location.href = result['location'];
                } else {
                //    Todo: 폼 필드 검증 에러처리 추가하기
                    alert(result['error_message'])
                }
            },

            error : function (xhr, err_msg, err) {
            //    Todo: 덤프파일 제출 후 서버 에러처리 추가하기
            }
        })
    })

});