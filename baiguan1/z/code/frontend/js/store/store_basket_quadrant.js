function itemMap(series) {
var chart = echarts.init(document.getElementById('mainly_map'));
//参数设置
schema = [
         {'name':'basket','index':0,'text':'购物篮系数'}, 
         {'name':'count','index':1,'text':'购物篮数量'}, 
         {'name':'name','index':2,'text':'商品名称'}, 
         {'name':'sum_sales','index':3,'text':'销售量','unit':'个'}, 
         {'name':'price_avg','index':4,'text':'价格','unit':'元'}, 
         {'name':'sum_num','index':5,'text':'销售额','unit':'元'}, 
];
option = {
        title: {
               text: '购物篮系数－四象限图',
               left: 'center', 
               },
        color: ['#3398DB'],
        tooltip: {    //提示框组件
            formatter:function(obj){
                var value = obj.value;
                if(value.length  >1){
                    return schema[2].text + ':' + value[2]+'<br>'+
                        schema[3].text+':'+value[3]+schema[3].unit+'<br>' +
                        schema[4].text + ':' + value[4]+schema[4].unit+'<br>' +
                        schema[5].text+':'+value[5]+schema[5].unit+'<br>';
                }
            }
        },
        xAxis: {type:'value','splitLine':{'show':false},name:'购物篮系数'},     //直角坐标系 grid 中的 x 轴
        yAxis: {       //直角坐标系 grid 中的 y 轴
            type: 'value',
            'splitLine':{'show':false},
            "axisLabel":{"formatter":'{value}个'},
            name:'购物篮数量',
        },
        series: series,      //系列列表
};

chart.setOption(option);   //参数设置方法
}
