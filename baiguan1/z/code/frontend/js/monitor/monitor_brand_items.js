$(function(){

var dateFormat = 'yy-mm-dd';
var start_date = $('#start_date').datepicker({
      changeMonth: true,
      dateFormat: dateFormat,
      defaultDate: getDate($(this).val()),
      maxDate: getDate($('#end_date').val())
    }).on('change', function() {
      end_date.datepicker('option','minDate', getDate($(this).val()));
    });

var end_date = $('#end_date').datepicker({
    changeMonth: true,
    dateFormat: dateFormat,
    defaultDate: getDate($(this).val()),
    minDate: getDate($('#start_date').val())
  }).on('change', function() {
    start_date.datepicker('option','maxDate', getDate($(this).val()));
  });

function getDate(val) {
  var date;
  try {
    date = $.datepicker.parseDate(dateFormat, val);
  } catch(error){
    date = null;
  }

  return date;
}


$('#refresh').click(function(){
    location.href = generateUrl({'s': $('#start_date').val(),
       'e': $('#end_date').val()});
});

function renderSparklines() {
    var height = 50;
    var width = 300;
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
                    return x_values[fields.offset] + '<br />' + fields.y;
                }
            }
        });
    });
}


renderSparklines();


});