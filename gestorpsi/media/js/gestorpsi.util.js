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

$(document).ready(function()
{
	
	var personInLine = function(list)
	{
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

	var isValidDate = function (value)
	{
	    var match = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(value),
	    isDate = function (d, m, y)
	    {
	        return m > 0 && m < 13 && y > 0 && y < 32768 && d > 0 && d <= (new Date(y, m, 0)).getDate();
	    };
	    return match && isDate(match[1], match[2], match[3]);
	}
	
    var verificaNumero = function(e)
    {
        if (e.which != 8 && e.which != 0 && e.which != 44 && e.which != 46 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    }
	

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
	
	function zeroFill( number, width )
	{
	  width -= number.toString().length;
	  if ( width > 0 )
	  {
	    return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
	  }
	  return number + ""; // always return a string
	}
	
	var calcTheAge = function(dBirth)
	{	
		try
		{
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
		catch(err){;}
		return ""
	}
	
	
	var CalcAge = function()
	{
	    dBirth = document.getElementById('id_birthDate').value;
	    calcTheAge( dBirth );
	}
	
	var calcBDay = function(age)
	{
		try
		{
		    var thedate = new Date()
		    var mm2 = thedate.getMonth() + 1;
		    var dd2 = thedate.getDate();
		    var yy2 = thedate.getFullYear();
		    
		    var yearBirth = yy2 - age;
		    
		    var dtBirth = zeroFill(dd2, 2) + "/" + zeroFill(mm2, 2) + "/" + zeroFill(yearBirth, 4);
		    return dtBirth;
		}
		catch(err){;}
	    return ''
	}
	
	var calcDate = function()
	{
	    age = document.getElementById('id_years').value;
	    return calcBDay(age);
	}
	
	var displayAge = function()
	{
	    if (document.getElementById('id_birthDate').value == "") {
	        document.getElementById('id_birthDate').value = calcDate();
	    }else{
	        document.getElementById('id_years').value = CalcAge();
	    }
	}


	
    $('#id_years').keypress( verificaNumero );
    
	$('#id_birthDateSupposed').change(function()
	{
	    if( !$('#id_birthDateSupposed').is(':checked') )
	    {	
	        $('#id_years').attr('disabled', true);
	        $('#id_years').val( calcTheAge( $('#id_birthDate').val() ) );
	        $('#id_birthDate').attr('disabled', false);
	    }
	    else
	    {
	        $('#id_birthDate').removeClass('formError').attr('disabled', true);
	        $('#id_birthDate').val( calcBDay( $('#id_years').val() ) );
	        $('#id_years').attr('disabled', false);
	    }
	}).trigger('change');
    
    
	$('form#form_client').submit(function(e)
	{
		if( $('#id_birthDate').attr('disabled')+'' == 'undefined' || $('#id_birthDate').attr('disabled') == true )
			return true
		else
			if( !isValidDate($('#id_birthDate').val()) )
			{
				alert('Data inválida!');
				$('body').scrollTo( $('#id_birthDate').closest('fieldset') );
				$('#id_birthDate').addClass('formError');
				
				e.preventDefault();
				return false;
			}
			else
				return true;
	});
	
	

	var maskPhones = function()
	{
		$("[name='phoneNumber']").unbind('focusout');
		$("[name='phoneNumber']").focusout(function()
		{
		    var phone, element;
		    element = $(this);
		    element.unmask();
		    phone = element.val().replace(/\D/g, '');
		    if(phone.length > 8) {
		        element.mask("9-9999-999?9");
		    } else {
		        element.mask("9999-9999?9");
		    }
		}).trigger('focusout');
	}
	maskPhones();
	$('fieldset a.add_to_form').click(function(){ maskPhones(); });
	
	/*$(window).load(function()
	{
		$('#id_birthCountry').trigger('change');
		$('#id_birthPlaceState').trigger('change');
	});*/

});




