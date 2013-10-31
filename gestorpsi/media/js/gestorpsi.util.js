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
        $.scrollTo(0,0, {duration:300});
        return false;
    });
    
    /**
     * cancel_button in dialog box
     */
    
    $('#dialog #cancel_button').live('click', function() {
        $.scrollTo(0,0, {duration:300});
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



});


/**
 * calcula idade
 */

function dateOrAge() {
    if (document.getElementById('id_birthDateSupposed').checked==false) {
        document.getElementById('id_years').disabled=true;
        document.getElementById('id_years').value="";
        document.getElementById('id_birthDate').disabled=false;
    }else{
        document.getElementById('id_birthDate').disabled=true;
        document.getElementById('id_birthDate').value="";
        document.getElementById('id_years').disabled=false;
    }
}
function CalcAge() {

    dBirth = document.getElementById('id_birthDate').value;
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
    age = document.getElementById('id_years').value;
    
    var thedate = new Date()
    var mm2 = thedate.getMonth() + 1;
    var dd2 = thedate.getDate();
    var yy2 = thedate.getFullYear();
    
    var yearBirth = yy2 - age;
    
    var dtBirth = dd2 + "/" + mm2 + "/" + yearBirth
    return dtBirth;

}

function displayAge() {
    if (document.getElementById('id_birthDate').value == "") {
        document.getElementById('id_birthDate').value = calcDate();
    }else{
        document.getElementById('id_years').value = CalcAge();
    }
}

