function graph(a, t) {
	var e = a.X_axis,
		i = a.Y_axis;
	Y_axis_list = [], $.each(i, function(a, e) {
		Y_axis_list.push(e[t])
	});
	var l = echarts.init(document.getElementById("main"));
	option = {
		tooltip: {
			trigger: "axis"
		},
		legend: {
			data: [t]
		},
		grid: {
			left: "3%",
			right: "4%",
			bottom: "3%",
			containLabel: !0
		},
		xAxis: {
		    type: "category",
			boundaryGap: !1,
			data: e
		},
		yAxis: {
			type: "value"
		},
		series: [{
			name: t,
			type: "line",
			stack: "店铺数量",
			data: i
		}]
	},
	l.setOption(option)
}
function init_char_data(source, city,start_day) {


	$.ajax({
		url: "/search?source=" + source+'&city='+city+'&start_day='+start_day,
		type: "GET",
		dataType: "json",
		success: function(data) {
		    console.log(data,'123');
//			Overall_data = a.Overall_data[0],
//			$("#total_data li:eq(0) span:eq(1)").text(Overall_data.sales),
//			$("#total_data li:eq(2) span:eq(1)").text(Overall_data.num_trades),
//			$("#total_data li:eq(3) span:eq(1)").text(Overall_data.each_num_trades_sales),
			graph(data, source);
		},
		error: function (jqXHR, textStatus, errorThrown) {
            /*弹出jqXHR对象的信息*/
            alert(jqXHR.responseText);
            alert(jqXHR.status);
            alert(jqXHR.readyState);
            alert(jqXHR.statusText);
            /*弹出其他两个参数的信息*/
            alert(textStatus);
            alert(errorThrown);
        }
	})
}

$("#source").change( function() {
  // 这里可以写些验证代码
     day = '2017,01,01',
	 city = '全部',
	 source=$("#source option:selected").val(),
	 $.ajax({
		url: "/city?source=" + source,
		type: "GET",
		dataType: "json",
		success: function(data) {
		    console.log(data,'456');
            $("#city").empty();
            for (var a = 0; a < data.length; a++) {
                var r = data[a];
                $("#city").append('<option>' + r + "</option>")
            }
            $("#city").first().attr("selected", "selected")
		},
		error: function (jqXHR, textStatus, errorThrown) {
            /*弹出jqXHR对象的信息*/
            alert(jqXHR.responseText);
            alert(jqXHR.status);
            alert(jqXHR.readyState);
            alert(jqXHR.statusText);
            /*弹出其他两个参数的信息*/
            alert(textStatus);
            alert(errorThrown);
        }
	})
	$('#cc .calendar-selected').removeClass("calendar-selected");
    var d=new Date();
    d.setDate(d.getDate()-7);
    year=d.getFullYear().toString();
    month=(d.getMonth()+1).toString();
    day=d.getDate().toString();
    start_day=year+','+month+','+day
    $('#cc td[abbr="'+start_day+'"]').addClass("calendar-selected");
    ((d.getMonth()+1).toString().length==2)?month=(d.getMonth()+1).toString():month='0'+(d.getMonth()+1).toString();
    (d.getDate().toString().length==2)?day=d.getDate().toString():day='0'+d.getDate().toString();
    new_start_day=year+','+month+','+day
	 init_char_data(source, city,new_start_day)
});

$("#search").click( function () {
    day = $('#cc .calendar-selected').attr('abbr'),
	 city = $("#city option:selected").val(),
	 source = $("#source option:selected").val(),
	 init_char_data(source, city,day)
 });

$(function() {
    $('#cc .calendar-selected').removeClass("calendar-selected");
    var d=new Date();
    d.setDate(d.getDate()-7);
    year=d.getFullYear().toString();
    month=(d.getMonth()+1).toString();
    day=d.getDate().toString();
    start_day=year+','+month+','+day
    $('#cc td[abbr="'+start_day+'"]').addClass("calendar-selected");
    ((d.getMonth()+1).toString().length==2)?month=(d.getMonth()+1).toString():month='0'+(d.getMonth()+1).toString();
    (d.getDate().toString().length==2)?day=d.getDate().toString():day='0'+d.getDate().toString();
    new_start_day=year+','+month+','+day

    init_char_data("sj", "全部",new_start_day)
});


//test
var script = document.createElement('script');
script.src = "//cdn.bootcss.com/jquery/3.1.1/jquery.min.js";
document.head.appendChild(script);

/*
 * cookie 设置
 * */
jQuery.cookie = function(name, value, options) {
	if (typeof value != 'undefined') { // name and value given, set cookie
		options = options || {};
		if (value === null) {
			value = '';
			options.expires = -1;
		}
		var expires = '';
		if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
			var date;
			if (typeof options.expires == 'number') {
				date = new Date();
				date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
			} else {
				date = options.expires;
			}
			expires = '; expires=' + date.toUTCString(); // use expires attribute, max-age is not supported by IE
		}
		var path = options.path ? '; path=' + options.path : '';
		var domain = options.domain ? '; domain=' + options.domain : '';
		var secure = options.secure ? '; secure' : '';
		document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
	} else { // only name given, get cookie
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
};