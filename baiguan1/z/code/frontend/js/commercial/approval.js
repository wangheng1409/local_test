$(document).ready(function () {
    $("input[class='approve']").click(function () {
              var index = layer.open({
              type: 2,
              title: "广告审核",
              skin: 'layui-layer-lan', //加上边框
              area: ['80%', '80%'], //宽高
              scrollbar: false,
              content: '/approve_ad?item='+$(this).attr("id"),
              end:function(){
                window.location.reload();
              }

            });
    });
});
