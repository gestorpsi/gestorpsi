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

/** 
* client referral list
*/

function updateReferral(url) {
    $.getJSON(url, function(json) {
        // flush list
        $('div#client_referral_list div.client_referral_list table tbody').html('');
        var tableTR = '';

        jQuery.each(json,  function(){
            var str_professional = ''; 
            var str_professional_inline = ''; 
            var str_service = '';

            str_professional_inline = personInLine(this.professional);

            /**
            * populate events view
            */

            tableTR = tableTR + '<tr><td class="title">' + this.service + '<br>' + str_professional_inline + '</td></tr>';
        });

        if(tableTR == '') {
            tableTR = '<div id="msg_area" class="alert">Este cliente ainda não foi encaminhado.</div>';
        }
        $('div.client_referral_list table tbody').html(tableTR);
        
        $('table.zebra tr:odd').addClass('zebra_0');
        $('table.zebra tr:even').addClass('zebra_1');

    });  

    return false;
}

/**
 * referral:
 * bind referral 
 */

function bindReferral() {
    $('div.client_referral_list').unbind().ready(function() {
        if($('div#edit_form input[name=object_id]').val()) {
            updateReferral('/referral/client/' + $('div#edit_form input[name=object_id]').val() + '/');
        }
    });
    $('form input[name=referral_type]').unbind().click(function() {
        if($(this).val() == 'subscription') {
            $('.referral_type_referral').hide();
        }
        if($(this).val() == 'referral') {
            $('.referral_type_referral').show();
        }
        
    });
}


