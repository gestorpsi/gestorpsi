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

    /*
     * show and hide date 
     */
    $(function() {
        $('select#id_date_started_0_month, select#id_date_started_0_day, select#id_date_started_0_year, select#id_date_started_1_second').hide();
        $('select#id_date_finished_0_month, select#id_date_finished_0_day, select#id_date_finished_0_year, select#id_date_finished_1_second').hide();
        $('form input[name=presence]').click(function(){
            if($(this).val()>2) {
                $('div.date_fields').hide();
            } else {
                $('div.date_fields').show();
            }
        });
    });


    /*
     * show and hide covenat when change select to new payment
     */
    $('select#payment_select').change( function(){ 
        if ( $('select#payment_select').val() == 'new' ){ 
            $('div#covenant').show();
        } else { 
            $('div#covenant').hide();
        }
    });

});
