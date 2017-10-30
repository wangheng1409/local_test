$(document).ready(function(){
    // 总页数
    var dataTotal = 0;
    // 当前页数
    var index = 1;
    // 判断商品列表是否加载完
    var loaded = false;
    // 城市列表
    var cityCode = [];
    // 定时器
    var timer = null;
    var productId = [];
    function ajaxRequestFun(url) {
        $.ajax({
            url: url,
            type: 'GET',
            statusCode: {
                500: function() {
                    $('.con-date-choice, .con-class-choice, .list-wrapper').hide();
                    $('.con-product').append('<p class="error">您查找的分类下，没有任何商品哦!<br/>返回<a href="discovery">首页</a></p>');
                },
                200: function(){
                    $('.con-date-choice, .con-class-choice, .list-wrapper').show();
                }
            },
            success:function(data) {
                for (var i = 0; i < data.results.length; i++) {
                    var name = data.results[i].name;
                    var score = data.results[i].score.toFixed(2);
                    var source = data.results[i].source;
                    var skuid = data.results[i].skuid;
                    // 商品id加入列表productId,判断是否被收藏
                    productId.push(skuid);
                    var imageUrl = data.results[i].image_url;
                    var price = data.results[i].price;
                    var area = data.results[i].area;
                    // 排名
                    var ranking = ((index - 1) * 50 + i + 1);
                    // 链接
                    var href = "product-info?area="+ area +"&source="+ source +"&skuid="+ skuid;
                    // 表示排名顺序
                    var orderDiv = $("<div class='order-num'>"+ ranking +"</div>");
                    // 商品图片
                    var img = $("<a href="+ href +"><img alt='图片加载失败' src="+ imageUrl +" title='"+ name +"'></img></a>");
                    // 商品价格
                    var priceItem = $("<p>销售价：<span class='date-price'>¥"+ price +"</span></p>");
                    // 商品名的链接
                    var newName = $("<a href="+ href +" title='"+ name +"' >"+ name +"</a>");
                    // 商品分
                    var newScore = $("<p>商品分：<span class='date-score'>"+ score +"</span></p>");

                    // 表示每一个商品
                    var li = $("<li></li>");
                    // 表示当前商品已收藏
                    var heart = $("<i class='big red icon'></i>").attr('name',skuid);
                    $(li).append(heart).append(orderDiv).append(img).append(newName).append(priceItem).append(newScore);
                    $('#con_list').append(li);
                }
                if (data !== 0) {
                    dataTotal = data.total;
                    loaded = true;
                }
            }
        });
    }

    function citySelectionFun(){
        // 当前城市对应的编码
        var code = 0;
        var cityObj = {
            'HD':['上海','江苏','浙江','安徽','福建','山东'],
            'HN':['广东','广西','海南'],
            'HB':['北京','天津','河北','山西','内蒙古']
        };
        var cityUrl = '/discovery?area=';
        // 循环每个对象 HB
        for (var val in cityObj) {
            // simp:每个对象下的城市
            var simp = cityObj[val];
            for (var i = 0; i < simp.length; i++) {
                var currentCityCode = $('<a class="item" href='+ cityUrl + val +"&code="+ code +'>'+ simp[i] +'</a>');
                $('#city_list').append(currentCityCode);
                cityCode.push(simp[i]);
                code++;
            }
        }
    }

    String.prototype.format = function(args) {
        if (arguments.length > 0) {
            var result = this;
            if (arguments.length == 1 && typeof (args) == "object") {
                for (var key in args) {
                var reg = new RegExp ("({"+key+"})","g");
                result = result.replace(reg, args[key]);
                }
            }
            else {
                for (var i = 0; i < arguments.length; i++) {
                    if(arguments[i]===undefined){
                        return "";
                    }else {
                        var regOther = new RegExp ("({["+i+"]})","g");
                        result = result.replace(regOther, arguments[i]);
                    }
                }
            }
            return result;
        }
        else {
            return this;
        }
    };

    function getParamsFun(){
        var code = $('#city_name').attr('name');
        var area = $('#city_name').attr('area');
        var catType = $('#category').attr('name');
        var order = $('#order').attr('name');
        var source = $('#shop_name').attr('source');
        var page = $('#current_page').html();
        var grand = $('.con-date-list').attr('name');
        var paramList = {code: code,
                         area: area,
                         std_cat: catType,
                         order: order,
                         source: source,
                         page: page,
                         grand: grand
                        };
        return paramList;
    }

    var param = getParamsFun();
    function requestDataFun(){
        var requestUrl = 'area={area}&source={source}&o={o}&page={page}&std_cat={std_cat}&grand={grand}';
        var currentUrl = requestUrl.format({area: param.area,
                                            source: param.source,
                                            o: param.order,
                                            std_cat: param.std_cat,
                                            page: param.page,
                                            grand: param.grand
                                          });
        // 请求数据
        ajaxRequestFun('api/v1/online-item?'+currentUrl);
    }

    function reloadPageFun(elem,val){
        var requestUrl = 'area={area}&source={source}&o={o}&page={page}&std_cat={std_cat}&grand={grand}';

        if (elem == 'source') {
            param.source = val;
            param.page = 1;
        }else if (elem == 'order') {
            param.order = val;
        }else if (elem == 'std_cat') {
            param.std_cat = val;
        }else if (elem == 'pagi') {
            param.page = val;
        }else if (elem == 'pre-page') {
            param.page --;
            if (param.page <= 0) {
                param.page = 1;
            }
        }else if (elem == 'next-page') {
            param.page ++;
            if (param.page >= dataTotal) {
                param.page = dataTotal;
            }
        }else if (elem == 'grand') {
            param.grand = val;
        }

        if (elem != 'pagi' && elem != 'pre-page' && elem != 'next-page') {
            param.page = 1;
        }

        var currentUrl = requestUrl.format({area: param.area,
                                            source: param.source,
                                            o: param.order,
                                            std_cat: param.std_cat,
                                            code: param.code,
                                            page: param.page,
                                            grand: param.grand
                                          });
        // 重载页面
        window.location.href = 'discovery?'+currentUrl;
    }

    function changeStatusFun() {
        // 每一页
        $('.pagi').click(function() {
            var sign = $(this).attr('sign');
            var name = $(this).html();
            reloadPageFun(sign,name);
        });

        // 左右翻页
        $('.next-page,.pre-page').click(function(){
            var sign = $(this).attr('sign');
            var name = $('#current_page').html();
            reloadPageFun(sign,name);
        });

        // 商城、排序、商品分类、时间范围
        $('.mall, .sort, #category .item, .date, .date').click(function(){
            var sign = $(this).attr('sign');
            var name = $(this).attr('name');
            reloadPageFun(sign,name);
            return false;
        });

        // 商品分类
        $('.con-cat-list').hover(function(){
            $('#category').show();
        },function(){
            $('#category').hide();
        });

        $('#category>div').hover(function(){
            $(this).children('.sec_wrapper').removeClass('popup');
        },function(){
            $(this).children('.sec_wrapper').addClass('popup');
        });

        $('.ui.dropdown').dropdown({
            on: 'hover'
        });
    }

    function currentStatusFun(){
        // 日期
        $('.date').each(function() {
            if ($(this).attr('name') == param.granularity) {
                $(this).addClass('current-date');
            }
        });

        // 分页
        for (var i = 1; i <= dataTotal; i++) {
            if (i <= 6) {
                var single = $('<a href="javascript:" class="item pagi" sign="pagi">'+ i +'</a>');
                $("#next_page").before(single);
            }
        }
        $('.pagi').each(function(){
            if ($(this).html() == param.page) {
                $(this).addClass('active');
            }
            if (param.page >= 4 && dataTotal > 6) {
                if (param.page >= dataTotal - 2) {
                    for (var i = 0; i < $('.pagi').length; i++) {
                        var nowPage = dataTotal - 5 + i;
                        $('.pagi')[i].innerHTML = nowPage;
                    }
                }else{
                    for (var j = 0; j < $('.pagi').length; j++) {
                        var nowPageOther = param.page - 3 + j;
                        $('.pagi')[j].innerHTML = nowPageOther;
                    }
                }

            }
        });

        // 排序方式
        $('.sort').each(function(){
            if ($(this).attr('name') == param.order) {
                $(this).addClass('red');
            }
        });

        // 商城
        $('.mall').each(function(){
            if ($(this).attr('name') == param.source) {
                $(this).addClass('current-date');
            }
        });

        // 城市
        var codeNum = $('#city_name').attr('name');
        $('#city_name').html(cityCode[codeNum]);

        // 商品分类
        var  productCat = $('#category').attr('name');
        var leg = $('#category a.item');
        var rightIcon = '<i class="right chevron icon divider"></i>';
        for (var k = 0; k < leg.length; k++) {
            if (leg[k].name == productCat){
                var inner = leg[k].innerHTML;
                $('.yellow.ui.button').html(inner);
                var firLevel = '<a href="javascript:" class="section">'+ inner +'</a>';
                for (var j = 0; j < leg.length; j++) {
                    if ($(leg[k]).attr('p_id') == leg[j].name) {
                        var productInner = $(leg[name=j]).html();
                        var secLevel = '<a href="javascript:" class="section">'+ productInner +'</a>';
                        if (leg[j].name != 1) {
                            for (var l = 0; l < leg.length; l++) {
                                if ($(leg[j]).attr('p_id') == leg[l].name) {
                                    var grandProductInner = $(leg[name=l]).html();
                                    var thiLevel = '<a href="javascript:" class="section">'+ grandProductInner +'</a>';
                                    $('#breadcrumb').append(thiLevel).append(rightIcon).append(secLevel).append(rightIcon).append(firLevel);
                                }
                            }
                        }else{
                            $('#breadcrumb').append(secLevel).append(rightIcon).append(firLevel);
                        }
                    }
                }
            }
        }

        // 日期
        $('.date').each(function(){
            if ($(this).attr('name') == param.grand) {
                $(this).addClass('current-date');
            }
        });
    }

    function getProductId(arr){
        $.ajax({
            url: 'api/v1/products-list-collected',
            type: 'POST',
            data: {
                'skuids': Array(arr),
                'source':param.source
            },
            header: {
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            dataType: 'json',
            success: function(collect){
                var resultRrray = [];
                for (var i = 0; i < collect.result.length; i++) {
                    var resultId = collect.result[i].product_id;
                    resultRrray.push(resultId);
                }
                $('#con_list i.icon').each(function(){
                    var listId = Number($(this).attr('name'));
                    if (resultRrray.indexOf(listId) != -1) {
                        $(this).addClass('heart');
                        $(this).parent().css('border', '1px solid red');
                    }
                });
            }
        });
    }

    var str = window.location.href;
        str = str.substring(str.lastIndexOf("/") + 1);
        if ($.cookie(str)) {
            $("html,body").animate({ scrollTop: $.cookie(str) }, 500);
        }

    $(window).scroll(function () {
        var str = window.location.href;
        str = str.substring(str.lastIndexOf("/") + 1);
        var top = $(document).scrollTop();
        $.cookie(str, top, { path: '/' });
        return $.cookie(str);
    });

    requestDataFun();
    citySelectionFun();
    index = param.page;
    timer = setInterval(function(){
        if (loaded === true){
            $('#total_page').html(dataTotal);
            currentStatusFun();
            changeStatusFun();
            loaded = false;
            clearInterval(timer);
            // 商品列表加载完，获取当前页面所有商品的id
            getProductId(productId);
        }
    },20);
});