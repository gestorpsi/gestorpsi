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
     deactive = $('table#search_results input[name=client_deactive]').val();

    /**
    * contact quick search
    */

    $('div#search_header.contact_search input[type=text].quick_search').keyup(function() {
        ($(this).val().length >= 1) ? updateContact('/contact/filter/' + $(this).val() + '/page1/', 'contact/filter/' + $(this).val()) : updateContact('/contact/page1');
    });
    
    /**
     * contact clean up
     */
    
    $('div#search_header.contact_search a#cleanup').click(function() {
        updateContact('/contact/page1');
    });
    

    /**
     * commom quick filter events
     */
    
    $('table#letter_menu tr td a, div#search_header a#letter_back, div#search_header a#letter_fwd').click(function() {

            var previous = ''
            var next = ''
        
            $('div#search_header a.arrow').show();
            $('table#letter_menu tr td a').removeClass('active');
            
            $('div.registers_available > h2 > span > span').html('"' + $(this).attr('initial').toUpperCase() + '"');
            $('div.registers_available > h2 > span').show();
            
            $(this).addClass('active');
            $('div#search_header div.capital_letter').text($(this).attr('initial').toUpperCase());

            if(!$(this).hasClass('arrow')) { // arrows < A - C >
                previous = $(this).parent('td').prev().children('a').text();
                next = $(this).parent('td').next().children('a').text();
            } else { // A,B,C,D,E etc 
                var selected = $('table#letter_menu tr td a[initial=' + $(this).attr('initial') + ']').addClass('active');
                previous = selected.parent('td').prev().children('a').text();
                next = selected.parent('td').next().children('a').text()
            }

            $('div#search_header a#letter_back').text(previous);
            $('div#search_header a#letter_back').attr('initial', previous.toLowerCase());
            
            $('div#search_header a#letter_fwd').text(next);
            $('div#search_header a#letter_fwd').attr('initial', next.toLowerCase());
            
            if(!previous)
                $('div#search_header a.arrow#letter_back').hide();
            if(!next)
                $('div#search_header a.arrow#letter_fwd').hide();
                
            $('div#search_header input[type=text].quick_search').val('');

    });

    /**
    * commom quick search events
    */

    $('div#search_header input[type=text].quick_search').keyup(function() {
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
    
    $('div#search_header a#cleanup').click(function() {
        $('div#search_header input[type=text].quick_search').val('');
        $('table#letter_menu tr td a').removeClass('active');
        $('div.registers_available > h2 span span').html('');
        $('div.registers_available > h2 span').hide();
    });

    if (deactive == "False"){
    /**
     * client quick filter
     */
    
    $('div#search_header.client_search table#letter_menu tr td a, div#search_header.client_search a#letter_back, div#search_header.client_search a#letter_fwd').click(function() {
        updateClient('/client/initial/' + $(this).attr('initial') + '/page1/', 'client/initial/'+$(this).attr('initial'));
    });

    
    /**
    * client quick search
    */

    $('div#search_header.client_search input[type=text].quick_search').keyup(function() {
        ($(this).val().length >= 1) ? updateClient('/client/filter/' + $(this).val() + '/page1/', 'client/filter/' + $(this).val()) : updateClient('/client/page1');
    }); 

    /**
     * client clean up
     */
    
    $('div#search_header.client_search a#cleanup').click(function() {
        updateClient('/client/page1');
    });
    
    
    /**
     * contact quick filter
     */
    
    $('div#search_header.contact_search table#letter_menu tr td a, div#search_header.contact_search a#letter_back, div#search_header.contact_search a#letter_fwd').click(function() {
        updateContact('/contact/initial/' + $(this).attr('initial') + '/page1/', 'contact/initial/'+$(this).attr('initial'));
    });

 } else {

    /**
     * client quick filter
     */
    
    $('div#search_header.client_search table#letter_menu tr td a, div#search_header.client_search a#letter_back, div#search_header.client_search a#letter_fwd').click(function() {
        updateClient('/client/initial/' + $(this).attr('initial') + '/page1/deactive/', 'client/initial/'+$(this).attr('initial')+'/deactive/');
    });

    
    /**
    * client quick search
    */

    $('div#search_header.client_search input[type=text].quick_search').keyup(function() {
        ($(this).val().length >= 1) ? updateClient('/client/filt/' + $(this).val() + '/page1/deactive/', 'client/filt/' + $(this).val()) : updateClient('/client/page1/deactive/');
    }); 

    /**
     * client clean up
     */
    
    $('div#search_header.client_search a#cleanup').click(function() {
        updateClient('/client/page1/deactive/');
    });
  }
});
