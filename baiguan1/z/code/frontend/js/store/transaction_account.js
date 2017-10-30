$(document).ready(function () {

    $("#wechat_form").submit(function () {

        var options = {
            // target:        '#output1',   // target element(s) to be updated with server response
            beforeSubmit: wechatShowRequest,  // pre-submit callback
            success: wechatShowResponse,  // post-submit callback

            // other available options:
            url: 'add-transaction-accounts',         // override for form's 'action' attribute
            type: 'post',        // 'get' or 'post', override for form's 'method' attribute
            dataType: 'json',        // 'xml', 'script', or 'json' (expected server response type)
            //clearForm: true        // clear all form fields after successful submit
            //resetForm: true        // reset the form after successful submit

            // $.ajax options can be used here too, for example:
            //timeout:   3000
            data: {'platform': 'wechat'}
        };
        $(this).ajaxSubmit(options);
        return false;
    });
    $("#alipay_form").submit(function () {

        var options = {
            // target:        '#output1',   // target element(s) to be updated with server response
            beforeSubmit: alipayShowRequest,  // pre-submit callback
            success: alipayShowResponse,  // post-submit callback

            // other available options:
            url: 'add-transaction-accounts',         // override for form's 'action' attribute
            type: 'post',        // 'get' or 'post', override for form's 'method' attribute
            dataType: 'json',        // 'xml', 'script', or 'json' (expected server response type)
            //clearForm: true        // clear all form fields after successful submit
            //resetForm: true        // reset the form after successful submit

            // $.ajax options can be used here too, for example:
            //timeout:   3000
            data: {'platform': 'alipay'}
        };
        $(this).ajaxSubmit(options);
        return false;
    });

    $("input").keydown(function () {

        $(this).parent().attr('class', 'field');
    });

    function wechatShowResponse(responseText, statusText, xhr) {
        if (responseText.success == 1) {
            $('.ui.page.dimmer').dimmer('hide');
            location.reload();
        } else {
            $('.ui.page.dimmer').dimmer('hide');

            alert("验证未通过，请重新填写。");
        }
    }

    function wechatShowRequest(formData, jqForm, options) {
        var send = true;
        $("#wechat_form").find("input").each(function () {
            if ($.trim($(this).val()) === "") {
                $(this).parent().attr('class', 'field error');
                send = false;
            }
        });
        if (!send)
            return false;
        $('.ui.page.dimmer').dimmer('show');
    }

    function alipayShowRequest() {
        var send = true;
        $("#alipay_form").find("input").each(function () {
            if ($.trim($(this).val()) === "") {
                $(this).parent().attr('class', 'field error');
                send = false;
            }
        });
        if (!send)
            return false;
        $('.ui.page.dimmer').dimmer('show');
    }

    function alipayShowResponse(responseText, statusText, xhr) {
        if (responseText.success == 1) {
            $('.ui.page.dimmer').dimmer('hide');
            alert('成功！');
            location.reload();
        } else {
            $('.ui.page.dimmer').dimmer('hide');

            alert("验证未通过，请重新填写。");
        }
    }
});
