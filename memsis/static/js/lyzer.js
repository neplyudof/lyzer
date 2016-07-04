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

    // 플러그인 명령 수행
    $('.run-plugin').click(function (event) {
        event.preventDefault();

        cmd = $(this).text();
        dump_id = $('#id_dump_id').val();

        $.ajax({
            url: '/runplugin/' + dump_id + '/' + cmd,
            type: 'GET',
            timeout: 20000,

            success: function (res) {
                var result = res['result'];
                // console.log(result);

                var columns = result['columns'];
                var rows = result['rows'];

                var col_list = [];
                for (var i in columns) {
                    col_list.push({
                        title: columns[i]
                    })
                }

                var result_table = $('#id_plugin_result');

                if ($.fn.DataTable.isDataTable(result_table)) {

                    // console.log('Datatable Destroy');
                    result_table.DataTable().clear();
                    result_table.DataTable().destroy();
                    result_table.children().remove();
                }

                console.log(rows);

                result_table
                    .DataTable({
                        data: rows,
                        columns: col_list,
                        retrieve: true,
                        bInfo: false,
                        destroy: true,
                        scrollX: true,
                        processing: true
                    });

            },

            error: function (xhr, err_msg, err) {
                console.log(err_msg);
                console.log(xhr.responseText);
                console.log(err);
                alert('아직 사용할 수 없는 플러그인입니다.');
            }
        })
    });

    // 메모리 덤프파일 저장
    $('#id-add-modal-form').submit(function (event) {
        // 이벤트에 의해 기본 동작이 수행되는 일을 방지할 수 있다
        // 일반적인 form 제출 방지
        event.preventDefault();

        var formValues = $(this).serializeObject();

        $.ajax({
            url: '/',
            type: 'POST',
            data: formValues,
            timeout: 20000,

            success: function (result) {
                // console.log(result)
                // var result = JSON.parse(result);

                if (result['isSuccess']) {
                    window.location.href = result['location'];
                } else {
                    //    Todo: 폼 필드 검증 에러처리 추가하기
                    alert(result['error_message'])
                }
            },

            error: function (xhr, err_msg, err) {
                //    Todo: 덤프파일 제출 후 서버 에러처리 추가하기
                console.log(err_msg);
                console.log(xhr.responseText);
                console.log(err);
            }
        })
    });

    $('#id_plugin_list').dataTable({
        "scrollY": "300px",
        "paging": false,
        "autoWidth": true,
        "dom": '<"pull-left"f><"pull-right"l>tip',
        "bInfo": false,
        "retrieve": true
    });

});