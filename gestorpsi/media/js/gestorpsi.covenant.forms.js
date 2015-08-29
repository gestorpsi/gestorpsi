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

// return msg
function charge_msg(){ 

    var id = $('select#id_charge').val();
    var msg = '';

    if ( id == '1' ){ 
        msg = 'Para cada evento na agenda, uma nova fatura é criada.';
    }

    if ( id == '2' ){ 
        msg = 'Para cada pacote de eventos, uma nova fatura é criada a partir do primeiro evento do pacote.';
    }

    if ( id == '10' ){ 
        msg = 'Uma fatura é criada todo domingo, independente do número de eventos agendados.';
    }

    if ( id == '11' ){ 
        msg = 'Uma fatura é criada todo dia 01 e 15 do mês, independente do número de eventos agendados.';
    }

    if ( id == '12' ){ 
        msg = 'Uma fatura é criada todo dia 01 do mês, independente do número de eventos.'; 
    }

    $("label[for='charge_text'] p").html(msg);
}


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
        setTimeout(reload_combobox, 900);
    });


    // change text about charge
    // mount html form
    charge_msg();
    // change
    $('select#id_charge').change( function(){ 
        charge_msg();
    });

});
