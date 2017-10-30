$(function () {
    init_store_data('2','1');
    $("#page_list").change( function() {
        day=$('#day').children('[class="date-choiced"]').attr("day");
        current_page=$(this).val();
        var add_row_list=[];
        var a=$('#add_row').find("input:checked");
        for(var i=0;i< a.length;i++){
            var inp=a[i];
            add_row_list.push($(inp).attr('tag'));
        }
        get_store_data(day,current_page,add_row_list); 

    });

    $('#search').click(function (){
        var add_row_list=[];
        var a=$('#add_row').find("input:checked");
        console.log(a);
        for(var i=0;i< a.length;i++){
            var inp=a[i];
            console.log(inp);
            add_row_list.push($(inp).attr('tag'));
        }
        get_store_data('2','1',add_row_list);
    });

    $('#day').children().click(function (){
        rule=$(this).attr("day");
        $(this).addClass("date-choiced").siblings().removeClass("date-choiced");
        day=$('#day').children('[class="date-choiced"]').attr("day");
        var add_row_list=[];
        var a=$('#add_row').find("input:checked");
        console.log(a);
        for(var i=0;i< a.length;i++){
            var inp=a[i];
            console.log(inp);
            add_row_list.push($(inp).attr('tag'));
        }
        console.log(day,111);
        get_store_data(day,'1',add_row_list);

    });

    $('#open_add_items').click(function(){
        $('#add-items').removeClass("hide");
    });

    $('#close_add_items').click(function(){
        $('#add-items').addClass("hide");
    });

    $('#cancel').click(function(){
        $('#add-items').addClass("hide");
    });

    $('#add_row1').click(function(){
        $('#new_row').children(':lt('+$('#new_row:last').children().last().index(this)+'):gt(1)').remove();
        var add_row_list=[];
        var a=$('#add_row').find("input:checked");
        console.log(a);
        for(var i=0;i< a.length;i++){
            var inp=a[i];
            console.log(inp);
            add_row_list.push($(inp).attr('tag'));
            $('#new_row:last').children().last().prev().after('<th>'+$(inp).parent().text()+'</th>');
            console.log($('#new_row:last').children().last().prev());
        }
        day=$('#day').children('[class="date-choiced"]').attr("day");
        get_store_data(day,'1',add_row_list);
        console.log(add_row_list);
        $('#add-items').addClass("hide");
        });

    $('#page_decrease').click(function(){
        current_page=parseInt($('#page_list').val());
        if(current_page>1){
            current_page-=1;
            current_page=current_page.toString();
            day=$('#day').children('[class="date-choiced"]').attr("day");
            $('#page_list').children(':eq('+(current_page-1).toString()+')').attr("selected","selected").siblings().attr("selected",false);
            var add_row_list=[];
            var a=$('#add_row').find("input:checked");
            console.log(a);
            for(var i=0;i< a.length;i++){
                var inp=a[i];
                console.log(inp);
                add_row_list.push($(inp).attr('tag'));
            }
            get_store_data(day,current_page,add_row_list);  

        }

    }); 

    $('#page_add').click(function(){
        all_page=parseInt($('#all_page').text());
        current_page=parseInt($('#page_list').val());
        console.log(current_page);
        if(current_page<all_page){
            current_page+=1;
            current_page=current_page.toString();
            day=$('#day').children('[class="date-choiced"]').attr("day");
            $('#page_list').children(':eq('+(current_page-1).toString()+')').attr("selected","selected").siblings().attr("selected",false);
            var add_row_list=[];
            var a=$('#add_row').find("input:checked");
            console.log(a);
            for(var i=0;i< a.length;i++){
                var inp=a[i];
                console.log(inp);
                add_row_list.push($(inp).attr('tag'));
            }
            get_store_data(day,current_page,add_row_list);     
        }
        
    });

});

function init_store_data(day,current_page){
    $.ajax({
        url: '/analytics/chain-stores/stores/get-store-list?current_page='+current_page+'&'+'date_rule='+day,
        type: 'GET',　　
        dataType: 'json',
        success: function(data){ 
            var all_page=data.all_page_count;
            var page_list=data.page_list;
            var current_store_list=data.current_store_list;
            init_page(all_page,page_list);
            init_table_data(current_store_list,[]);
        }
    });
}

function init_table_data(current_store_list,add_row_list){
    $('#store_list').empty();
     for(var i=0;i< current_store_list.length;i++){
        var n=i+1;
        var inp=current_store_list[i];
        var name=inp.name+'('+inp['city_name']+')';
        var target=inp.sales_target;
        var sales_growth=inp.sales_growth;
        var store_id=inp.store_id;
        var sales=inp.sales;
        var over_sale_percent=parseInt(inp.completeness*100).toString()+'%';
        var balance=(target-sales);
        var gross_profit=inp.gross_profit;
        var gross_profit_rate=inp.gross_profit_rate;
        console.log(name,sales,over_sale_percent,balance);
        var obj = {};

        obj['store_id'] = store_id;
        obj['sales'] = sales;
        obj['target'] = target;
        obj['over_sale_percent'] = over_sale_percent;
        obj['balance'] = balance;
        obj['sales_growth'] = sales_growth;
        obj['gross_profit'] = gross_profit;
        obj['gross_profit_rate'] = gross_profit_rate;

        
        // var picture={% static 'images/up.png' %};
        var store_item_box = [];
                
                store_item_box.push("<tr><td>"+n+'</td><td>'+
                    '<a href="/analytics/chain-stores/stores/store-detailed-info?store_id='+store_id+' '+
                    'title="">'+name+'</a>'+
                                '</td>');
                for (var j=0;j< add_row_list.length;j++){
                        store_item_box.push('<td>'+obj[add_row_list[j]]+'</td>');
                    }

                store_item_box.push(
                            '</tr>');
            
                var store_item = store_item_box.join(' ');
                $('#store_list').append(store_item);
    }

}

function get_store_data(day,current_page,add_row_list){
    var keywords=$('#keywords').val();
    $.ajax({
        url: '/analytics/chain-stores/stores/get-store-list?current_page='+current_page+'&'+'date_rule='+day, 
        type: 'GET',
        data:{'keywords':keywords},　　
        dataType: 'json',
        success: function(data){ 
            var all_page=data.all_page_count;
            var page_list=data.page_list;
            var current_store_list=data.current_store_list;
            if(current_page=='1'){
                init_page(all_page,page_list);
            }
            init_table_data(current_store_list,add_row_list);

        }
    });
}


function init_page(all_page,page_list){
    $('#all_page').text(all_page);
    $('#page_list').empty();
    for(var i=0;i< page_list.length;i++){
        var inp=page_list[i];
        $('#page_list').append('<option value="'+(i+1).toString()+'">'+inp+'</option>');
    }
    $('#page_list').first().attr("selected","selected");
}
