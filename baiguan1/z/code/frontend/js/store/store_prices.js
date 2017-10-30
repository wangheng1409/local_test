function itemMap(series,xAxis,markPoint) {
var chart = echarts.init(document.getElementById('mainly_map'));
//参数设置
option = {
        title: {
               text: '价格带（有过销售）',
               left: 'center', 
               },
        color: ['#3398DB'],
        legend: {     //图例组件
            data: ['数量'],
            right:'10%',
        },
        tooltip: {    //提示框组件
            trigger: 'axis'
        },
        xAxis: xAxis,     //直角坐标系 grid 中的 x 轴
        yAxis: {       //直角坐标系 grid 中的 y 轴
            type: 'value',
            "axisLabel":{"formatter":'{value}个'},
            name:'数量',
        },
        series: series,      //系列列表
};

chart.setOption(option);   //参数设置方法
}
