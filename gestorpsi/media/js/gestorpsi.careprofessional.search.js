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
     deactive = $('table#search_results input[name=careprofessional_deactive]').val();
    
    if (deactive == "True" ){
	    /**
	     * careprofessional quick filter
	     */
	    
	    $('div#search_careprofessional_header.careprofessional_search table#letter_menu tr td a, div#search_careprofessional_header.careprofessional_search a#letter_back, div#search_careprofessional_header.careprofessional_search a#letter_fwd').click(function() {
		updateProfessional('/careprofessional/initial/' + $(this).attr('initial') + '/page1/deactive/', 'careprofessional/initial/'+$(this).attr('initial')+ '/deactive/');
	    });

	    /**
	    * careprofessional quick search
	    */

	    $('div#search_careprofessional_header.careprofessional_search input[type=text].quick_careprofessional_search').keyup(function() {
		($(this).val().length >= 1) ? updateProfessional('/careprofessional/filt/' + $(this).val() + '/page1/deactive/', 'careprofessional/filt/' + $(this).val()+ '/deactive/') : updateProfessional('/careprofessional/page1/deactive/');
	    }); 

	    /**
	     * careprofessional clean up
	     */
	    
	    $('div#search_careprofessional_header.careprofessional_search a#cleanup').click(function() {
		updateProfessional('/careprofessional/page1/deactive/');
	    });
	    
	    /**
	     * commom quick filter events
	     */
	    
	    $('table#letter_menu tr td a, div#search_careprofessional_header a#letter_back, div#search_careprofessional_header a#letter_fwd').click(function() {

		    var previous = ''
		    var next = ''
		
		    $('div#search_careprofessional_header a.arrow').show();
		    $('table#letter_menu tr td a').removeClass('active');
		    
		    $('div.registers_available > h2 > span > span').html('"' + $(this).attr('initial').toUpperCase() + '"');
		    $('div.registers_available > h2 > span').show();
		    
		    $(this).addClass('active');
		    $('div#search_careprofessional_header div.capital_letter').text($(this).attr('initial').toUpperCase());

		    if(!$(this).hasClass('arrow')) { // arrows < A - C >
			previous = $(this).parent('td').prev().children('a').text();
			next = $(this).parent('td').next().children('a').text();
		    } else { // A,B,C,D,E etc 
			var selected = $('table#letter_menu tr td a[initial=' + $(this).attr('initial') + ']').addClass('active');
			previous = selected.parent('td').prev().children('a').text();
			next = selected.parent('td').next().children('a').text()
		    }

		    $('div#search_careprofessional_header a#letter_back').text(previous);
		    $('div#search_careprofessional_header a#letter_back').attr('initial', previous.toLowerCase());
		    
		    $('div#search_careprofessional_header a#letter_fwd').text(next);
		    $('div#search_careprofessional_header a#letter_fwd').attr('initial', next.toLowerCase());
		    
		    if(!previous)
			$('div#search_careprofessional_header a.arrow#letter_back').hide();
		    if(!next)
			$('div#search_careprofessional_header a.arrow#letter_fwd').hide();
			
		    $('div#search_careprofessional_header input[type=text].quick_careprofessional_search').val('');

	    });

	    /**
	    * commom quick search events
	    */

	    $('div#search_careprofessional_header input[type=text].quick_careprofessional_search').keyup(function() {
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
	    
	    $('div#search_careprofessional_header a#cleanup').click(function() {
		$('div#search_careprofessional_header input[type=text].quick_careprofessional_search').val('');
		$('table#letter_menu tr td a').removeClass('active');
		$('div.registers_available > h2 span span').html('');
		$('div.registers_available > h2 span').hide();
	    });

    }else{
	    /**
	     * careprofessional quick filter
	     */
	    
	    $('div#search_careprofessional_header.careprofessional_search table#letter_menu tr td a, div#search_careprofessional_header.careprofessional_search a#letter_back, div#search_careprofessional_header.careprofessional_search a#letter_fwd').click(function() {
		updateProfessional('/careprofessional/initial/' + $(this).attr('initial') + '/page1/', 'careprofessional/initial/'+$(this).attr('initial'));
	    });

	    
	    /**
	    * careprofessional quick search
	    */

	    $('div#search_careprofessional_header.careprofessional_search input[type=text].quick_careprofessional_search').keyup(function() {
		($(this).val().length >= 1) ? updateProfessional('/careprofessional/filter/' + $(this).val() + '/page1/', 'careprofessional/filter/' + $(this).val()) : updateProfessional('/careprofessional/page1');
	    }); 

	    /**
	     * careprofessional clean up
	     */
	    
	    $('div#search_careprofessional_header.careprofessional_search a#cleanup').click(function() {
		updateProfessional('/careprofessional/page1');
	    });
	    
	    /**
	     * commom quick filter events
	     */
	    
	    $('table#letter_menu tr td a, div#search_careprofessional_header a#letter_back, div#search_careprofessional_header a#letter_fwd').click(function() {

		    var previous = ''
		    var next = ''
		
		    $('div#search_careprofessional_header a.arrow').show();
		    $('table#letter_menu tr td a').removeClass('active');
		    
		    $('div.registers_available > h2 > span > span').html('"' + $(this).attr('initial').toUpperCase() + '"');
		    $('div.registers_available > h2 > span').show();
		    
		    $(this).addClass('active');
		    $('div#search_careprofessional_header div.capital_letter').text($(this).attr('initial').toUpperCase());

		    if(!$(this).hasClass('arrow')) { // arrows < A - C >
			previous = $(this).parent('td').prev().children('a').text();
			next = $(this).parent('td').next().children('a').text();
		    } else { // A,B,C,D,E etc 
			var selected = $('table#letter_menu tr td a[initial=' + $(this).attr('initial') + ']').addClass('active');
			previous = selected.parent('td').prev().children('a').text();
			next = selected.parent('td').next().children('a').text()
		    }

		    $('div#search_careprofessional_header a#letter_back').text(previous);
		    $('div#search_careprofessional_header a#letter_back').attr('initial', previous.toLowerCase());
		    
		    $('div#search_careprofessional_header a#letter_fwd').text(next);
		    $('div#search_careprofessional_header a#letter_fwd').attr('initial', next.toLowerCase());
		    
		    if(!previous)
			$('div#search_careprofessional_header a.arrow#letter_back').hide();
		    if(!next)
			$('div#search_careprofessional_header a.arrow#letter_fwd').hide();
			
		    $('div#search_careprofessional_header input[type=text].quick_careprofessional_search').val('');

	    });

	    /**
	    * commom quick search events
	    */

	    $('div#search_careprofessional_header input[type=text].quick_careprofessional_search').keyup(function() {
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
	    
	    $('div#search_careprofessional_header a#cleanup').click(function() {
		$('div#search_careprofessional_header input[type=text].quick_careprofessional_search').val('');
		$('table#letter_menu tr td a').removeClass('active');
		$('div.registers_available > h2 span span').html('');
		$('div.registers_available > h2 span').hide();
	    });
	}	
	
});
