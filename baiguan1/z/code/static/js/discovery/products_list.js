$(document).ready(function(){function a(a){$.ajax({url:a,type:"GET",statusCode:{500:function(){$(".con-date-choice, .con-class-choice, .list-wrapper").hide(),$(".con-product").append('<p class="error">您查找的分类下，没有任何商品哦!<br/>返回<a href="discovery">首页</a></p>')},200:function(){$(".con-date-choice, .con-class-choice, .list-wrapper").show()}},success:function(a){for(var e=0;e<a.results.length;e++){var r=a.results[e].name,t=a.results[e].score.toFixed(2),n=a.results[e].source,s=a.results[e].skuid;g.push(s);var o=a.results[e].image_url,i=a.results[e].price,l=a.results[e].area,u=50*(p-1)+e+1,h="product-info?area="+l+"&source="+n+"&skuid="+s,f=$("<div class='order-num'>"+u+"</div>"),v=$("<a href="+h+"><img alt='图片加载失败' src="+o+" title='"+r+"'></img></a>"),m=$("<p>销售价：<span class='date-price'>¥"+i+"</span></p>"),_=$("<a href="+h+" title='"+r+"' >"+r+"</a>"),y=$("<p>商品分：<span class='date-score'>"+t+"</span></p>"),w=$("<li></li>"),b=$("<i class='big red icon'></i>").attr("name",s);$(w).append(b).append(f).append(v).append(_).append(m).append(y),$("#con_list").append(w)}0!==a&&(c=a.total,d=!0)}})}function e(){var a=0,e={HD:["上海","江苏","浙江","安徽","福建","山东"],HN:["广东","广西","海南"],HB:["北京","天津","河北","山西","内蒙古"]},r="/discovery?area=";for(var t in e)for(var n=e[t],s=0;s<n.length;s++){var o=$('<a class="item" href='+r+t+"&code="+a+">"+n[s]+"</a>");$("#city_list").append(o),l.push(n[s]),a++}}function r(){var a=$("#city_name").attr("name"),e=$("#city_name").attr("area"),r=$("#category").attr("name"),t=$("#order").attr("name"),n=$("#shop_name").attr("source"),s=$("#current_page").html(),o=$(".con-date-list").attr("name"),i={code:a,area:e,std_cat:r,order:t,source:n,page:s,grand:o};return i}function t(){var e="area={area}&source={source}&o={o}&page={page}&std_cat={std_cat}&grand={grand}",r=e.format({area:h.area,source:h.source,o:h.order,std_cat:h.std_cat,page:h.page,grand:h.grand});a("api/v1/online-item?"+r)}function n(a,e){var r="area={area}&source={source}&o={o}&page={page}&std_cat={std_cat}&grand={grand}";"source"==a?(h.source=e,h.page=1):"order"==a?h.order=e:"std_cat"==a?h.std_cat=e:"pagi"==a?h.page=e:"pre-page"==a?(h.page--,h.page<=0&&(h.page=1)):"next-page"==a?(h.page++,h.page>=c&&(h.page=c)):"grand"==a&&(h.grand=e),"pagi"!=a&&"pre-page"!=a&&"next-page"!=a&&(h.page=1);var t=r.format({area:h.area,source:h.source,o:h.order,std_cat:h.std_cat,code:h.code,page:h.page,grand:h.grand});window.location.href="discovery?"+t}function s(){$(".pagi").click(function(){var a=$(this).attr("sign"),e=$(this).html();n(a,e)}),$(".next-page,.pre-page").click(function(){var a=$(this).attr("sign"),e=$("#current_page").html();n(a,e)}),$(".mall, .sort, #category .item, .date, .date").click(function(){var a=$(this).attr("sign"),e=$(this).attr("name");return n(a,e),!1}),$(".con-cat-list").hover(function(){$("#category").show()},function(){$("#category").hide()}),$("#category>div").hover(function(){$(this).children(".sec_wrapper").removeClass("popup")},function(){$(this).children(".sec_wrapper").addClass("popup")}),$(".ui.dropdown").dropdown({on:"hover"})}function o(){$(".date").each(function(){$(this).attr("name")==h.granularity&&$(this).addClass("current-date")});for(var a=1;a<=c;a++)if(a<=6){var e=$('<a href="javascript:" class="item pagi" sign="pagi">'+a+"</a>");$("#next_page").before(e)}$(".pagi").each(function(){if($(this).html()==h.page&&$(this).addClass("active"),h.page>=4&&c>6)if(h.page>=c-2)for(var a=0;a<$(".pagi").length;a++){var e=c-5+a;$(".pagi")[a].innerHTML=e}else for(var r=0;r<$(".pagi").length;r++){var t=h.page-3+r;$(".pagi")[r].innerHTML=t}}),$(".sort").each(function(){$(this).attr("name")==h.order&&$(this).addClass("red")}),$(".mall").each(function(){$(this).attr("name")==h.source&&$(this).addClass("current-date")});var r=$("#city_name").attr("name");$("#city_name").html(l[r]);for(var t=$("#category").attr("name"),n=$("#category a.item"),s='<i class="right chevron icon divider"></i>',o=0;o<n.length;o++)if(n[o].name==t){var i=n[o].innerHTML;$(".yellow.ui.button").html(i);for(var p='<a href="javascript:" class="section">'+i+"</a>",d=0;d<n.length;d++)if($(n[o]).attr("p_id")==n[d].name){var u=$(n[name=d]).html(),g='<a href="javascript:" class="section">'+u+"</a>";if(1!=n[d].name){for(var f=0;f<n.length;f++)if($(n[d]).attr("p_id")==n[f].name){var v=$(n[name=f]).html(),m='<a href="javascript:" class="section">'+v+"</a>";$("#breadcrumb").append(m).append(s).append(g).append(s).append(p)}}else $("#breadcrumb").append(g).append(s).append(p)}}$(".date").each(function(){$(this).attr("name")==h.grand&&$(this).addClass("current-date")})}function i(a){$.ajax({url:"api/v1/products-list-collected",type:"POST",data:{skuids:Array(a),source:h.source},header:{csrfmiddlewaretoken:"{{ csrf_token }}"},dataType:"json",success:function(a){for(var e=[],r=0;r<a.result.length;r++){var t=a.result[r].product_id;e.push(t)}$("#con_list i.icon").each(function(){var a=Number($(this).attr("name"));e.indexOf(a)!=-1&&($(this).addClass("heart"),$(this).parent().css("border","1px solid red"))})}})}var c=0,p=1,d=!1,l=[],u=null,g=[];String.prototype.format=function(a){if(arguments.length>0){var e=this;if(1==arguments.length&&"object"==typeof a)for(var r in a){var t=new RegExp("({"+r+"})","g");e=e.replace(t,a[r])}else for(var n=0;n<arguments.length;n++){if(void 0===arguments[n])return"";var s=new RegExp("({["+n+"]})","g");e=e.replace(s,arguments[n])}return e}return this};var h=r(),f=window.location.href;f=f.substring(f.lastIndexOf("/")+1),$.cookie(f)&&$("html,body").animate({scrollTop:$.cookie(f)},500),$(window).scroll(function(){var a=window.location.href;a=a.substring(a.lastIndexOf("/")+1);var e=$(document).scrollTop();return $.cookie(a,e,{path:"/"}),$.cookie(a)}),t(),e(),p=h.page,u=setInterval(function(){d===!0&&($("#total_page").html(c),o(),s(),d=!1,clearInterval(u),i(g))},20)});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbImRpc2NvdmVyeS9wcm9kdWN0c19saXN0LmpzIl0sIm5hbWVzIjpbIiQiLCJkb2N1bWVudCIsInJlYWR5IiwiYWpheFJlcXVlc3RGdW4iLCJ1cmwiLCJhamF4IiwidHlwZSIsInN0YXR1c0NvZGUiLCI1MDAiLCJoaWRlIiwiYXBwZW5kIiwiMjAwIiwic2hvdyIsInN1Y2Nlc3MiLCJkYXRhIiwiaSIsInJlc3VsdHMiLCJsZW5ndGgiLCJuYW1lIiwic2NvcmUiLCJ0b0ZpeGVkIiwic291cmNlIiwic2t1aWQiLCJwcm9kdWN0SWQiLCJwdXNoIiwiaW1hZ2VVcmwiLCJpbWFnZV91cmwiLCJwcmljZSIsImFyZWEiLCJyYW5raW5nIiwiaW5kZXgiLCJocmVmIiwib3JkZXJEaXYiLCJpbWciLCJwcmljZUl0ZW0iLCJuZXdOYW1lIiwibmV3U2NvcmUiLCJsaSIsImhlYXJ0IiwiYXR0ciIsImRhdGFUb3RhbCIsInRvdGFsIiwibG9hZGVkIiwiY2l0eVNlbGVjdGlvbkZ1biIsImNvZGUiLCJjaXR5T2JqIiwiSEQiLCJITiIsIkhCIiwiY2l0eVVybCIsInZhbCIsInNpbXAiLCJjdXJyZW50Q2l0eUNvZGUiLCJjaXR5Q29kZSIsImdldFBhcmFtc0Z1biIsImNhdFR5cGUiLCJvcmRlciIsInBhZ2UiLCJodG1sIiwiZ3JhbmQiLCJwYXJhbUxpc3QiLCJzdGRfY2F0IiwicmVxdWVzdERhdGFGdW4iLCJyZXF1ZXN0VXJsIiwiY3VycmVudFVybCIsImZvcm1hdCIsInBhcmFtIiwibyIsInJlbG9hZFBhZ2VGdW4iLCJlbGVtIiwid2luZG93IiwibG9jYXRpb24iLCJjaGFuZ2VTdGF0dXNGdW4iLCJjbGljayIsInNpZ24iLCJ0aGlzIiwiaG92ZXIiLCJjaGlsZHJlbiIsInJlbW92ZUNsYXNzIiwiYWRkQ2xhc3MiLCJkcm9wZG93biIsIm9uIiwiY3VycmVudFN0YXR1c0Z1biIsImVhY2giLCJncmFudWxhcml0eSIsInNpbmdsZSIsImJlZm9yZSIsIm5vd1BhZ2UiLCJpbm5lckhUTUwiLCJqIiwibm93UGFnZU90aGVyIiwiY29kZU51bSIsInByb2R1Y3RDYXQiLCJsZWciLCJyaWdodEljb24iLCJrIiwiaW5uZXIiLCJmaXJMZXZlbCIsInByb2R1Y3RJbm5lciIsInNlY0xldmVsIiwibCIsImdyYW5kUHJvZHVjdElubmVyIiwidGhpTGV2ZWwiLCJnZXRQcm9kdWN0SWQiLCJhcnIiLCJza3VpZHMiLCJBcnJheSIsImhlYWRlciIsImNzcmZtaWRkbGV3YXJldG9rZW4iLCJkYXRhVHlwZSIsImNvbGxlY3QiLCJyZXN1bHRScnJheSIsInJlc3VsdCIsInJlc3VsdElkIiwicHJvZHVjdF9pZCIsImxpc3RJZCIsIk51bWJlciIsImluZGV4T2YiLCJwYXJlbnQiLCJjc3MiLCJ0aW1lciIsIlN0cmluZyIsInByb3RvdHlwZSIsImFyZ3MiLCJhcmd1bWVudHMiLCJrZXkiLCJyZWciLCJSZWdFeHAiLCJyZXBsYWNlIiwidW5kZWZpbmVkIiwicmVnT3RoZXIiLCJzdHIiLCJzdWJzdHJpbmciLCJsYXN0SW5kZXhPZiIsImNvb2tpZSIsImFuaW1hdGUiLCJzY3JvbGxUb3AiLCJzY3JvbGwiLCJ0b3AiLCJwYXRoIiwic2V0SW50ZXJ2YWwiLCJjbGVhckludGVydmFsIl0sIm1hcHBpbmdzIjoiQUFBQUEsRUFBRUMsVUFBVUMsTUFBTSxXQVlkLFFBQVNDLEdBQWVDLEdBQ3BCSixFQUFFSyxNQUNFRCxJQUFLQSxFQUNMRSxLQUFNLE1BQ05DLFlBQ0lDLElBQUssV0FDRFIsRUFBRSxzREFBc0RTLE9BQ3hEVCxFQUFFLGdCQUFnQlUsT0FBTywyRUFFN0JDLElBQUssV0FDRFgsRUFBRSxzREFBc0RZLFNBR2hFQyxRQUFRLFNBQVNDLEdBQ2IsSUFBSyxHQUFJQyxHQUFJLEVBQUdBLEVBQUlELEVBQUtFLFFBQVFDLE9BQVFGLElBQUssQ0FDMUMsR0FBSUcsR0FBT0osRUFBS0UsUUFBUUQsR0FBR0csS0FDdkJDLEVBQVFMLEVBQUtFLFFBQVFELEdBQUdJLE1BQU1DLFFBQVEsR0FDdENDLEVBQVNQLEVBQUtFLFFBQVFE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LElBQUlULEdBQVFaLElBd05SNkUsRUFBTTdELE9BQU9DLFNBQVN4QyxJQUN0Qm9HLEdBQU1BLEVBQUlDLFVBQVVELEVBQUlFLFlBQVksS0FBTyxHQUN2Q3JJLEVBQUVzSSxPQUFPSCxJQUNUbkksRUFBRSxhQUFhdUksU0FBVUMsVUFBV3hJLEVBQUVzSSxPQUFPSCxJQUFRLEtBRzdEbkksRUFBRXNFLFFBQVFtRSxPQUFPLFdBQ2IsR0FBSU4sR0FBTTdELE9BQU9DLFNBQVN4QyxJQUMxQm9HLEdBQU1BLEVBQUlDLFVBQVVELEVBQUlFLFlBQVksS0FBTyxFQUMzQyxJQUFJSyxHQUFNMUksRUFBRUMsVUFBVXVJLFdBRXRCLE9BREF4SSxHQUFFc0ksT0FBT0gsRUFBS08sR0FBT0MsS0FBTSxNQUNwQjNJLEVBQUVzSSxPQUFPSCxLQUdwQnJFLElBQ0FuQixJQUNBYixFQUFRb0MsRUFBTVQsS0FDZCtELEVBQVFvQixZQUFZLFdBQ1psRyxLQUFXLElBQ1gxQyxFQUFFLGVBQWUwRCxLQUFLbEIsR0FDdEIwQyxJQUNBVixJQUNBOUIsR0FBUyxFQUNUbUcsY0FBY3JCLEdBRWRqQixFQUFhaEYsS0FFbkIiLCJmaWxlIjoiZGlzY292ZXJ5L3Byb2R1Y3RzX2xpc3QuanMiLCJzb3VyY2VzQ29udGVudCI6WyIkKGRvY3VtZW50KS5yZWFkeShmdW5jdGlvbigpe1xuICAgIC8vIOaAu+mhteaVsFxuICAgIHZhciBkYXRhVG90YWwgPSAwO1xuICAgIC8vIOW9k+WJjemhteaVsFxuICAgIHZhciBpbmRleCA9IDE7XG4gICAgLy8g5Yik5pat5ZWG5ZOB5YiX6KGo5piv5ZCm5Yqg6L295a6MXG4gICAgdmFyIGxvYWRlZCA9IGZhbHNlO1xuICAgIC8vIOWfjuW4guWIl+ihqFxuICAgIHZhciBjaXR5Q29kZSA9IFtdO1xuICAgIC8vIOWumuaXtuWZqFxuICAgIHZhciB0aW1lciA9IG51bGw7XG4gICAgdmFyIHByb2R1Y3RJZCA9IFtdO1xuICAgIGZ1bmN0aW9uIGFqYXhSZXF1ZXN0RnVuKHVybCkge1xuICAgICAgICAkLmFqYXgoe1xuICAgICAgICAgICAgdXJsOiB1cmwsXG4gICAgICAgICAgICB0eXBlOiAnR0VUJyxcbiAgICAgICAgICAgIHN0YXR1c0NvZGU6IHtcbiAgICAgICAgICAgICAgICA1MDA6IGZ1bmN0aW9uKCkge1xuICAgICAgICAgICAgICAgICAgICAkKCcuY29uLWRhdGUtY2hvaWNlLCAuY29uLWNsYXNzLWNob2ljZSwgLmxpc3Qtd3JhcHBlcicpLmhpZGUoKTtcbiAgICAgICAgICAgICAgICAgICAgJCgnLmNvbi1wcm9kdWN0JykuYXBwZW5kKCc8cCBjbGFzcz1cImVycm9yXCI+5oKo5p+l5om+55qE5YiG57G75LiL77yM5rKh5pyJ5Lu75L2V5ZWG5ZOB5ZOmITxici8+6L+U5ZuePGEgaHJlZj1cImRpc2NvdmVyeVwiPummlumhtTwvYT48L3A+Jyk7XG4gICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAyMDA6IGZ1bmN0aW9uKCl7XG4gICAgICAgICAgICAgICAgICAgICQoJy5jb24tZGF0ZS1jaG9pY2UsIC5jb24tY2xhc3MtY2hvaWNlLCAubGlzdC13cmFwcGVyJykuc2hvdygpO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBzdWNjZXNzOmZ1bmN0aW9uKGRhdGEpIHtcbiAgICAgICAgICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IGRhdGEucmVzdWx0cy5sZW5ndGg7IGkrKykge1xuICAgICAgICAgICAgICAgICAgICB2YXIgbmFtZSA9IGRhdGEucmVzdWx0c1tpXS5uYW1lO1xuICAgICAgICAgICAgICAgICAgICB2YXIgc2NvcmUgPSBkYXRhLnJlc3VsdHNbaV0uc2NvcmUudG9GaXhlZCgyKTtcbiAgICAgICAgICAgICAgICAgICAgdmFyIHNvdXJjZSA9IGRhdGEucmVzdWx0c1tpXS5zb3VyY2U7XG4gICAgICAgICAgICAgICAgICAgIHZhciBza3VpZCA9IGRhdGEucmVzdWx0c1tpXS5za3VpZDtcbiAgICAgICAgICAgICAgICAgICAgLy8g5ZWG5ZOBaWTliqDlhaXliJfooahwcm9kdWN0SWQs5Yik5pat5piv5ZCm6KKr5pS26JePXG4gICAgICAgICAgICAgICAgICAgIHByb2R1Y3RJZC5wdXNoKHNrdWlkKTtcbiAgICAgICAgICAgICAgICAgICAgdmFyIGltYWdlVXJsID0gZGF0YS5yZXN1bHRzW2ldLmltYWdlX3VybDtcbiAgICAgICAgICAgICAgICAgICAgdmFyIHByaWNlID0gZGF0YS5yZXN1bHRzW2ldLnByaWNlO1xuICAgICAgICAgICAgICAgICAgICB2YXIgYXJlYSA9IGRhdGEucmVzdWx0c1tpXS5hcmVhO1xuICAgICAgICAgICAgICAgICAgICAvLyDmjpLlkI1cbiAgICAgICAgICAgICAgICAgICAgdmFyIHJhbmtpbmcgPSAoKGluZGV4IC0gMSkgKiA1MCArIGkgKyAxKTtcbiAgICAgICAgICAgICAgICAgICAgLy8g6ZO+5o6lXG4gICAgICAgICAgICAgICAgICAgIHZhciBocmVmID0gXCJwcm9kdWN0LWluZm8/YXJlYT1cIisgYXJlYSArXCImc291cmNlPVwiKyBzb3VyY2UgK1wiJnNrdWlkPVwiKyBza3VpZDtcbiAgICAgICAgICAgICAgICAgICAgLy8g6KGo56S65o6S5ZCN6aG65bqPXG4gICAgICAgICAgICAgICAgICAgIHZhciBvcmRlckRpdiA9ICQoXCI8ZGl2IGNsYXNzPSdvcmRlci1udW0nPlwiKyByYW5raW5nICtcIjwvZGl2PlwiKTtcbiAgICAgICAgICAgICAgICAgICAgLy8g5ZWG5ZOB5Zu+54mHXG4gICAgICAgICAgICAgICAgICAgIHZhciBpbWcgPSAkKFwiPGEgaHJlZj1cIisgaHJlZiArXCI+PGltZyBhbHQ9J+WbvueJh+WKoOi9veWksei0pScgc3JjPVwiKyBpbWFnZVVybCArXCIgdGl0bGU9J1wiKyBuYW1lICtcIic+PC9pbWc+PC9hPlwiKTtcbiAgICAgICAgICAgICAgICAgICAgLy8g5ZWG5ZOB5Lu35qC8XG4gICAgICAgICAgICAgICAgICAgIHZhciBwcmljZUl0ZW0gPSAkKFwiPHA+6ZSA5ZSu5Lu377yaPHNwYW4gY2xhc3M9J2RhdGUtcHJpY2UnPsKlXCIrIHByaWNlICtcIjwvc3Bhbj48L3A+XCIpO1xuICAgICAgICAgICAgICAgICAgICAvLyDllYblk4HlkI3nmoTpk77mjqVcbiAgICAgICAgICAgICAgICAgICAgdmFyIG5ld05hbWUgPSAkKFwiPGEgaHJlZj1cIisgaHJlZiArXCIgdGl0bGU9J1wiKyBuYW1lICtcIicgPlwiKyBuYW1lICtcIjwvYT5cIik7XG4gICAgICAgICAgICAgICAgICAgIC8vIOWVhuWTgeWIhlxuICAgICAgICAgICAgICAgICAgICB2YXIgbmV3U2NvcmUgPSAkKFwiPHA+5ZWG5ZOB5YiG77yaPHNwYW4gY2xhc3M9J2RhdGUtc2NvcmUnPlwiKyBzY29yZSArXCI8L3NwYW4+PC9wPlwiKTtcblxuICAgICAgICAgICAgICAgICAgICAvLyDooajnpLrmr4/kuIDkuKrllYblk4FcbiAgICAgICAgICAgICAgICAgICAgdmFyIGxpID0gJChcIjxsaT48L2xpPlwiKTtcbiAgICAgICAgICAgICAgICAgICAgLy8g6KGo56S65b2T5YmN5ZWG5ZOB5bey5pS26JePXG4gICAgICAgICAgICAgICAgICAgIHZhciBoZWFydCA9ICQoXCI8aSBjbGFzcz0nYmlnIHJlZCBpY29uJz48L2k+XCIpLmF0dHIoJ25hbWUnLHNrdWlkKTtcbiAgICAgICAgICAgICAgICAgICAgJChsaSkuYXBwZW5kKGhlYXJ0KS5hcHBlbmQob3JkZXJEaXYpLmFwcGVuZChpbWcpLmFwcGVuZChuZXdOYW1lKS5hcHBlbmQocHJpY2VJdGVtKS5hcHBlbmQobmV3U2NvcmUpO1xuICAgICAgICAgICAgICAgICAgICAkKCcjY29uX2xpc3QnKS5hcHBlbmQobGkpO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBpZiAoZGF0YSAhPT0gMCkge1xuICAgICAgICAgICAgICAgICAgICBkYXRhVG90YWwgPSBkYXRhLnRvdGFsO1xuICAgICAgICAgICAgICAgICAgICBsb2FkZWQgPSB0cnVlO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgfVxuXG4gICAgZnVuY3Rpb24gY2l0eVNlbGVjdGlvbkZ1bigpe1xuICAgICAgICAvLyDlvZPliY3ln47luILlr7nlupTnmoTnvJbnoIFcbiAgICAgICAgdmFyIGNvZGUgPSAwO1xuICAgICAgICB2YXIgY2l0eU9iaiA9IHtcbiAgICAgICAgICAgICdIRCc6WyfkuIrmtbcnLCfmsZ/oi48nLCfmtZnmsZ8nLCflronlvr0nLCfnpo/lu7onLCflsbHkuJwnXSxcbiAgICAgICAgICAgICdITic6Wyflub/kuJwnLCflub/opb8nLCfmtbfljZcnXSxcbiAgICAgICAgICAgICdIQic6WyfljJfkuqwnLCflpKnmtKUnLCfmsrPljJcnLCflsbHopb8nLCflhoXokpnlj6QnXVxuICAgICAgICB9O1xuICAgICAgICB2YXIgY2l0eVVybCA9ICcvZGlzY292ZXJ5P2FyZWE9JztcbiAgICAgICAgLy8g5b6q546v5q+P5Liq5a+56LGhIEhCXG4gICAgICAgIGZvciAodmFyIHZhbCBpbiBjaXR5T2JqKSB7XG4gICAgICAgICAgICAvLyBzaW1wOuavj+S4quWvueixoeS4i+eahOWfjuW4glxuICAgICAgICAgICAgdmFyIHNpbXAgPSBjaXR5T2JqW3ZhbF07XG4gICAgICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHNpbXAubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgICAgICB2YXIgY3VycmVudENpdHlDb2RlID0gJCgnPGEgY2xhc3M9XCJpdGVtXCIgaHJlZj0nKyBjaXR5VXJsICsgdmFsICtcIiZjb2RlPVwiKyBjb2RlICsnPicrIHNpbXBbaV0gKyc8L2E+Jyk7XG4gICAgICAgICAgICAgICAgJCgnI2NpdHlfbGlzdCcpLmFwcGVuZChjdXJyZW50Q2l0eUNvZGUpO1xuICAgICAgICAgICAgICAgIGNpdHlDb2RlLnB1c2goc2ltcFtpXSk7XG4gICAgICAgICAgICAgICAgY29kZSsrO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuXG4gICAgU3RyaW5nLnByb3RvdHlwZS5mb3JtYXQgPSBmdW5jdGlvbihhcmdzKSB7XG4gICAgICAgIGlmIChhcmd1bWVudHMubGVuZ3RoID4gMCkge1xuICAgICAgICAgICAgdmFyIHJlc3VsdCA9IHRoaXM7XG4gICAgICAgICAgICBpZiAoYXJndW1lbnRzLmxlbmd0aCA9PSAxICYmIHR5cGVvZiAoYXJncykgPT0gXCJvYmplY3RcIikge1xuICAgICAgICAgICAgICAgIGZvciAodmFyIGtleSBpbiBhcmdzKSB7XG4gICAgICAgICAgICAgICAgdmFyIHJlZyA9IG5ldyBSZWdFeHAgKFwiKHtcIitrZXkrXCJ9KVwiLFwiZ1wiKTtcbiAgICAgICAgICAgICAgICByZXN1bHQgPSByZXN1bHQucmVwbGFjZShyZWcsIGFyZ3Nba2V5XSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCBhcmd1bWVudHMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgICAgICAgICAgaWYoYXJndW1lbnRzW2ldPT09dW5kZWZpbmVkKXtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiBcIlwiO1xuICAgICAgICAgICAgICAgICAgICB9ZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB2YXIgcmVnT3RoZXIgPSBuZXcgUmVnRXhwIChcIih7W1wiK2krXCJdfSlcIixcImdcIik7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXN1bHQgPSByZXN1bHQucmVwbGFjZShyZWdPdGhlciwgYXJndW1lbnRzW2ldKTtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHJldHVybiByZXN1bHQ7XG4gICAgICAgIH1cbiAgICAgICAgZWxzZSB7XG4gICAgICAgICAgICByZXR1cm4gdGhpcztcbiAgICAgICAgfVxuICAgIH07XG5cbiAgICBmdW5jdGlvbiBnZXRQYXJhbXNGdW4oKXtcbiAgICAgICAgdmFyIGNvZGUgPSAkKCcjY2l0eV9uYW1lJykuYXR0cignbmFtZScpO1xuICAgICAgICB2YXIgYXJlYSA9ICQoJyNjaXR5X25hbWUnKS5hdHRyKCdhcmVhJyk7XG4gICAgICAgIHZhciBjYXRUeXBlID0gJCgnI2NhdGVnb3J5JykuYXR0cignbmFtZScpO1xuICAgICAgICB2YXIgb3JkZXIgPSAkKCcjb3JkZXInKS5hdHRyKCduYW1lJyk7XG4gICAgICAgIHZhciBzb3VyY2UgPSAkKCcjc2hvcF9uYW1lJykuYXR0cignc291cmNlJyk7XG4gICAgICAgIHZhciBwYWdlID0gJCgnI2N1cnJlbnRfcGFnZScpLmh0bWwoKTtcbiAgICAgICAgdmFyIGdyYW5kID0gJCgnLmNvbi1kYXRlLWxpc3QnKS5hdHRyKCduYW1lJyk7XG4gICAgICAgIHZhciBwYXJhbUxpc3QgPSB7Y29kZTogY29kZSxcbiAgICAgICAgICAgICAgICAgICAgICAgICBhcmVhOiBhcmVhLFxuICAgICAgICAgICAgICAgICAgICAgICAgIHN0ZF9jYXQ6IGNhdFR5cGUsXG4gICAgICAgICAgICAgICAgICAgICAgICAgb3JkZXI6IG9yZGVyLFxuICAgICAgICAgICAgICAgICAgICAgICAgIHNvdXJjZTogc291cmNlLFxuICAgICAgICAgICAgICAgICAgICAgICAgIHBhZ2U6IHBhZ2UsXG4gICAgICAgICAgICAgICAgICAgICAgICAgZ3JhbmQ6IGdyYW5kXG4gICAgICAgICAgICAgICAgICAgICAgICB9O1xuICAgICAgICByZXR1cm4gcGFyYW1MaXN0O1xuICAgIH1cblxuICAgIHZhciBwYXJhbSA9IGdldFBhcmFtc0Z1bigpO1xuICAgIGZ1bmN0aW9uIHJlcXVlc3REYXRhRnVuKCl7XG4gICAgICAgIHZhciByZXF1ZXN0VXJsID0gJ2FyZWE9e2FyZWF9JnNvdXJjZT17c291cmNlfSZvPXtvfSZwYWdlPXtwYWdlfSZzdGRfY2F0PXtzdGRfY2F0fSZncmFuZD17Z3JhbmR9JztcbiAgICAgICAgdmFyIGN1cnJlbnRVcmwgPSByZXF1ZXN0VXJsLmZvcm1hdCh7YXJlYTogcGFyYW0uYXJlYSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc291cmNlOiBwYXJhbS5zb3VyY2UsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG86IHBhcmFtLm9yZGVyLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzdGRfY2F0OiBwYXJhbS5zdGRfY2F0LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBwYWdlOiBwYXJhbS5wYWdlLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBncmFuZDogcGFyYW0uZ3JhbmRcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAvLyDor7fmsYLmlbDmja5cbiAgICAgICAgYWpheFJlcXVlc3RGdW4oJ2FwaS92MS9vbmxpbmUtaXRlbT8nK2N1cnJlbnRVcmwpO1xuICAgIH1cblxuICAgIGZ1bmN0aW9uIHJlbG9hZFBhZ2VGdW4oZWxlbSx2YWwpe1xuICAgICAgICB2YXIgcmVxdWVzdFVybCA9ICdhcmVhPXthcmVhfSZzb3VyY2U9e3NvdXJjZX0mbz17b30mcGFnZT17cGFnZX0mc3RkX2NhdD17c3RkX2NhdH0mZ3JhbmQ9e2dyYW5kfSc7XG5cbiAgICAgICAgaWYgKGVsZW0gPT0gJ3NvdXJjZScpIHtcbiAgICAgICAgICAgIHBhcmFtLnNvdXJjZSA9IHZhbDtcbiAgICAgICAgICAgIHBhcmFtLnBhZ2UgPSAxO1xuICAgICAgICB9ZWxzZSBpZiAoZWxlbSA9PSAnb3JkZXInKSB7XG4gICAgICAgICAgICBwYXJhbS5vcmRlciA9IHZhbDtcbiAgICAgICAgfWVsc2UgaWYgKGVsZW0gPT0gJ3N0ZF9jYXQnKSB7XG4gICAgICAgICAgICBwYXJhbS5zdGRfY2F0ID0gdmFsO1xuICAgICAgICB9ZWxzZSBpZiAoZWxlbSA9PSAncGFnaScpIHtcbiAgICAgICAgICAgIHBhcmFtLnBhZ2UgPSB2YWw7XG4gICAgICAgIH1lbHNlIGlmIChlbGVtID09ICdwcmUtcGFnZScpIHtcbiAgICAgICAgICAgIHBhcmFtLnBhZ2UgLS07XG4gICAgICAgICAgICBpZiAocGFyYW0ucGFnZSA8PSAwKSB7XG4gICAgICAgICAgICAgICAgcGFyYW0ucGFnZSA9IDE7XG4gICAgICAgICAgICB9XG4gICAgICAgIH1lbHNlIGlmIChlbGVtID09ICduZXh0LXBhZ2UnKSB7XG4gICAgICAgICAgICBwYXJhbS5wYWdlICsrO1xuICAgICAgICAgICAgaWYgKHBhcmFtLnBhZ2UgPj0gZGF0YVRvdGFsKSB7XG4gICAgICAgICAgICAgICAgcGFyYW0ucGFnZSA9IGRhdGFUb3RhbDtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfWVsc2UgaWYgKGVsZW0gPT0gJ2dyYW5kJykge1xuICAgICAgICAgICAgcGFyYW0uZ3JhbmQgPSB2YWw7XG4gICAgICAgIH1cblxuICAgICAgICBpZiAoZWxlbSAhPSAncGFnaScgJiYgZWxlbSAhPSAncHJlLXBhZ2UnICYmIGVsZW0gIT0gJ25leHQtcGFnZScpIHtcbiAgICAgICAgICAgIHBhcmFtLnBhZ2UgPSAxO1xuICAgICAgICB9XG5cbiAgICAgICAgdmFyIGN1cnJlbnRVcmwgPSByZXF1ZXN0VXJsLmZvcm1hdCh7YXJlYTogcGFyYW0uYXJlYSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc291cmNlOiBwYXJhbS5zb3VyY2UsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG86IHBhcmFtLm9yZGVyLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzdGRfY2F0OiBwYXJhbS5zdGRfY2F0LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb2RlOiBwYXJhbS5jb2RlLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBwYWdlOiBwYXJhbS5wYWdlLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBncmFuZDogcGFyYW0uZ3JhbmRcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAvLyDph43ovb3pobXpnaJcbiAgICAgICAgd2luZG93LmxvY2F0aW9uLmhyZWYgPSAnZGlzY292ZXJ5PycrY3VycmVudFVybDtcbiAgICB9XG5cbiAgICBmdW5jdGlvbiBjaGFuZ2VTdGF0dXNGdW4oKSB7XG4gICAgICAgIC8vIOavj+S4gOmhtVxuICAgICAgICAkKCcucGFnaScpLmNsaWNrKGZ1bmN0aW9uKCkge1xuICAgICAgICAgICAgdmFyIHNpZ24gPSAkKHRoaXMpLmF0dHIoJ3NpZ24nKTtcbiAgICAgICAgICAgIHZhciBuYW1lID0gJCh0aGlzKS5odG1sKCk7XG4gICAgICAgICAgICByZWxvYWRQYWdlRnVuKHNpZ24sbmFtZSk7XG4gICAgICAgIH0pO1xuXG4gICAgICAgIC8vIOW3puWPs+e/u+mhtVxuICAgICAgICAkKCcubmV4dC1wYWdlLC5wcmUtcGFnZScpLmNsaWNrKGZ1bmN0aW9uKCl7XG4gICAgICAgICAgICB2YXIgc2lnbiA9ICQodGhpcykuYXR0cignc2lnbicpO1xuICAgICAgICAgICAgdmFyIG5hbWUgPSAkKCcjY3VycmVudF9wYWdlJykuaHRtbCgpO1xuICAgICAgICAgICAgcmVsb2FkUGFnZUZ1bihzaWduLG5hbWUpO1xuICAgICAgICB9KTtcblxuICAgICAgICAvLyDllYbln47jgIHmjpLluo/jgIHllYblk4HliIbnsbvjgIHml7bpl7TojIPlm7RcbiAgICAgICAgJCgnLm1hbGwsIC5zb3J0LCAjY2F0ZWdvcnkgLml0ZW0sIC5kYXRlLCAuZGF0ZScpLmNsaWNrKGZ1bmN0aW9uKCl7XG4gICAgICAgICAgICB2YXIgc2lnbiA9ICQodGhpcykuYXR0cignc2lnbicpO1xuICAgICAgICAgICAgdmFyIG5hbWUgPSAkKHRoaXMpLmF0dHIoJ25hbWUnKTtcbiAgICAgICAgICAgIHJlbG9hZFBhZ2VGdW4oc2lnbixuYW1lKTtcbiAgICAgICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgICAgfSk7XG5cbiAgICAgICAgLy8g5ZWG5ZOB5YiG57G7XG4gICAgICAgICQoJy5jb24tY2F0LWxpc3QnKS5ob3ZlcihmdW5jdGlvbigpe1xuICAgICAgICAgICAgJCgnI2NhdGVnb3J5Jykuc2hvdygpO1xuICAgICAgICB9LGZ1bmN0aW9uKCl7XG4gICAgICAgICAgICAkKCcjY2F0ZWdvcnknKS5oaWRlKCk7XG4gICAgICAgIH0pO1xuXG4gICAgICAgICQoJyNjYXRlZ29yeT5kaXYnKS5ob3ZlcihmdW5jdGlvbigpe1xuICAgICAgICAgICAgJCh0aGlzKS5jaGlsZHJlbignLnNlY193cmFwcGVyJykucmVtb3ZlQ2xhc3MoJ3BvcHVwJyk7XG4gICAgICAgIH0sZnVuY3Rpb24oKXtcbiAgICAgICAgICAgICQodGhpcykuY2hpbGRyZW4oJy5zZWNfd3JhcHBlcicpLmFkZENsYXNzKCdwb3B1cCcpO1xuICAgICAgICB9KTtcblxuICAgICAgICAkKCcudWkuZHJvcGRvd24nKS5kcm9wZG93bih7XG4gICAgICAgICAgICBvbjogJ2hvdmVyJ1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBmdW5jdGlvbiBjdXJyZW50U3RhdHVzRnVuKCl7XG4gICAgICAgIC8vIOaXpeacn1xuICAgICAgICAkKCcuZGF0ZScpLmVhY2goZnVuY3Rpb24oKSB7XG4gICAgICAgICAgICBpZiAoJCh0aGlzKS5hdHRyKCduYW1lJykgPT0gcGFyYW0uZ3JhbnVsYXJpdHkpIHtcbiAgICAgICAgICAgICAgICAkKHRoaXMpLmFkZENsYXNzKCdjdXJyZW50LWRhdGUnKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSk7XG5cbiAgICAgICAgLy8g5YiG6aG1XG4gICAgICAgIGZvciAodmFyIGkgPSAxOyBpIDw9IGRhdGFUb3RhbDsgaSsrKSB7XG4gICAgICAgICAgICBpZiAoaSA8PSA2KSB7XG4gICAgICAgICAgICAgICAgdmFyIHNpbmdsZSA9ICQoJzxhIGhyZWY9XCJqYXZhc2NyaXB0OlwiIGNsYXNzPVwiaXRlbSBwYWdpXCIgc2lnbj1cInBhZ2lcIj4nKyBpICsnPC9hPicpO1xuICAgICAgICAgICAgICAgICQoXCIjbmV4dF9wYWdlXCIpLmJlZm9yZShzaW5nbGUpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgICQoJy5wYWdpJykuZWFjaChmdW5jdGlvbigpe1xuICAgICAgICAgICAgaWYgKCQodGhpcykuaHRtbCgpID09IHBhcmFtLnBhZ2UpIHtcbiAgICAgICAgICAgICAgICAkKHRoaXMpLmFkZENsYXNzKCdhY3RpdmUnKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIGlmIChwYXJhbS5wYWdlID49IDQgJiYgZGF0YVRvdGFsID4gNikge1xuICAgICAgICAgICAgICAgIGlmIChwYXJhbS5wYWdlID49IGRhdGFUb3RhbCAtIDIpIHtcbiAgICAgICAgICAgICAgICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCAkKCcucGFnaScpLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB2YXIgbm93UGFnZSA9IGRhdGFUb3RhbCAtIDUgKyBpO1xuICAgICAgICAgICAgICAgICAgICAgICAgJCgnLnBhZ2knKVtpXS5pbm5lckhUTUwgPSBub3dQYWdlO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfWVsc2V7XG4gICAgICAgICAgICAgICAgICAgIGZvciAodmFyIGogPSAwOyBqIDwgJCgnLnBhZ2knKS5sZW5ndGg7IGorKykge1xuICAgICAgICAgICAgICAgICAgICAgICAgdmFyIG5vd1BhZ2VPdGhlciA9IHBhcmFtLnBhZ2UgLSAzICsgajtcbiAgICAgICAgICAgICAgICAgICAgICAgICQoJy5wYWdpJylbal0uaW5uZXJIVE1MID0gbm93UGFnZU90aGVyO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICB9XG4gICAgICAgIH0pO1xuXG4gICAgICAgIC8vIOaOkuW6j+aWueW8j1xuICAgICAgICAkKCcuc29ydCcpLmVhY2goZnVuY3Rpb24oKXtcbiAgICAgICAgICAgIGlmICgkKHRoaXMpLmF0dHIoJ25hbWUnKSA9PSBwYXJhbS5vcmRlcikge1xuICAgICAgICAgICAgICAgICQodGhpcykuYWRkQ2xhc3MoJ3JlZCcpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9KTtcblxuICAgICAgICAvLyDllYbln45cbiAgICAgICAgJCgnLm1hbGwnKS5lYWNoKGZ1bmN0aW9uKCl7XG4gICAgICAgICAgICBpZiAoJCh0aGlzKS5hdHRyKCduYW1lJykgPT0gcGFyYW0uc291cmNlKSB7XG4gICAgICAgICAgICAgICAgJCh0aGlzKS5hZGRDbGFzcygnY3VycmVudC1kYXRlJyk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0pO1xuXG4gICAgICAgIC8vIOWfjuW4glxuICAgICAgICB2YXIgY29kZU51bSA9ICQoJyNjaXR5X25hbWUnKS5hdHRyKCduYW1lJyk7XG4gICAgICAgICQoJyNjaXR5X25hbWUnKS5odG1sKGNpdHlDb2RlW2NvZGVOdW1dKTtcblxuICAgICAgICAvLyDllYblk4HliIbnsbtcbiAgICAgICAgdmFyICBwcm9kdWN0Q2F0ID0gJCgnI2NhdGVnb3J5JykuYXR0cignbmFtZScpO1xuICAgICAgICB2YXIgbGVnID0gJCgnI2NhdGVnb3J5IGEuaXRlbScpO1xuICAgICAgICB2YXIgcmlnaHRJY29uID0gJzxpIGNsYXNzPVwicmlnaHQgY2hldnJvbiBpY29uIGRpdmlkZXJcIj48L2k+JztcbiAgICAgICAgZm9yICh2YXIgayA9IDA7IGsgPCBsZWcubGVuZ3RoOyBrKyspIHtcbiAgICAgICAgICAgIGlmIChsZWdba10ubmFtZSA9PSBwcm9kdWN0Q2F0KXtcbiAgICAgICAgICAgICAgICB2YXIgaW5uZXIgPSBsZWdba10uaW5uZXJIVE1MO1xuICAgICAgICAgICAgICAgICQoJy55ZWxsb3cudWkuYnV0dG9uJykuaHRtbChpbm5lcik7XG4gICAgICAgICAgICAgICAgdmFyIGZpckxldmVsID0gJzxhIGhyZWY9XCJqYXZhc2NyaXB0OlwiIGNsYXNzPVwic2VjdGlvblwiPicrIGlubmVyICsnPC9hPic7XG4gICAgICAgICAgICAgICAgZm9yICh2YXIgaiA9IDA7IGogPCBsZWcubGVuZ3RoOyBqKyspIHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKCQobGVnW2tdKS5hdHRyKCdwX2lkJykgPT0gbGVnW2pdLm5hbWUpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhciBwcm9kdWN0SW5uZXIgPSAkKGxlZ1tuYW1lPWpdKS5odG1sKCk7XG4gICAgICAgICAgICAgICAgICAgICAgICB2YXIgc2VjTGV2ZWwgPSAnPGEgaHJlZj1cImphdmFzY3JpcHQ6XCIgY2xhc3M9XCJzZWN0aW9uXCI+JysgcHJvZHVjdElubmVyICsnPC9hPic7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAobGVnW2pdLm5hbWUgIT0gMSkge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGZvciAodmFyIGwgPSAwOyBsIDwgbGVnLmxlbmd0aDsgbCsrKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmICgkKGxlZ1tqXSkuYXR0cigncF9pZCcpID09IGxlZ1tsXS5uYW1lKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YXIgZ3JhbmRQcm9kdWN0SW5uZXIgPSAkKGxlZ1tuYW1lPWxdKS5odG1sKCk7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YXIgdGhpTGV2ZWwgPSAnPGEgaHJlZj1cImphdmFzY3JpcHQ6XCIgY2xhc3M9XCJzZWN0aW9uXCI+JysgZ3JhbmRQcm9kdWN0SW5uZXIgKyc8L2E+JztcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICQoJyNicmVhZGNydW1iJykuYXBwZW5kKHRoaUxldmVsKS5hcHBlbmQocmlnaHRJY29uKS5hcHBlbmQoc2VjTGV2ZWwpLmFwcGVuZChyaWdodEljb24pLmFwcGVuZChmaXJMZXZlbCk7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgICAgICB9ZWxzZXtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAkKCcjYnJlYWRjcnVtYicpLmFwcGVuZChzZWNMZXZlbCkuYXBwZW5kKHJpZ2h0SWNvbikuYXBwZW5kKGZpckxldmVsKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuXG4gICAgICAgIC8vIOaXpeacn1xuICAgICAgICAkKCcuZGF0ZScpLmVhY2goZnVuY3Rpb24oKXtcbiAgICAgICAgICAgIGlmICgkKHRoaXMpLmF0dHIoJ25hbWUnKSA9PSBwYXJhbS5ncmFuZCkge1xuICAgICAgICAgICAgICAgICQodGhpcykuYWRkQ2xhc3MoJ2N1cnJlbnQtZGF0ZScpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBmdW5jdGlvbiBnZXRQcm9kdWN0SWQoYXJyKXtcbiAgICAgICAgJC5hamF4KHtcbiAgICAgICAgICAgIHVybDogJ2FwaS92MS9wcm9kdWN0cy1saXN0LWNvbGxlY3RlZCcsXG4gICAgICAgICAgICB0eXBlOiAnUE9TVCcsXG4gICAgICAgICAgICBkYXRhOiB7XG4gICAgICAgICAgICAgICAgJ3NrdWlkcyc6IEFycmF5KGFyciksXG4gICAgICAgICAgICAgICAgJ3NvdXJjZSc6cGFyYW0uc291cmNlXG4gICAgICAgICAgICB9LFxuICAgICAgICAgICAgaGVhZGVyOiB7XG4gICAgICAgICAgICAgICAgY3NyZm1pZGRsZXdhcmV0b2tlbjogJ3t7IGNzcmZfdG9rZW4gfX0nXG4gICAgICAgICAgICB9LFxuICAgICAgICAgICAgZGF0YVR5cGU6ICdqc29uJyxcbiAgICAgICAgICAgIHN1Y2Nlc3M6IGZ1bmN0aW9uKGNvbGxlY3Qpe1xuICAgICAgICAgICAgICAgIHZhciByZXN1bHRScnJheSA9IFtdO1xuICAgICAgICAgICAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgY29sbGVjdC5yZXN1bHQubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgICAgICAgICAgdmFyIHJlc3VsdElkID0gY29sbGVjdC5yZXN1bHRbaV0ucHJvZHVjdF9pZDtcbiAgICAgICAgICAgICAgICAgICAgcmVzdWx0UnJyYXkucHVzaChyZXN1bHRJZCk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICQoJyNjb25fbGlzdCBpLmljb24nKS5lYWNoKGZ1bmN0aW9uKCl7XG4gICAgICAgICAgICAgICAgICAgIHZhciBsaXN0SWQgPSBOdW1iZXIoJCh0aGlzKS5hdHRyKCduYW1lJykpO1xuICAgICAgICAgICAgICAgICAgICBpZiAocmVzdWx0UnJyYXkuaW5kZXhPZihsaXN0SWQpICE9IC0xKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAkKHRoaXMpLmFkZENsYXNzKCdoZWFydCcpO1xuICAgICAgICAgICAgICAgICAgICAgICAgJCh0aGlzKS5wYXJlbnQoKS5jc3MoJ2JvcmRlcicsICcxcHggc29saWQgcmVkJyk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgfVxuXG4gICAgdmFyIHN0ciA9IHdpbmRvdy5sb2NhdGlvbi5ocmVmO1xuICAgICAgICBzdHIgPSBzdHIuc3Vic3RyaW5nKHN0ci5sYXN0SW5kZXhPZihcIi9cIikgKyAxKTtcbiAgICAgICAgaWYgKCQuY29va2llKHN0cikpIHtcbiAgICAgICAgICAgICQoXCJodG1sLGJvZHlcIikuYW5pbWF0ZSh7IHNjcm9sbFRvcDogJC5jb29raWUoc3RyKSB9LCA1MDApO1xuICAgICAgICB9XG5cbiAgICAkKHdpbmRvdykuc2Nyb2xsKGZ1bmN0aW9uICgpIHtcbiAgICAgICAgdmFyIHN0ciA9IHdpbmRvdy5sb2NhdGlvbi5ocmVmO1xuICAgICAgICBzdHIgPSBzdHIuc3Vic3RyaW5nKHN0ci5sYXN0SW5kZXhPZihcIi9cIikgKyAxKTtcbiAgICAgICAgdmFyIHRvcCA9ICQoZG9jdW1lbnQpLnNjcm9sbFRvcCgpO1xuICAgICAgICAkLmNvb2tpZShzdHIsIHRvcCwgeyBwYXRoOiAnLycgfSk7XG4gICAgICAgIHJldHVybiAkLmNvb2tpZShzdHIpO1xuICAgIH0pO1xuXG4gICAgcmVxdWVzdERhdGFGdW4oKTtcbiAgICBjaXR5U2VsZWN0aW9uRnVuKCk7XG4gICAgaW5kZXggPSBwYXJhbS5wYWdlO1xuICAgIHRpbWVyID0gc2V0SW50ZXJ2YWwoZnVuY3Rpb24oKXtcbiAgICAgICAgaWYgKGxvYWRlZCA9PT0gdHJ1ZSl7XG4gICAgICAgICAgICAkKCcjdG90YWxfcGFnZScpLmh0bWwoZGF0YVRvdGFsKTtcbiAgICAgICAgICAgIGN1cnJlbnRTdGF0dXNGdW4oKTtcbiAgICAgICAgICAgIGNoYW5nZVN0YXR1c0Z1bigpO1xuICAgICAgICAgICAgbG9hZGVkID0gZmFsc2U7XG4gICAgICAgICAgICBjbGVhckludGVydmFsKHRpbWVyKTtcbiAgICAgICAgICAgIC8vIOWVhuWTgeWIl+ihqOWKoOi9veWujO+8jOiOt+WPluW9k+WJjemhtemdouaJgOacieWVhuWTgeeahGlkXG4gICAgICAgICAgICBnZXRQcm9kdWN0SWQocHJvZHVjdElkKTtcbiAgICAgICAgfVxuICAgIH0sMjApO1xufSk7Il0sInNvdXJjZVJvb3QiOiIvc291cmNlLyJ9
