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

    // jquery.maskmoney
    // http://plentz.github.io/jquery-maskmoney/
    /*$("#price").maskMoney({ thousands:'', decimal:',', allowZero:true });*/
    $("#price").maskMoney();
    /*$("#off").maskMoney({ thousands:'', decimal:',', allowZero:true });*/
    /*$("#total").maskMoney({ thousands:'', decimal:',', allowZero:true });*/

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
        var id = $('select#payment_select').val();

        // hide all
        $('div[id*="payment_form"]').hide(); // hide all
        $('div#covenant').hide(); //select

        if ( id == 'new' ){ 
            $('div#covenant').show(); //select
            /*$('div#payment_form_new').show();*/
        }
        
        if ( id !=0 ){ 
            $('div#payment_form'+id).show();
        }
    });


    /*
     * show and hide covenant
     */
    $('select#covenant_select').change( function(){ 
        var idc = $('select#covenant_select').val();
        $('div[id*="payment_form_covenant"]').hide(); // hide all
        $('div#payment_form_covenant'+idc).show(); // show
    });

    // cal off
    $('input[name*="off"]').keyup( function(){ 
        var idc = $('select#covenant_select').val();
        var off = parseFloat( $('input[name=off'+idc+']').val() );
        var price = parseFloat( $('input[name=price'+idc+']').val() );

        if ( isNaN(off) == true ){ 
            var total = +price;
        } else { 
            var total = -off+price;
        }

        $('input[name=total'+idc+']').val( total );
    });

});
