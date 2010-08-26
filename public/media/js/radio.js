$('.showname').bind('click', function() {
    alert($(this).next('.jsondata').html());
});