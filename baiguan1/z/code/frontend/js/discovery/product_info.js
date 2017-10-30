$(document).ready(function() {
    var source = null;
    var area = null;
    var grand = $('#product_grand').attr('name');

    function getProductsInfo(url) {
        $.ajax({
            url: url,
            type: 'GET',
            // data: {'grand':grand},
            success:function(data){
                $('#product_name').html(data.results[0].name);
                $('#product_price').html('¥' + data.results[0].price);
                $('#image_url').attr('src',data.results[0].image_url);
                // 商品分
                var good_score = data.results[0].score;
                var score = good_score.toFixed(2);
                $('#product_score').html(score);

                var rankNum = data.results[0].date_rank.split(',').length;
                var getRank = [];
                for (var i = 0; i < rankNum; i++) {
                    var everyRank = (data.results[0].date_rank).split(',')[i].split(':')[1];
                    getRank.push(everyRank);
                }

                var getRankDate = [];
                for (var j = 0; j < rankNum; j++) {
                    var everyRankDate = (data.results[0].date_rank).split(',')[j].split(':')[0];
                    getRankDate.push(everyRankDate);
                }
                graph(getRankDate,getRank);
            }
        });
    }

    // 折线图
    function graph(rankDate,rank){
        //初始化
        var myChart = echarts.init(document.getElementById('main'));
        //参数设置
        option = {
                //标题组件
                title: {
                    text: '增长曲线'
                },
                //提示框组件：坐标轴触发
                tooltip: {
                    trigger: 'axis'
                },
                //图例组件
                legend: {
                    data: ['商品销量排名']
                },
                //直角坐标系内绘图网格
                grid: {
                    // 距离左侧容器的距离
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                //工具栏
                toolbox: {
                    feature: {
                        // 保存图片
                        saveAsImage: {}
                    }
                },
                //直角坐标系 grid 中的 x 轴
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: rankDate
                },
                //直角坐标系 grid 中的 y 轴
                yAxis: {
                    type: 'value'
                },
                //系列列表
                series: [
                    {
                        name: '商品销量排名',
                        type: 'line',
                        stack: '总量',
                        data: rank
                    }
                ]

            };
        //参数设置方法
        myChart.setOption(option);
    }

    function judgeSourchFun(mall){
        var re = /source=[a-z]+/;
        var reArea = /area=[A-Z]{2}/;
        var mallName = mall.match(re)[0].split('=')[1];
        var mallArea = mall.match(reArea)[0].split('=')[1];
        source = mallName;
        area = mallArea;
        var mallArray = ['tmall','yhd','feiniu'];
        for (var i = 0; i < mallArray.length; i++) {
            if ($('#store-list>li').attr('name') == mallArray[i]) {
                var currentMall = $('#store-list>li[name='+ mallArray[i] +']');
                $(currentMall).children().attr('target','_Blank');
                $(currentMall).show().siblings().hide();
            }
        }

        // 判断当前日期段
        $('.ui.right.floated.button').each(function() {
            if ($(this).attr('name') == grand) {
                $(this).addClass('red');
            }
        });
    }

    function collectProductsFun(requestParam){
        $('#collect_btn').click(function(){
            var skuid = $(this).attr('name');
            var product_name = $('h3').html();
            var product_image = $('img').attr('src');
            var product_source = source;
            var product_area = area;
            $.ajax({
                url: 'product-collect?skuid='+ skuid +'&name='+ product_name +'&image='+ product_image +'&source='+ product_source +'&area='+ product_area,
                type: 'GET',
                data: {exist: 1},
                success: function(obj){
                    if (obj.success == 1) {
                        // 添加成功
                        $('#collect_btn').children().removeClass('empty');
                        $('#collect_btn').children('span').html('已收藏');
                    }else {
                        // 删除成功
                        $('#collect_btn').children().addClass('empty');
                        $('#collect_btn').children('span').html('加入收藏');
                    }
                }
            });
        });


        // 日期
        $('.ui.right.floated.button').click(function(){
            grand = $(this).attr('name');
            window.location.href = 'product-info'+requestParam+'&grand='+grand;
        });
    }

    function requestDataFun(url){
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function(argument){
                if (argument.results === undefined) {
                    judgeProductCollected(argument);
                }else{
                    dateChoiceFun(argument);
                }
            }
        });
    }

    // 判断当前商品是否收藏
    function judgeProductCollected(coll){
        // coll＝0：存在
        if (coll.success === 0) {
            $('#collect_btn').children().removeClass('empty');
            $('#collect_btn').children('span').html('已收藏');
        }else {
            $('#collect_btn').children().addClass('empty');
            $('#collect_btn').children('span').html('加入收藏');
        }
    }

    //选择日期
    function dateChoiceFun(arg){
        var getRankDate = [];
        for (var j = 0; j < rankNum; j++) {
            var everyRankDate = (data.results[0].date_rank).split(',')[j].split(':')[0];
            getRankDate.push(everyRankDate);
        }
        graph(getRankDate,getRank);
    }

    function init(){
        var linkParam = window.location.search;
        getProductsInfo('/api/v1/online-item'+linkParam);//展示商品
        judgeSourchFun(linkParam);//判断当前商城
        collectProductsFun(linkParam);//点击收藏
        requestDataFun('product-collect'+linkParam);
    }
    init();
});
