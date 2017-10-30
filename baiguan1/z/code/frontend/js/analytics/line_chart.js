$(function () {
    var browser_height = window.innerHeight;
    $('#sidebar').css('height', browser_height);
    init_char_data('sales','2');

    $('#day').children().click(function(){
        day=$(this).attr("day");
        $(this).addClass("date-choiced").siblings().removeClass("date-choiced");
        rule=$('#total_data').children('[class="graph-color"]').attr("rule");
        init_char_data(rule,day); 
    });

    $('#total_data').children().click(function(){
        rule=$(this).attr("rule");
        $(this).addClass("graph-color").siblings().removeClass("graph-color");
        day=$('#day').children('[class="date-choiced"]').attr("day");
        init_char_data(rule,day);
        
    });

    $('#store_property').children().click(function (){
        store_property=$(this).attr("tag");
        $(this).addClass("store-color").siblings().removeClass("store-color");
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
                    Y_axis_list.push(v);      
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

function init_char_data(rule,day){
    $.ajax({
        url: '/analytics/chain-stores/store-overview/overall', 
        type: 'GET',　　
        dataType: 'json',
        success: function(data){ 
            console.log(data);
            var overall_data=data.overall_data;
            $('#tsales').text(overall_data.tsales<10000?overall_data.tsales:parseFloat((overall_data.tsales/10000).toFixed(2)).toString()+'万');
            $('#total_finish_rate').text(parseInt(overall_data.finsh_rate*100).toFixed(2).toString()+'%');
            $('#balance').text(overall_data.balance>-10000?overall_data.balance:parseFloat((overall_data.balance/10000).toFixed(2)).toString()+'万');
            $('#total_turnover').text(overall_data.total_turnover.toFixed(2));

            $('#total_data li:eq(0) span:eq(1)').text(overall_data.sales<10000?overall_data.sales:parseFloat((overall_data.sales/10000).toFixed(2)).toString()+'万');
            $('#total_data li:eq(1) span:eq(1)').text(overall_data.gross_profit<10000?overall_data.gross_profit:parseFloat((overall_data.gross_profit/10000).toFixed(2)).toString()+'万');
            $('#total_data li:eq(2) span:eq(1)').text(overall_data.num_trades<10000?overall_data.num_trades:parseFloat((overall_data.num_trades/10000).toFixed(2)).toString()+'万');
            $('#total_data li:eq(3) span:eq(1)').text(overall_data.each_num_trades_sales<10000?overall_data.each_num_trades_sales.toFixed(2):parseFloat((overall_data.each_num_trades_sales/10000).toFixed(2)).toString()+'万');
            graph(data,rule);
            var area_list=data.area_list;
            init_area_data(area_list);
        }
    });
}


function init_area_data(area_list){
    console.log(area_list,123)
    $('#area_list').empty();
     for(var i=0;i< area_list.length;i++){
        var n=i+1;
        var inp=area_list[i];
        var name=inp.name;
        var tsales=inp.sales_target;
        var sales=inp.sales;
        var finish_rate=sales/tsales;
        var balance=sales-tsales;
        var gross_profit=inp.gross_profit;
        var store_item_box = [];
        // console.log(typeof inp['tsales'])
                
        store_item_box.push('<tr>'+
                    '<td>'+name+'</td>'+
                    '<td>'+tsales+'</td>'+
                    '<td>'+sales+'</td>'+
                    '<td>'+finish_rate+'</td>'+
                    '<td>'+balance+'</td>'+
                    '<td>'+gross_profit+'</td>'+
                    '<td>'+16.8+'</td>'+
                '</tr>');
    
        var store_item = store_item_box.join(' ');
        $('#area_list').append(store_item);
    }

}