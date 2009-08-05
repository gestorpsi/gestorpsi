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
    * client initial list links
    */
    
    $('table#letter_menu.client tr td a, div#search_header a#letter_back, div#search_header a#letter_fwd').click(function() {

            var previous = ''
            var next = ''
        
            $('div#search_header a.arrow').show();
            $('table#letter_menu tr td a').removeClass('active');
            
            $('h2.title_clients span span').html('"' + $(this).attr('initial').toUpperCase() + '"');
            $('h2.title_clients span').show();
            
            updateClient('/client/initial/' + $(this).attr('initial') + '/page1/', 'client/initial/'+$(this).attr('initial'));
            $(this).addClass('active');
            $('div#search_header div.capital_letter').text($(this).attr('initial').toUpperCase());

            if(!$(this).hasClass('arrow')) { // arrows < A - C >
                previous = $(this).parent('td').prev().children('a').text();
                next = $(this).parent('td').next().children('a').text();
            } else { // A,B,C,D,E etc 
                var selected = $('table#letter_menu.client tr td a[initial=' + $(this).attr('initial') + ']').addClass('active');
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

    });
    
    /**
     * client quick search input text
     */
     
     
     $('div#search_header input[type=text].quick_search').keyup(function() {
         if($(this).val().length >= 1) {
            updateClient('/client/filter/' + $(this).val() + '/page1/', 'client/filter/' + $(this).val());
            $('h2.title_clients span span').html('"' + $(this).val().toUpperCase() + '"');
            $('h2.title_clients span').show();
        } else {
            $('h2.title_clients span').hide();
            updateClient('/client/page1');
        }
        }); 
});
