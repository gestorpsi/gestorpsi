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
 * build paginator from JSON data
 */

function buildPaginator(app, json_paginator, json_util, selector, deactive, extra_context) { 
        if(!selector) selector = 'div#list';
        url_extra = (deactive)?'/deactive/':'';
        url_extra += (extra_context)? extra_context:'';

        /* don't work, get extra_context formated
        if(extra_context) {
            var element_count = 0;
            url_extra += "?";
            for(var i in extra_context) {
                if(element_count > 0) { url_extra += "&"; }
                url_extra += i + "=" + extra_context[i];
                element_count++;
            }
        }*/

        var page_range = '';

        jQuery.each(json_paginator,  function(){
            if(this != json_util['paginator_actual_page']) 
                page_range += '<a href="/' + app + '/page'+ this + url_extra + '">';
                page_range += this;

            if(this != json_util['paginator_actual_page']) 
                page_range += '</a>';
            page_range += ' | ';
        });

        $('ul.paginator li.page_range').html(page_range.substr(0, (page_range.length-2)));

        $('ul.paginator').attr('actual_page', json_util['paginator_actual_page']);

        $('ul.paginator li.previous a').hide();
        $('ul.paginator li.next a').hide();
        
        if(json_util['paginator_has_previous']) {
            $('ul.paginator li.previous a').attr('href','/' + app + '/page' + json_util['paginator_previous_page_number'] + url_extra);
            $('ul.paginator li.previous a').show();
        }

        if(json_util['paginator_has_next']) {
            $('ul.paginator li.next a').attr('href','/' + app + '/page' + json_util['paginator_next_page_number'] + url_extra);
            $('ul.paginator li.next a').show();
        }
        
        $('div.registers_available p.description b:first').text(json_util['paginator_actual_page']);
        $('div.registers_available p.description b:last').text(json_util['paginator_num_pages']);
        $('div.registers_available p.description span#object_length').text(json_util['object_length']);
        
}


/**
 * build itens list from JSON data
 */

function buildTableList(tableTR, selector, has_perm_read) {
    
    /**
     * flush old list
     */
    
    $('table#search_results tbody').html('');

    /**
     * display table if results or show 'no register available' dialog box
     */

    if(tableTR == '') {
        $('div.no_registers_available').show();
    } else {
        $('div.no_registers_available').hide();
    }

    /**
     * populate table
     */

    $('table#search_results tbody').html(tableTR);
    
    /**
     * remove links if dont have perms
     */

    if(has_perm_read != true) {
        $('table#search_results tbody a').each(function() {
            $(this).parent('td').text($(this).text());
            $(this).remove();
        }); 
    }   
    
    $('table.zebra tr:odd').addClass('zebra_0');
	$('table.zebra tr:even').addClass('zebra_1');

}
