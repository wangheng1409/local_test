var bar_chart = document.getElementById('bar_chart');
var myChart = echarts.init(bar_chart);
option = {
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        data : ['销售额']
    },
    grid: {
        show : true,
        left : 70
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value'
        }
    ],
    yAxis : [
        {
            type : 'category',
            axisTick : {show: false},
            data:['烟','酒','饮料','休闲食品','粮油冲调','用品','冷冻冷藏','鲜食','进口','电商商品','特许自采']
        }
    ],
    series : [
        {
            name:'销售额',
            type:'bar',
            itemStyle : {
                normal: {
                    label : {
                        show: true,
                        position: 'inside'
                    },
                    color : '#FF491F'
                }
            },
            data:[200, 170, 240, 244, 200, 220, -21, -32, -234]
        }
    ]
};
myChart.setOption(option);