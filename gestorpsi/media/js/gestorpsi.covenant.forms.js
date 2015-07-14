/**

Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

*/

// create new combobox after load new options
function reload_combobox(){ 
    $('select#id_service').multiSelect();
}

$(document).ready(function() {

    // show and hide event numnber input
    $('select[name=charge]').change( function(){ 
        if ( this.value == '2' ){ 
            $('label[for=event_time]').show(); 
            $('input[name=event_time]').attr("required","true");
        } else { 
            $('label[for=event_time]').hide(); 
            $('input[name=event_time]').removeAttr('required'); 
        }
    });

    // jquery.maskMoney
    // http://plentz.github.io/jquery-maskmoney/
    
    // 2 decimal places and positive 
    $("#numbersOnly").maskMoney({ thousands:'', decimal:',', allowZero:true });
    // event number positive
    $("#event_time").maskMoney({ allowZero:false, thousands:'', decimal:'' });


    /*
     * filter service. Individual or all.
     */
    $('select#id_charge').change( function(){ 

        // clear
        $('select#id_service').html('');
        // remove
        $('div#ms-id_service').remove();

        // get all services. Individual and group
        if ( this.value == '1'){ 
            $.getJSON("/service/list/all/" , function(json) {
                jQuery.each(json,  function(){
                    $('select#id_service').append('<option value="' + this.id + '">' + this.name + '</option>');
                });
            });
        // get individual services
        } else { 
            $.getJSON("/service/list/indiv/" , function(json) {
                jQuery.each(json,  function(){
                    $('select#id_service').append('<option value="' + this.id + '">' + this.name + '</option>');
                });
            });
        }

        // reload_combobox must have a delay
        setTimeout(reload_combobox, 500);
    });

});
