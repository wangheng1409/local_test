function itemMap(series,xAxis) {
var chart = echarts.init(document.getElementById('mainly_map'));
//参数设置
option = {
        title: {
               text: '一周购物篮系数变化',
               },
        color: ['#3398DB'],
        legend: {     //图例组件
            data: ['购物篮系数','周边购物篮系数'],
            right:'20%',
        },
        tooltip: {    //提示框组件
            trigger: 'axis'
        },
        xAxis: xAxis,     //直角坐标系 grid 中的 x 轴
        yAxis: {       //直角坐标系 grid 中的 y 轴
            type: 'value'
        },
        series: series,      //系列列表
};

chart.setOption(option);   //参数设置方法
}
