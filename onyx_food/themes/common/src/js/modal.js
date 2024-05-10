$(document).ready(function () {
    $('.btn-modal-open').click(function () {
        var url = $(this).data('modal');
        $.get(url, function (data) {
            $('#Modal .modal-content').html(data);
            $('#Modal').modal();
            $('#Modal').addClass('active');
            $('#overlay-modal').addClass('active');
            $('.btn-modal-close').click(function (event){
                $('#Modal').removeClass('active');
                $('#overlay-modal').removeClass('active');
            });
            $('#submit').click(function (event) {
                event.preventDefault();
                form = document.getElementById("ModalForm")
                const myFormData = new FormData(form)
                const formDataObj = Object.fromEntries(myFormData.entries());
                $.post(url, data = JSON.parse(JSON.stringify(formDataObj)), function (
                    data) {
                    if (JSON.parse(JSON.stringify(data)) == 'ok') {
                        console.log("WTF?!");
                        $('#Modal').removeClass('active');
                        $('#overlay-modal').removeClass('active');
                        location.reload();
                    } else {
                        var obj = JSON.parse(JSON.stringify(data));
                        $('.has-error').each(function() {
                            $(this).removeClass('has-error')
                        });
                        for (var key in obj) {
                            if (obj.hasOwnProperty(key)) {
                                var value = obj[key];
                                $('#' + key).addClass('has-error')
                            }
                        }                        
                    }
                })
            });
        })
    });

    $('.btn-order-open').click(function () {
        var url = $(this).data('modal');
        $.get(url, function (data) {
            $('#Modal .modal-content').html(data);
            $('#Modal').modal();
            $('#Modal').addClass('active');
            $('.btn-modal-close').click(function (event){
                $('#Modal').removeClass('active');
            });
            $('#submit').click(function (event) {
                event.preventDefault();
                form = document.getElementById("ModalForm")
                const myFormData = new FormData(form)
                const formDataObj = Object.fromEntries(myFormData.entries());
                $.post(url, data = JSON.parse(JSON.stringify(formDataObj)), function (
                    data) {
                    if (JSON.parse(JSON.stringify(data)) == 'ok') {
                        console.log("WTF?!");
                        $('#Modal').removeClass('active');
                        location.reload();
                    } else {
                        var obj = JSON.parse(JSON.stringify(data));
                        $('.has-error').each(function() {
                            $(this).removeClass('has-error')
                        });
                        for (var key in obj) {
                            if (obj.hasOwnProperty(key)) {
                                var value = obj[key];
                                $('#' + key).addClass('has-error')
                            }
                        }                        
                    }
                })
            });
        })
    });
});