/*

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


/*

// hide all these fields or divs
function hideAll(){ 
    $('div[id*="pagseguro_cartao"]').hide(); // hide all pagseguro cartao
    $('div[id="pagseguro_boleto"]').hide(); // hide all pagseguro boleto
}

// mostrar ao cliente valor total e tempo do plano
function updateValue(tempo, value){ 
    // clean
    $('input[name="valor_plano"]').val('');
    $('input[name="tempo_plano"]').val('');
    // new value
    $('input[name="valor_plano"]').val('R$ ' +  parseFloat(tempo*value).toFixed(2) );
    $('input[name="tempo_plano"]').val(tempo + ' mes(es)');
}


// show cartao or boleto
function showCartaoOrBoleto(){ 
    // cartao
    if ( $('select.payment_type').val() == '1' ) { 
        plan = $('select[name="prefered_plan"]').val(); // get selected plan id
        $('div[id="pagseguro_cartao' + plan + '"]').show(); // show selected form
    }
    // boleto
    if ( $('select.payment_type').val() == '2' ) { 
        $('div[id="pagseguro_boleto"]').show(); // show selected form
    }
}
*/


$(document).ready(function() {

    $('select.payment_type').change( function() { 
        $('div[id*="payment_type"]').hide(); // hide all div contains payment type / text about 
        $('div[id="payment_type' + this.value + '"]').show(); // show selected payment type
    });
    
    /*
     * update fields when mount html
    
    payment_id = $('select.payment_type').val(); // get payment form
    plan_id = $('select[name="prefered_plan"]').val(); // get selected plan id
    tempo = $('input[name="payment_id' + payment_id + '_time"]').val();
    value = $('input[name="plan_id' + plan_id + '"]' ).val(); // get price of plan

    // cartao
    if ( payment_id == '1' ) { 
        $('div[id="pagseguro_cartao' + plan_id + '"]').show(); // show selected form
    }
    // boleto
    if ( payment_id == '2' ) { 
        $('div[id="pagseguro_boleto"]').show(); // show selected form
        // update boleto data
        label = $('input[name="plan_label' + plan_id + '"]' ).val(); // get price of plan
        $('input[name="itemDescription1"]').val(label);
        $('input[name="itemAmount1"]').val( parseFloat(tempo*value).toFixed(2) );
    }

    
    // plan, hide or show pagseguro form
    $('select.prefered_plan').change( function() { 

        // hide all
        hideAll();

        // plan 
        planid = $('select[name="prefered_plan"]').val(); // get selected plan id
        value = $('input[name="plan_id' + planid + '"]' ).val(); // get price of plan

        // payment form
        payment_id = $('select.payment_type').val(); // get payment form
        tempo = $('input[name="payment_id' + payment_id + '_time"]').val();

        // update boleto data
        if ( $('select.payment_type').val() == '2' ) { 
            label = $('input[name="plan_label' + planid + '"]' ).val(); // get price of plan
            $('input[name="itemDescription1"]').val(label);
            $('input[name="itemAmount1"]').val( parseFloat(tempo*value).toFixed(2) );
        }

        // mostrar ao cliente valor total e tempo do plano
        updateValue(tempo, value);

        showCartaoOrBoleto();
    });



    // show and hide information about payment type
    $('select.payment_type').change( function() { 

        hideAll();
        $('div[id*="payment_type"]').hide(); // hide all div contains payment type / text about 
        
        // plan 
        planid = $('select[name="prefered_plan"]').val(); // get selected plan id
        value = $('input[name="plan_id' + planid + '"]' ).val(); // get price of plan

        // payment form
        payment_id = $('select.payment_type').val(); // get payment form
        tempo = $('input[name="payment_id' + payment_id + '_time"]').val();

        // mostrar ao cliente valor total e tempo do plano
        updateValue(tempo, value);

        $('div[id="payment_type' + this.value + '"]').show(); // show selected payment type
        
        showCartaoOrBoleto();
        
        // update boleto data
        if ( $('select.payment_type').val() == '2' ) { 
            label = $('input[name="plan_label' + planid + '"]' ).val(); // get price of plan
            $('input[name="itemDescription1"]').val(label);
            $('input[name="itemAmount1"]').val( parseFloat(tempo*value).toFixed(2) );
        }
    });
    */

}); // ready
