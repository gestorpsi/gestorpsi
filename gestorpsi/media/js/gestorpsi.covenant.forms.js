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

    // jquery.numeric
    // 2 decimal places and positive 
    $("#numbersOnly").numeric({ decimal : "," , negative: false , decimalPlaces: 2 });
    // event number positive
    $("#event_time").numeric({ negative: false });

});
