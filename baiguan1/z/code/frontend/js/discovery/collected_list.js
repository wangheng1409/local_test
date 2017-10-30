$(document).ready(function(){
    var collectedTotal = null;
    var currentPage = Number($('#pagination').attr('name'));

    function requestCollected(){
        $.ajax({
            url: 'collected-product',
            type: 'GET',
            data: {'page': currentPage},
            dataType: 'json',
            success: function(collect){
                if (collect.result !== '') {
                    $('.ui.single.line.table').show();
                    for (var i = 0; i < collect.result.length; i++) {
                        var h = 'product-info?area='+ collect.result[i].product_area +'&source='+ collect.result[i].product_source +"&skuid="+collect.result[i].product_id;
                        var fir_td = $('<td><input type="checkbox"></input></td>');

                        var sec_td_a = $('<a href='+ h +'></a>');
                        var sec_td_img = $('<img src='+ collect.result[i].product_image +' class="ui mini rounded image">');

                        var sec_td_name = $('<a href='+ h +' class="content">'+ collect.result[i].product_name +'</a>');
                        var sec_td = $('<td class="sec_td left aligned"></td>');

                        var thi_td = $('<td>'+ collect.result[i].collect_time +'</td>');

                        var for_td = $('<td><a href="javascript:" class="delete" name='+ collect.result[i].product_id +'>删除收藏</a></td>');

                        var tr_wrapper = $('<tr class="center aligned"></tr>');

                        sec_td_a.append(sec_td_img);
                        sec_td.append(sec_td_a).append(sec_td_name);
                        tr_wrapper.append(fir_td).append(sec_td).append(thi_td).append(for_td);
                        $('#product_list').append(tr_wrapper);
                    }
                }else{
                    $('.remind').show();
                }
                collectedTotal = collect.total;
            }
        });
    }
    requestCollected();

    $(document).ajaxSuccess(function (event, xhr, settings) {
        if (settings.url === ("collected-product?page="+currentPage)) {
            deleteCollected();
            collectedPagination();
        }
    });

    // 删除收藏的商品
    function deleteCollected(){
        $('.delete').click(function(){
            var product_id = $(this).attr('name');
            $.ajax({
                url: 'product-collect',
                type: 'GET',
                dataType: 'json',
                data: {'skuid': product_id},
                success: function(del){
                    // del=0 删除
                    if (del.success === 0) {
                        alert('删除成功');
                        $('.delete[name='+ product_id +']').parent().parent('tr').remove();
                        if ($('.delete').length === 0) {
                            $('.remind').show();
                            $('.ui.single.line.table').hide();
                        }
                    }
                }
            });
        });
    }

    // 分页
    function collectedPagination(){
        for (var i = 1; i <= collectedTotal; i++) {
            if (i <= 6) {
                var single = $('<a href="javascript:" class="item page_item">'+ i +'</a>');
                $("#pagi_next").before(single);
            }
        }

        $('.page_item').each(function(){
            if ($(this).html() == currentPage) {
                $(this).addClass('active');
            }

            if (currentPage >= 4 && collectedTotal > 6) {
                if (currentPage >= collectedTotal - 2) {
                    for (var i = 0; i < $('.pagi').length; i++) {
                        var nowPage = collectedTotal - 5 + i;
                        $('.pagi')[i].innerHTML = nowPage;
                    }
                }else{
                    for (var j = 0; j < $('.pagi').length; j++) {
                        var nowPageOther = currentPage - 3 + j;
                        $('.pagi')[j].innerHTML = nowPageOther;
                    }
                }

            }
        });

        // 每一页
        $('.page_item').click(function() {
            var pageItem = $(this).html();
            reloadPageFun(pageItem);
        });

        // 左右翻页
        $('#pagi_prev, #pagi_next').click(function(){
            if ($(this).attr('id') == 'pagi_prev') {
                currentPage --;
            }else{
                currentPage ++;
            }


            if (currentPage <= 0) {
                currentPage = 1;
            }

            if (currentPage >= collectedTotal) {
                currentPage = collectedTotal;
            }
            reloadPageFun(currentPage);
        });
    }

    function reloadPageFun(param){
        window.location.href = 'collect?page='+ param;
    }
});