function itemMap(series,xAxis,lose_days,lose_dates,lose_count,item_name) {
var chart = echarts.init(document.getElementById('container'));
days = xAxis['data'].length
//参数设置
option = {
        title: {      //标题组件
            text: item_name,
            subtext: '缺货'+ lose_days + '天 损失'+lose_count+'元',
            x:'center'
        },
        legend: {     //图例组件
            data: ['本店销量', '历史销量'],
            right:'20%'
        },
        tooltip: {    //提示框组件
            trigger: 'axis'
        },
        toolbox: {     //工具栏
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: xAxis,     //直角坐标系 grid 中的 x 轴
        yAxis: {       //直角坐标系 grid 中的 y 轴
            type: 'value'
        },
        series: series,      //系列列表
};

chart.setOption(option);   //参数设置方法
}
