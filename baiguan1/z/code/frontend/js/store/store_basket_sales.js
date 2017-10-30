function itemMap(series,xAxis) {
var chart = echarts.init(document.getElementById('mainly_map'));
//参数设置
option = {
        color: ['#3398DB'],
        legend: {     //图例组件
            data: ['销售占比','购物篮系数'],
            right:'20%',
        },
        tooltip: {    //提示框组件
            trigger: 'axis',
            formatter: function(obj){
                       out = '日期:'+obj[0].name+'<br>'+
                             '销售占比:'+obj[0].value+'%<br>'+
                             '购物篮系数:'+obj[1].value;
                       return out;
            },
        },
        xAxis: xAxis,     //直角坐标系 grid 中的 x 轴
        yAxis: [       //直角坐标系 grid 中的 y 轴
            {
              name:'销售占比',
              type: 'value',
              axisLabel:{formatter:'{value}%'},
            },
            {
              name:'购物篮系数',
              type: 'value',
            },
        ],
        series: series,      //系列列表
};

chart.setOption(option);   //参数设置方法
}
