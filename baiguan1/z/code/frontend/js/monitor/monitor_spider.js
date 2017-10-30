$(function(){

function renderSparklines() {
    var height = 50;
    var width = 150;
    var x_values = $('#spark-x-values').attr('values').split(',');
    $('.sparklines').each(function() {
        $(this).sparkline('html', {
            type:'line',
            height:height,
            width:width,
            tooltipFormatter: function(sparkline, options, fields) {
                if (typeof fields.y === 'undefined') {
                    return x_values[fields.offset] + '<br />' + fields.value;
                } else {
                    return x_values[fields.offset] + '&nbsp;&nbsp;&nbsp;<br />' + fields.y + 
                           '&nbsp;&nbsp;&nbsp;<br /><br / >';
                /*    return x_values[fields.offset] + '<br />' + fields.y;
                */
                }
            }
        });
    });
}

renderSparklines();

});
