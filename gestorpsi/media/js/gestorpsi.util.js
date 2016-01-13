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
 * array to string util function
 */

function personInLine(list) {
    
    var str = ''
    
    //append person list
    if(list) {
    jQuery.each(list,  function(){
        str = str + this.name + ", " ;
    });
    str = str.substr(0, (str.length-2))
    }
    return str
    
}


$(document).ready(function() {
    $('a.load_html').live('click', function() {
        var element = $(this).attr('element');
        $(element).load($(this).attr('href'));
        return false;
    });
    
    
    /**
     * generic metho to load href into DOM element
     */
    $('a.load').live('click', function() {
        $($(this).attr('element')).load($(this).attr('href'));
        $($(this).attr('element')).show();
        //$.scrollTo(0,0, {duration:300});
        return false;
    });
    
    /**
     * cancel_button in dialog box
     */
    
    $('#dialog #cancel_button').live('click', function() {
        //$.scrollTo(0,0, {duration:300});
        return false;
    });
    
    /**
     * jquery color picker
     */
     
     //$('#colorpickerHolder').ColorPicker({flat: true});

    $('.colorpicker_open').ColorPicker({
        onSubmit: function(hsb, hex, rgb, el) {
            $(el).val(hex);
            $(el).ColorPickerHide();
            $('div.colorpicker_preview').css('background-color','#'+hex);
        },
        onBeforeShow: function () {
            $(this).ColorPickerSetColor(this.value);
        }
    })

    .bind('keyup', function(){
        $(this).ColorPickerSetColor(this.value);
        
    });

    // report event - show and hide list of clients
    $('a.showdialog').live('click', function(){ 
        $('div.client_dialog').hide();
        $('div.client_dialog[id=' + this.name + ']').show();
    });

    $('input.confirmation_select').click( function(){ 

       if (this.value == '999'){ 

           if ( this.checked ) { 
               $('input#id_confirmation_status_1').attr("checked","checked");
               $('input#id_confirmation_status_1').attr("disabled",true);
               $('input#id_confirmation_status_2').removeAttr("checked");
               $('input#id_confirmation_status_2').attr("disabled",true);
               $('input#id_confirmation_status_3').attr("checked","checked");
               $('input#id_confirmation_status_3').attr("disabled",true);
               $('input#id_confirmation_status_4').attr("checked","checked");
               $('input#id_confirmation_status_4').attr("disabled",true);
               $('input#id_confirmation_status_5').attr("checked","checked");
               $('input#id_confirmation_status_5').attr("disabled",true);
               $('input#id_confirmation_status_6').attr("checked","checked");
               $('input#id_confirmation_status_6').attr("disabled",true);
               $('input#id_confirmation_status_7').attr("checked","checked");
               $('input#id_confirmation_status_7').attr("disabled",true);
               $('input#id_confirmation_status_8').attr("checked","checked");
               $('input#id_confirmation_status_8').attr("disabled",true);
           } else { 
               $('input#id_confirmation_status_1').removeAttr("checked");
               $('input#id_confirmation_status_1').attr("disabled",false);
               $('input#id_confirmation_status_2').attr("disabled",false);
               $('input#id_confirmation_status_3').removeAttr("checked");
               $('input#id_confirmation_status_3').attr("disabled",false);
               $('input#id_confirmation_status_4').removeAttr("checked");
               $('input#id_confirmation_status_4').attr("disabled",false);
               $('input#id_confirmation_status_5').removeAttr("checked");
               $('input#id_confirmation_status_5').attr("disabled",false);
               $('input#id_confirmation_status_6').removeAttr("checked");
               $('input#id_confirmation_status_6').attr("disabled",false);
               $('input#id_confirmation_status_7').removeAttr("checked");
               $('input#id_confirmation_status_7').attr("disabled",false);
               $('input#id_confirmation_status_8').removeAttr("checked");
               $('input#id_confirmation_status_8').attr("disabled",false);
           }
       }

    });

});


/**
 * calula idade
 */

function dateOrAge() {
    if (document.getElementById('aprox').checked==false) {
        document.getElementById('Years').disabled=true;
        document.getElementById('Years').value="";
        document.getElementById('dateBirth').disabled=false;
    }else{
        document.getElementById('dateBirth').disabled=true;
        document.getElementById('dateBirth').value="";
        document.getElementById('Years').disabled=false;
    }
}
function CalcAge() {

    dBirth = document.getElementById('dateBirth').value;
    x = dBirth.split("/");
    var mm = x[1];
    var dd = x[0];
    var yy = x[2];
    
    var thedate = new Date()
    var mm2 = thedate.getMonth() + 1;
    var dd2 = thedate.getDate();
    var yy2 = thedate.getFullYear();
    
    var yourage = yy2 - yy
        if (mm2 < mm) {
        yourage = yourage - 1;
        }
        if (mm2 == mm) {
            if (dd2 < dd) {
            yourage = yourage - 1;
            }
        }
    if(yourage > 0)
        return yourage;
    else
        return ""
}
function calcDate() {
    age = document.getElementById('Years').value;
    
    var thedate = new Date()
    var mm2 = thedate.getMonth() + 1;
    var dd2 = thedate.getDate();
    var yy2 = thedate.getFullYear();
    
    var yearBirth = yy2 - age;
    
    var dtBirth = dd2 + "/" + mm2 + "/" + yearBirth
    return dtBirth;

}

function displayAge() {
    if (document.getElementById('dateBirth').value == "") {
        document.getElementById('dateBirth').value = calcDate();
    }else{
        document.getElementById('Years').value = CalcAge();
    }
}

