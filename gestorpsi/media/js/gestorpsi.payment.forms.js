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
    $('input[id*="off"]').maskMoney({ thousands:'', decimal:',', allowZero:true });

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
     * When change input OFF update total
     * 
     * <input name="payment_form-59-off" placeholder="1.234,56" required="required" type="text" class="big" value="20,50" id="id_payment_form-59-off" />
     * Any input contains the word "off" in name. Pattern: *-ID-off; str.split('-')[1] = ID
     *
     */
    $('input[name*="off"]').keyup( function(){ 

        // get id
        idc = this.name.split("-")[1];

        // get values
        var off = parseFloat( $('input[name=payment_form-'+idc+'-off]').val().replace(",", ".") );
        var price = parseFloat( $('input[name=payment_form-'+idc+'-price]').val().replace(",",".") );

        // sum values
        if ( isNaN(off) == true ){ 
            var total = parseFloat(+price);
        } else { 
            var total = parseFloat(-off+price);
        }

        // convert to currency
        tt = total.toFixed(2).replace(".",",");

        $('input[name=payment_form-'+idc+'-total]').val(tt);
    });

});
