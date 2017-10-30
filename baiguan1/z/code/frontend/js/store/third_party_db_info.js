(function(cmApp) {
    "use strict";

    cmApp.toast = new Vue({
        el: '#error',
        data: {
            isHidden: true,
            isError: true,
            message: ''
        },
        computed: {
            isSuccess: function() {
                return !this.isError;
            }
        },
        methods: {
            dismiss: function() {
                this.isHidden = true;
            },
            show: function() {
                this.isError = false;
                this.isHidden = false;
            },
            showError: function() {
                this.isError = true;
                this.isHidden = false;
            }
        }
    });

    cmApp.dbInfo = new Vue({
        el: '#dbinfo',
        data: {
            dbinfo: null,
            tableNames: [],
            permission_code: '',
            statusCode: 0,
            posted: false
        },
        computed: {
            tableNum: function() {
                return this.tableNames.length;
            },
            hasPermission: function() {
                var hasPermission = true;
                for (var i=0; i < this.permission_code.length; i++) {
                    if (this.permission_code[i] !== '0') {
                        hasPermission = false;
                        break;
                    }
                }
                return hasPermission;
            }
        }
    });

    $(document).ready(function() {
        $('.ui.dropdown').dropdown();

        $('#db_info').submit(function() {
            console.log("Submitting db info form");
            var options = {
                url: '/api/v1/thirdpartydb',
                type: 'post',
                dataType: 'json',
                beforeSumit: function() {
                    $($('#db_info .submit')[0]).addClass('loading');
                },
                success: function(e) {
                    cmApp.dbInfo.posted = true;
                    console.log(e);
                    $($('#db_info .submit')[0]).removeClass('loading');
                    cmApp.dbInfo.statusCode = e.code;
                    if (e.code === 0) {
                        console.log("success");
                        cmApp.dbInfo.dbinfo = e.data.dbinfo;
                        cmApp.dbInfo.tableNames= e.data.table_names;
                        cmApp.dbInfo.permission_code = e.data.permission_code;
                        if (cmApp.dbInfo.hasPermission) {
                            cmApp.toast.message = '连接数据库成功';
                            cmApp.toast.show();
                            $('#nav-btn').removeClass('disabled');
                        } else {
                            cmApp.toast.message = '权限不全 Err(' + cmApp.dbInfo.permission_code + ')';
                            cmApp.toast.showError();
                        }
                    } else {
                        cmApp.dbInfo.dbinfo = null;
                        cmApp.dbInfo.tableNames = [];
                        cmApp.dbInfo.permission_code = '22222';
                        cmApp.toast.message = e.message + ':' + e.errors;
                        cmApp.toast.showError();
                    }
                }
            };
            $(this).ajaxSubmit(options);
            return false;
        });
    });
})(window.cmApp = window.cmApp || {});
