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


