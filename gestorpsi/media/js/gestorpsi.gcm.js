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

    // plan, hide or show pagseguro form
    $('select.prefered_plan').change( function() { 

        $('div[id*="pagseguro_cartao"]').hide(); // hide all payments forms

        // plan 
        planid = $('select[name="prefered_plan"]').val(); // get selected plan id
        value = $('input[name="plan_id' + planid + '"]' ).val(); // get price of plan

        // payment form
        payment_id = $('select.payment_type').val(); // get payment form
        tempo = $('input[name="payment_id' + payment_id + '_time"]').val();

        // mostrar ao cliente valor total e tempo do plano
        // clean
        $('input[name="valor_plano"]').val('');
        $('input[name="tempo_plano"]').val('');
        // new value
        $('input[name="valor_plano"]').val('R$ ' + tempo*value);
        $('input[name="tempo_plano"]').val(tempo + ' mes(es)');

        // cartao
        if ( $('select.payment_type').val() == '1' ) { 
            plan = $('select[name="prefered_plan"]').val(); // get selected plan id
            $('div[id="pagseguro_cartao' + plan + '"]').show(); // show selected form
        }
        
        // boleto
        if ( $('select.payment_type').val() == '2' ) { 
            $('div[id="pagseguro_boleto"]').show(); // show selected form
        }

    });

    /*
     * show and hide information about payment type
     */
    $('select.payment_type').change( function() { 

        $('div[id*="pagseguro_cartao"]').hide(); // hide all pagseguro cartao
        $('div[id="pagseguro_boleto"]').hide(); // hide all pagseguro boleto
        $('div[id*="payment_type"]').hide(); // hide all div contains payment type / text about 
        
        // plan 
        planid = $('select[name="prefered_plan"]').val(); // get selected plan id
        value = $('input[name="plan_id' + planid + '"]' ).val(); // get price of plan

        // payment form
        payment_id = $('select.payment_type').val(); // get payment form
        tempo = $('input[name="payment_id' + payment_id + '_time"]').val();

        // mostrar ao cliente valor total e tempo do plano
        // clean
        $('input[name="valor_plano"]').val('');
        $('input[name="tempo_plano"]').val('');
        // new value
        $('input[name="valor_plano"]').val('R$ ' + tempo*value);
        $('input[name="tempo_plano"]').val(tempo + ' mes(es)');

        $('div[id="payment_type' + this.value + '"]').show(); // show selected payment type

        // cartao
        if ( $('select.payment_type').val() == '1' ) { 
            plan = $('select[name="prefered_plan"]').val(); // get selected plan id
            $('div[id="pagseguro_cartao' + plan + '"]').show(); // show selected form
        }
        
        // boleto
        if ( $('select.payment_type').val() == '2' ) { 
            $('div[id="pagseguro_boleto"]').show(); // show selected form
        }

    });

}); // ready
