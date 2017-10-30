$.ajax({
    url:'api/v1/products-category',
    type: 'GET',
    success: function(data) {
        var every_id = [];
        for (var i = 0; i < data.length; i++) {
            var name = data[i].id;
            every_id[name] = data[i];
        }
        for (var j = 0; j < data.length; j++) {
            if (data[j].level === 0) {
                var fir_item = $('<a class="item" href="javascript:"></a>').html(data[j].name).attr('sign','std_cat').attr('name',data[j].id);
                var sec_wrapper = $('<div class="ui six column relaxed divided grid popup sec_wrapper"></div>').attr('name',data[j].id);
                var fir_list = $('<div class="ui inverted grey basic button fir_list"></div>').attr('name',data[j].id).append(fir_item).append(sec_wrapper);
                $('#category').append(fir_list);
            }else if (data[j].level === 1) {
                var sec_cur_id = data[j].parent_id;
                var sec_item = $('<a class="ui header item" href="javascript:"></a>').html(data[j].name).attr('sign','std_cat').attr('name', data[j].id).attr('p_id', data[j].parent_id);
                var sec_list = $('<div class="column sec_list"></div>').attr('name', data[j].id).attr('p_id', data[j].parent_id).append(sec_item);
                if (sec_cur_id == every_id[sec_cur_id].id) {
                    $('.sec_wrapper[name='+ sec_cur_id +']').append(sec_list);
                }
            }else if (data[j].level === 2) {
                var thi_cur_id = data[j].parent_id;
                var thi_item = $('<a class="item" href="javascript:"></a>').html(data[j].name).attr('sign','std_cat').attr('name',data[j].id).attr('p_id', data[j].parent_id);
                var thi_list = $('<div class="ui link list"></div>').attr('name', data[j].id).attr('p_id', data[j].parent_id).append(thi_item);
                if (thi_cur_id === every_id[thi_cur_id].id) {
                    $('.sec_list[name='+ thi_cur_id +']').append(thi_list);
                }
            }
        }
    }
});