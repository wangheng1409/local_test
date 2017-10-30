$(function () {
    var browser_height = window.innerHeight;
    $('#sidebar').css('height', browser_height);
    init_char_data1('sales','2');
    init_store_data(1,2);
    init_circle_graph_data('sales','2');

    $('#day1').children().click(function(){
        day=$(this).attr("day");
        $(this).addClass("date-choiced").siblings().removeClass("date-choiced");
        rule=$('#total_data').children('[class="graph-color"]').attr("rule");
        init_char_data1(rule,day);
    });

    $('#total_data').children().click(function(){
        rule=$(this).attr("rule");
        $(this).addClass("graph-color").siblings().removeClass("graph-color");
        day=$('#day1').children('[class="date-choiced"]').attr("day");
        init_char_data1(rule,day);
    });

    $('#day2').children().click(function(){
        day=$(this).attr("day");
        $(this).addClass("date-choiced").siblings().removeClass("date-choiced");
        rule=$('#total_data').children('[class="graph-color"]').attr("rule");
        init_circle_graph_data(rule,day);
        
    });

    $('#y2').children().click(function(){
        rule=$(this).attr("rule");
        $(this).addClass("graph-color").siblings().removeClass("graph-color");
        day=$('#day2').children('[class="date-choiced"]').attr("day");
        init_circle_graph_data(rule,day);
    });

    $('#day3').children().click(function(){
        day=$(this).attr("day");
        $(this).addClass("date-choiced").siblings().removeClass("date-choiced");
        rule=$('#total_data').children('[class="graph-color"]').attr("rule");
        init_char_data3(rule,day);
        
    });

    $('#y3').children().click(function(){
        rule=$(this).attr("rule");
        $(this).addClass("graph-color").siblings().removeClass("graph-color");
        day=$('#day3').children('[class="date-choiced"]').attr("day");
        init_char_data3(rule,day);
    });

    $('#day4').children().click(function(){
        day=$(this).attr("day");
        $(this).addClass("date-choiced").siblings().removeClass("date-choiced");
        rule=$('#rule').children().attr("sort_rule");
         console.log(rule,777);
        var add_row_list=[];
            var a=$('#add_row').find("input:checked");
            console.log(a);
            for(var i=0;i< a.length;i++){
                var inp=a[i];
                add_row_list.push($(inp).attr('tag'));
            }
        get_store_data(rule,day,add_row_list);    
    });

    $('#rule').children().click(function(){
        rule=$(this).attr("sort_rule");
        $(this).addClass("graph-color").siblings().removeClass("graph-color");
        day=$('#day4').children('[class="date-choiced"]').attr("day");
        var add_row_list=[];
            var a=$('#add_row').find("input:checked");
            console.log(a);
            for(var i=0;i< a.length;i++){
                var inp=a[i];
                add_row_list.push($(inp).attr('tag'));
            }
        get_store_data(rule,day,add_row_list);
            
        });

    $('#open_add_items').click(function(){
        $('#add-items').removeClass("hide");
        
    });

    $('#close_add_items').click(function(){
         $('#add-items').addClass("hide");
        
    });

    $('#cancel').click(function(){
         $('#add-items').addClass("hide");
        
    });

    $('#add_row1').click(function(){
        $('#new_row').children(':lt('+$('#new_row:last').children().last().index(this)+'):gt(1)').remove();
        var add_row_list=[];
        var a=$('#add_row').find("input:checked");
        console.log(a);
        for(var i=0;i< a.length;i++){
            var inp=a[i];
            add_row_list.push($(inp).attr('tag'));
            $('#new_row:last').children().last().prev().after('<th>'+$(inp).parent().text()+'</th>');
        }
        rule=$('#rule').children().attr("sort_rule");
        day=$('#day4').children('[class="date-choiced"]').attr("day");
        get_store_data(rule,day,add_row_list);
        $('#add-items').addClass("hide");
        
    });


});

function graph(data,rule){
        //数据初始化
        var X_axis=data.X_axis;
        var Y=data.Y_axis;
        var Y_axis=Y['sales'];
        if(rule=='sales'){
           var Y_axis=Y['sales'];
        }else if(rule=='gross_profit'){
            var Y_axis=Y['gross_profit'];
        }else if(rule=='each_num_trades_sales'){
            var Y_axis=Y['num_trades'];
        }else if(rule=='num_trades'){
            var Y_axis=Y['num'];
        }

        Y_axis_list=[];
         $.each(Y_axis, function(k,v){
                    Y_axis_list.push(v[rule]);      
                        });




        //初始化
        var myChart = echarts.init(document.getElementById('main'));
        //参数设置
        option = {
            tooltip: {    //提示框组件
                trigger: 'axis'
            },
            legend: {     //图例组件
                data: [rule]
            },
            grid: {       //直角坐标系内绘图网格
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {       //直角坐标系 grid 中的 x 轴
                type: 'category',
                boundaryGap: false,
                data:X_axis
            },
            yAxis: {       //直角坐标系 grid 中的 y 轴
                type: 'value'
            },
            series: [      //系列列表
                {
                    name: rule,
                    type: 'line',
                    stack: '总量',
                    data: Y_axis_list
                }
            ]
        };
        myChart.setOption(option);   //参数设置方法
    }

function init_char_data1(rule,day){
    store_id=location.href.split("=")[1].split("%")[0];
    $.ajax({
        url: '/analytics/chain-stores/stores/'+store_id+'/overall'+'?date_rule1='+day, 
        type: 'GET',　　
        dataType: 'json',
        success: function(data){ 
            overall_data=data.overall_data;
            $('#total_target').text(overall_data.tsales);
            $('#total_finish_rate').text(overall_data.sales/overall_data.tsales);
            $('#total_balance').text(overall_data.sales-overall_data.tsales);
            $('#total_turnover').text(overall_data.total_turnover);

            $('#total_data li:eq(0) span:eq(1)').text(overall_data.sales);
            $('#total_data li:eq(1) span:eq(1)').text(overall_data.gross_profit);
            $('#total_data li:eq(2) span:eq(1)').text(overall_data.num_trades);
            $('#total_data li:eq(3) span:eq(1)').text(overall_data.each_num_trades_sales);
            graph(data,rule);
        }
    });
}

function init_char_data3(rule,day){
    $.ajax({
        url: '/analytics/get-overall-data?date_rule='+day, 
        type: 'GET',　　
        dataType: 'json',
        success: function(data){ 
            Overall_data=data.Overall_data[0];
            $('#total_data li:eq(0) span:eq(1)').text(Overall_data.sales);
            $('#total_data li:eq(2) span:eq(1)').text(Overall_data.num_trades);
            $('#total_data li:eq(3) span:eq(1)').text(Overall_data.each_num_trades_sales);
            graph(data,rule);
        }
    });
}


function init_store_data(rule,day){
    var store_id=location.href.split("=")[1].split("%")[0];
    $.ajax({
        url: '/analytics/chain-stores/stores/store-detailed-info/special-items/'+store_id+'?sort_rule='+rule+','+day,
        type: 'GET',　　
        dataType: 'json',
        success: function(data){ 
            init_table_data(data,[]);
        }
    });
}

function init_table_data(current_store_list,add_row_list){
    $('#store_list').empty();
     for(var i=0;i< current_store_list.length;i++){
        var n=i+1;
        var inp=current_store_list[i];
        var num=inp.num;
        var status=inp.status;
        var each_sales=inp.each_sales;
        var barcode=inp.barcode;
        var sales=inp.sales;
        var sales_growth=inp.sales_growth;
        var num_growth=inp.num_growth;
        var name=inp.name;
        var item_id=inp.item_id;
        var eachday_num=inp.eachday_num;
        var obj = {};

        // console.log(typeof add_row_list[0]);
        obj['item_id'] = item_id;
        obj['sales'] = sales;
        obj['num'] = num;
        obj['status'] = status;
        obj['barcode'] = barcode;
        obj['each_sales'] = each_sales;
        obj['eachday_num'] = eachday_num;
        obj['sales_growth'] = sales_growth;
        obj['num_growth'] = num_growth;


        
        // var picture={% static 'images/up.png' %};
        var store_item_box = [];
                
                store_item_box.push('<tr>'+
                                '<td>'+n+'</td>'+
                                '<td>'+name+'</td>'
                                );
                for (var j=0;j< add_row_list.length;j++){
                        store_item_box.push('<td>'+obj[add_row_list[j]]+'</td>');
                    }

                store_item_box.push(
                            '</tr>');
            
                var store_item = store_item_box.join(' ');
                // console.log(store_item,666);
                $('#store_list').append(store_item);
    }

}

function get_store_data(rule,day,add_row_list){
    var store_id=location.href.split("=")[1].split("%")[0];
    $.ajax({
        url: '/analytics/chain-stores/stores/store-detailed-info/special-items/'+store_id+'?sort_rule='+rule+','+day,
        type: 'GET',　　
        dataType: 'json',
        success: function(data){ 
            init_table_data(data,add_row_list);
        }
    });
}

function circle_graph(data,rule){
    var circle = document.getElementById("circle_chart");
    var myChart = echarts.init(circle);
    var num=data.num;
    var sales=data.sales;
    var level0_name=data.level0_name;
    var obj = {};
    var d=[];
    obj['num'] = num;
    obj['sales'] = sales;
    obj['level0_name'] = level0_name;
    for (var j=0;j< level0_name.length;j++){
                        d.push({value:obj[rule][j], name:level0_name[j]});
                    }
    var app = {};
    option = null;
    app.title = '环形图';

    option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data:level0_name
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                saveAsImage : {show: true}
            }
        },
        series: [
            {
                name:'',
                type:'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '20',
                            fontWeight: 'bold'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data:d
            }
        ]
    };
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }

}

function init_circle_graph_data(rule,day){
    var  store_id=location.href.split("=")[1].split("%")[0];
    $.ajax({
        url: '/analytics/chain-stores/top-items/'+store_id+'?'+'days='+day,
        type: 'GET',　　
        dataType: 'json',
        success: function(data){ 
            circle_graph(data,rule);
        }
    });


    }