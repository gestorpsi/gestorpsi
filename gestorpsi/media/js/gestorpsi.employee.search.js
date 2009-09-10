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

$(function() {
   
    /**
     * Get deactive True OR False
     */
     deactive = $('div.main_area table#search_results input[name=employee_deactive]').val();

    if (deactive == "True" ){
	    /**
	     * employee quick filter
	     */
	    
	    $('div#search_employee_header.employee_search table#letter_menu tr td a, div#search_employee_header.employee_search a#letter_back, div#search_employee_header.employee_search a#letter_fwd').click(function() {
		updateEmployee('/employee/initial/' + $(this).attr('initial') + '/page1/deactive/', 'employee/initial/'+$(this).attr('initial')+ '/deactive/');
	    });

	    /**
	    * employee quick search
	    */

	    $('div#search_employee_header.employee_search input[type=text].quick_employee_search').keyup(function() {
		($(this).val().length >= 1) ? updateEmployee('/employee/filt/' + $(this).val() + '/page1/deactive/', 'employee/filt/' + $(this).val()+ '/deactive/') : updateEmployee('/employee/page1/deactive/');
	    }); 

	    /**
	     * employee clean up
	     */
	    
	    $('div#search_employee_header.employee_search a#cleanup').click(function() {
		updateEmployee('/employee/page1/deactive/');
	    });
	    
	    /**
	     * commom quick filter events
	     */
	    
	    $('table#letter_menu tr td a, div#search_employee_header a#letter_back, div#search_employee_header a#letter_fwd').click(function() {

		    var previous = ''
		    var next = ''
		
		    $('div#search_employee_header a.arrow').show();
		    $('table#letter_menu tr td a').removeClass('active');
		    
		    $('div.registers_available > h2 > span > span').html('"' + $(this).attr('initial').toUpperCase() + '"');
		    $('div.registers_available > h2 > span').show();
		    
		    $(this).addClass('active');
		    $('div#search_employee_header div.capital_letter').text($(this).attr('initial').toUpperCase());

		    if(!$(this).hasClass('arrow')) { // arrows < A - C >
			previous = $(this).parent('td').prev().children('a').text();
			next = $(this).parent('td').next().children('a').text();
		    } else { // A,B,C,D,E etc 
			var selected = $('table#letter_menu tr td a[initial=' + $(this).attr('initial') + ']').addClass('active');
			previous = selected.parent('td').prev().children('a').text();
			next = selected.parent('td').next().children('a').text()
		    }

		    $('div#search_employee_header a#letter_back').text(previous);
		    $('div#search_employee_header a#letter_back').attr('initial', previous.toLowerCase());
		    
		    $('div#search_employee_header a#letter_fwd').text(next);
		    $('div#search_employee_header a#letter_fwd').attr('initial', next.toLowerCase());
		    
		    if(!previous)
			$('div#search_employee_header a.arrow#letter_back').hide();
		    if(!next)
			$('div#search_employee_header a.arrow#letter_fwd').hide();
			
		    $('div#search_employee_header input[type=text].quick_employee_search').val('');

	    });

	    /**
	    * commom quick search events
	    */

	    $('div#search_employee_header input[type=text].quick_employee_search').keyup(function() {
		if($(this).val().length >= 1) {
		    $('div.registers_available > h2 > span > span').html('"' + $(this).val().toUpperCase() + '"');
		    $('div.registers_available > h2 > span').show();
		} else {
		    $('h2.title_clients span').hide();
		}
	    }); 
	    
	    /**
	     * commom clean up
	     */
	    
	    $('div#search_employee_header a#cleanup').click(function() {
		$('div#search_employee_header input[type=text].quick_employee_search').val('');
		$('table#letter_menu tr td a').removeClass('active');
		$('div.registers_available > h2 span span').html('');
		$('div.registers_available > h2 span').hide();
	    });

    }else{
	    /**
	     * employee quick filter
	     */
	    
	    $('div#search_employee_header.employee_search table#letter_menu tr td a, div#search_employee_header.employee_search a#letter_back, div#search_employee_header.employee_search a#letter_fwd').click(function() {
		updateEmployee('/employee/initial/' + $(this).attr('initial') + '/page1/', 'employee/initial/'+$(this).attr('initial'));
	    });

	    
	    /**
	    * employee quick search
	    */

	    $('div#search_employee_header.employee_search input[type=text].quick_employee_search').keyup(function() {
		($(this).val().length >= 1) ? updateEmployee('/employee/filter/' + $(this).val() + '/page1/', 'employee/filter/' + $(this).val()) : updateEmployee('/employee/page1');
	    }); 

	    /**
	     * employee clean up
	     */
	    
	    $('div#search_employee_header.employee_search a#cleanup').click(function() {
		updateEmployee('/employee/page1');
	    });
	    
	    /**
	     * commom quick filter events
	     */
	    
	    $('table#letter_menu tr td a, div#search_employee_header a#letter_back, div#search_employee_header a#letter_fwd').click(function() {

		    var previous = ''
		    var next = ''
		
		    $('div#search_employee_header a.arrow').show();
		    $('table#letter_menu tr td a').removeClass('active');
		    
		    $('div.registers_available > h2 > span > span').html('"' + $(this).attr('initial').toUpperCase() + '"');
		    $('div.registers_available > h2 > span').show();
		    
		    $(this).addClass('active');
		    $('div#search_employee_header div.capital_letter').text($(this).attr('initial').toUpperCase());

		    if(!$(this).hasClass('arrow')) { // arrows < A - C >
			previous = $(this).parent('td').prev().children('a').text();
			next = $(this).parent('td').next().children('a').text();
		    } else { // A,B,C,D,E etc 
			var selected = $('table#letter_menu tr td a[initial=' + $(this).attr('initial') + ']').addClass('active');
			previous = selected.parent('td').prev().children('a').text();
			next = selected.parent('td').next().children('a').text()
		    }

		    $('div#search_employee_header a#letter_back').text(previous);
		    $('div#search_employee_header a#letter_back').attr('initial', previous.toLowerCase());
		    
		    $('div#search_employee_header a#letter_fwd').text(next);
		    $('div#search_employee_header a#letter_fwd').attr('initial', next.toLowerCase());
		    
		    if(!previous)
			$('div#search_employee_header a.arrow#letter_back').hide();
		    if(!next)
			$('div#search_employee_header a.arrow#letter_fwd').hide();
			
		    $('div#search_employee_header input[type=text].quick_employee_search').val('');

	    });

	    /**
	    * commom quick search events
	    */

	    $('div#search_employee_header input[type=text].quick_employee_search').keyup(function() {
		if($(this).val().length >= 1) {
		    $('div.registers_available > h2 > span > span').html('"' + $(this).val().toUpperCase() + '"');
		    $('div.registers_available > h2 > span').show();
		} else {
		    $('h2.title_clients span').hide();
		}
	    }); 
	    
	    /**
	     * commom clean up
	     */
	    
	    $('div#search_employee_header a#cleanup').click(function() {
		$('div#search_employee_header input[type=text].quick_employee_search').val('');
		$('table#letter_menu tr td a').removeClass('active');
		$('div.registers_available > h2 span span').html('');
		$('div.registers_available > h2 span').hide();
	    });
	}	
	
});
