function itemMap(series,xAxis,legend_data) {
var chart = echarts.init(document.getElementById('mainly_map'));
//参数设置
option = {
    color: ['#EE0000','#F0F8FF','#525252','#EEEE00','#EE9A00','#C6E2FF','#BCEE68','#F4F4F4','#EE5C42','#BCD2EE','#B7B7B7','#8B7500','#7AC5CD','#36648B','#EED5B7','#A020F0','#0000CD','#FFFF00','#EE00EE'],
    title: {
        text: '购物篮系数分类占比',
        left: 'center', 
           },
    tooltip: {    //提示框组件
        formatter:function(obj){
            var value = obj.value;
            if(value.length  >1){
                return  value[3]+'<br>'+
                        value[1]+'<br>'+
                        value[2]+'<br>';
            }
        },

    },
    legend: {     //图例组件
        data: legend_data,
        'top':'0%',
        'left':'90%',
        'itemWidth':10,
        'itemHeight':6,
        'itemGap':8,
        'orient':'vertical',
        formatter:function(value){
            var out = '';
            var size = 5;
            while(value.length>size)
            {
                out = out+value.slice(0,size)+'\n';
                value = value.slice(size);
            }
            out+=value;
            return out;
        },
    },
    xAxis: xAxis,     //直角坐标系 grid 中的 x 轴
   //     xAxis : {'type':'category','axisLabel':{'interval':0,}},    
    yAxis: {       //直角坐标系 grid 中的 y 轴
        type: 'value',
        "axisLabel":{"formatter":'{value}个'},
        name:'数量',
    },
    series: series,      //系列列表
};

chart.setOption(option);   //参数设置方法
}
