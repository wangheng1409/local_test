$(function(){
  $('.action').click(function(e){
    e.preventDefault();

    var that = $(this);
    var oriText = $(this).text();
    var customInputPlaceholder = $('#custom-input').attr('placeholder');
    var shouldFadeout = $(this).attr('data-tag-name') !== undefined;
    var tagType = $(this).attr('data-tag-type');
    var tagName;

    if(shouldFadeout){
      tagName = $(this).attr('data-tag-name');
    }else{
      tagName = $('#custom-input').val();
    }

    if(!$(this).hasClass('loading')){
      $(this).addClass('loading').text('Loading');
      $.post('/standards/add-tag', {'tag': tagName, 'type': tagType}, function(data){
        console.log(data);
        that.removeClass('loading').text(oriText);
        if(shouldFadeout){
          that.parent().fadeOut();
        }else{
          $('#custom-input').val('').attr('placeholder', '添加成功!');
          setTimeout(function(){
            $('#custom-input').attr('placeholder', customInputPlaceholder);
          }, 1000);
        }
      });
    }
  });

  $('.tag').mouseup(function(){
    // console.log(window.getSelection().toString());
    $('#custom-input').val(window.getSelection().toString());
  });


  $('.refresh-button').click(function(e){
    e.preventDefault();
    var itemIds = [];
    var items = $(this).siblings('ul').children();
    for(var i = 0; i < items.length; i++){
      itemIds.push($(items[i]).attr('data-id'));
    }
    console.log(itemIds.join(','));
    var that = $(this);
    $(this).addClass('loading');
    $.post('/standards/update-item-keywords', {'q': itemIds.join(',')}, function(data){
      console.log(data);
      that.removeClass('loading');
      that.parent().fadeOut();
    });
  });

  $('#search-btn').click(function(e){
    var win = window.open('https://www.baidu.com/s?wd=' + $('#custom-input').val(), '_blank');
    win.focus();
  });


});