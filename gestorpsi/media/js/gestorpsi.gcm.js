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
     * show and hide information about payment type
     */
    $('select.payment_type').change( function() { 
        $('div[id*="pagseguro_form"]').hide(); // hide all pagseguro forms
        $('div[id*="payment_type"]').hide(); // hide all div contains payment type
        $('div[id="payment_type' + this.value + '"]').show(); // show selected payment type

        // if cartao, show pagseguro forms
        if ( $('select.payment_type').val() == '1' ) { 
            plan = $('select[name="prefered_plan"]').val(); // get selected plan id
            $('div[id="pagseguro_form' + plan + '"]').show(); // show selected form
        }
    });

    // plan, hide or show pagseguro form
    $('select.prefered_plan').change( function() { 

        $('div[id*="pagseguro_form"]').hide(); // hide all forms

        // just for cartao credito, pagseguro
        if ( $('select.payment_type').val() == '1' ){
            // show pagseguro form 
            plan = $('select[name="prefered_plan"]').val(); // get selected plan id
            $('div[id="pagseguro_form' + plan + '"]').show(); // show selected form
        }
    });

}); // ready
