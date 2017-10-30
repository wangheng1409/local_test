$(document)
    .ready(function () {
        // fix main menu to page on passing
        $('.main.menu').visibility({
            type: 'fixed'
        });
        $('.overlay').visibility({
            type: 'fixed',
            offset: 80
        });
        $('.ui.sidebar')
            .sidebar('attach events', '.toc.item')
        ;
        // lazy load images
        $('.image').visibility({
            type: 'image',
            transition: 'vertical flip in',
            duration: 500
        });

        // show dropdown on hover
        $('.main.menu.ui.dropdown').dropdown({
            on: 'hover'
        });

        $('#disclaimer').click(function () {
            $('.long.modal').modal('show');
        });

        $('.ui.primary.approve.button').click(function () {
            $('#terms').attr('checked', 'checked');
        });

        $('#sql').click(function () {
            if ($(this).find('.checkmark').length == 1)
                return false;
            location.href = '/integration/add-db';
        });
        $('#wechat').click(function () {
            if ($(this).find('.checkmark').length == 1)
                return false;
            location.href = '/integration/add-transaction-accounts';
        });
        $('#alipay').click(function () {
            if ($(this).find('.checkmark').length == 1)
                return false;
            location.href = '/integration/add-transaction-accounts';
        });
    });
