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
     * filter service by group or not
     */
    $('select#id_charge').change( function(){ 
        alert(this.value);

        /*$('div#ms-id_service ul').html('');*/

        $('select#id_service').html('');
        $('select#id_service').html('<option value="2ebfcd82-1cd5-4958-8811-f1cb97b49758">Fisioterapia1</option>');

        $('div.ms-selectable ul').html('');
        $('div.ms-selection ul').html('');

        $('select#id_service').multiSelect();
    });

});
