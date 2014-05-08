/*
 * Tiago de Souza Moraes / 08-05-2014
 * tiago@futuria.com.br
 */
$(document).ready( function() { 
    $('input[name=client_search_button]').click(function() {
        $.getJSON('/client/filter/' + $('input[name=client_search_key]').val() + '/', function(json) {
            var tableTR = '';

            /**
            * build html
            */

            jQuery.each(json,  function(){
                if(this.id) {
                    tableTR += '<tr>';
                    tableTR += '<td>' + this.name + '</td>';
                    tableTR += '<td> <a href="#form" class="add_as_member_family" id="' + this.id + '" name="' + this.name + '">Adicionar</a></td>';
                    tableTR += '<td></td>';
                    tableTR += '</tr>';
                }
            });
            
            $('table#client_family_results tbody').html(tableTR);
            
            // bind when click
            $('table#client_family_results tbody a.add_as_member_family').click(function(){
                $('form#form_family input[name=client_id]').val($(this).attr('id'));
                $('form#form_family input[name=name]').val($(this).attr('name'));
                
            });
        });  
    });
});
