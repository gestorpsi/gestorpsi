var line = '';

$(function() {

    $("form input:text[mask]").each(function(){
      $(this).mask($(this).attr('mask'));
    });
    
    $('label.state select.city_search').unbind().change(function() {

        $.get('/address/search/cities/state/' + $(this).val() + '/', function( data ) {
            $('select[name=city]').html(data); // rebuild city combo 
        });

     });
});
