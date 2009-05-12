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


function bindList() {
    
    /**
     *
     * Message Area (#msg_area)
     *
     * hide msg area and dialog in ever click
     * 
     */
    
    $('table.newtab tr td a, a.ajax, a.fast_content').unbind().click(function() {
        $('#msg_area').removeClass();
        $('#msg_area').hide();
        $('.sidebar').css('padding-top','165px');
    });
    
    
    /**
     * load content inside in a div
     * ex: <a href="/schedule/" div="client_schedule">
     * if div attribute is not defined, insert into div#edit_form by default
     */

	$("table.newtab tr td a, a.ajax").click(function(){
	    
		var link = $(this);
		var div = '';
		if(!link.attr('div')) {
		    div = '#edit_form';
        } else {
            div = link.attr('div');
        }
		$('#core .fast_menu_content').hide();
		$('ul.opened_tabs').hide();
		$("#core div" + div).load(link.attr('href'));
		$.ajax({
			complete: function(){
				$('ul.opened_tabs').show();
				$("#core div" + div).show();
			}
		});

		$('#sub_menu ul li a').removeClass('active'); // unselect other tabs
		$("ul.opened_tabs").show(); // display tab
		$("ul.opened_tabs li div a:first").text(link.attr('title')); // set newtab title
		
		$("ul.opened_tabs li div a:first").unbind().click(function() {
            $('#core .fast_menu_content').hide();
			$('#core div' + div).show();
            $('#sub_menu ul li a').removeClass('active');
            if(link.attr('hide')) {
                $(link.attr('hide')).hide();    
            }
		});

        if(link.attr('fast_content')) {
		    $('div.fast_content').hide();
		    $('div.fast_content#' + link.attr('fast_content')).show();
        } 
        $('#msg_area').removeClass();
        $('#msg_area').hide();
        $('.sidebar').css('padding-top','165px');
        
		return false;
	});


/**
 * 
 *  rows table switch classes
 * 
 * _description:
 * 
 *  change classes rows in a table
 * 
 * 	tables must to have 'zebra' class
 *
 *	eg.: 
 * 		<table class="zebra">
 * 			<tr><td>Hello Baby!</td></tr>
 * 			<tr><td>You know what i like!</td></tr>
 * 		</table>
 * 
 */

	$('table.zebra tr:odd').addClass('zebra_0');
	$('table.zebra tr:even').addClass('zebra_1');
	
	// draw top-border for multirows fieldsets (eg.: address fieldset)
	$('fieldset.set_multirow').each(function() {
		$(this).children('div').removeClass('multirow');
		$(this).children('div').not(':first').addClass('multirow');
	});
	
	
	/**
	* 
	* ajaxlink
	* 
	* _description:
	* 
	* load content inside the div "core"
	* 
	* to exclude this function, in your personalized links, define 'notajax' as class in your <a> tag.
	*   
	* eg.:
	* 	<a class="notajax" href="http://disneyland.disney.go.com/">I'm an ajaxless link!</a>
	* 
	*/
	
	$("#core :not(table.zebra tr td) a:not(.notajax)").click(function(){
		var link = $(this);
		$('#edit_form div.admission_form').hide();
		$("#core").load(link.attr('href'));
		$.ajax({
			complete: function(){
				// if attribute exists, display div
				if(link.attr('display')) {
					$('#'+link.attr('display')).show();
					// if exists, change class in submenu to active
					if(link.attr('sub_menu')) {
						$('#sub_menu ul li a').removeClass('active');
						// select option in submenu
						$('div#sub_menu ul#'+link.attr('sub_menu')+' li a[display="'+link.attr('display')+'"]').addClass('active');
					}
					
				}
			}
			});
		return false;
	});



	/**
	 * client (customers)
	 * 
	 * _description:
	 * 
	 * show menu options
	 */
	
	$("#main_area span#client_add_infotypes").each(function(){
		var link = $(this);
		link.click(function() {
			 $('#main_area ul#form_options').toggle();
		 });
	});
	
	

    /**
     *
     * hide opened extra tabs when close (or Cancel Button) is clicked
     * !! only for editing registers
     *
     */
    
    $("ul.opened_tabs li div a.close, .edit_form input#cancel_button").click(function() {
        $("ul.opened_tabs").hide();
        $('div.fast_menu_content').hide();
        $('div#sub_menu li a.fastmenu.first').addClass('active');
        $('div.fast_menu_content:first').show();
        $('div#msg_area').hide();
    });
	

	

	$("table.devices td.item").unbind().click(function(){
		var class_name_to_display = $(this).attr('display');
		$('.' + class_name_to_display).toggle();
	});
	
	
	/**
	 * tabs:
	 * only switch opened tabs, without request
	 */
    
	$('#core a.fastmenu, #core p.description a').click(function() {
		
		// hide all opened content        
		$('.fast_menu_content').hide();
		
		// display choiced item and set it to already loaded
		if(!$(this).attr('display'))
			display = 'list';
		else
			display = $(this).attr('display');

		$('#' + display).show();
	
		link = $(this);
		if(link.attr('sub_menu')) {
			$('#sub_menu ul li a').removeClass('active');
			// select option in submenu
			$('div#sub_menu ul#' + link.attr('sub_menu')+' li a[display="'+link.attr('display')+'"]').addClass('active');
		}
	
	    if(link.attr('hide')) {
	        $(link.attr('hide')).hide();  
         }
		return false;
        });

    /**
     * switch already loaded forms
     */
    
	$('a.fast_content').click(function() {
		// hide all opened content        
		$('div.fast_content').hide();
		// display choiced item
		$('div.fast_content#'+$(this).attr('display')).show();
		return false;
        });

    $('a.notajax').click(function() {
        return false;
    });

}

/**
 * build paginator from JSON data
 */

function buildPaginator(app, json_paginator, json_util, selector) { 
    
        if(!selector)
            selector = 'div#list';

        var page_range = '';

        jQuery.each(json_paginator,  function(){
            if(this != json_util['paginator_actual_page']) 
                page_range += '<a href="/' + app + '/page'+ this +'">';
            page_range += this;
            if(this != json_util['paginator_actual_page']) 
                page_range += '</a>';
            page_range += ' | ';
        });

        $(selector + ' ul.paginator li.page_range').html(page_range.substr(0, (page_range.length-2)));

        $(selector + ' ul.paginator').attr('actual_page', json_util['paginator_actual_page']);

        $(selector + ' ul.paginator li.previous a').hide();
        $(selector + ' ul.paginator li.next a').hide();
        
        if(json_util['paginator_has_previous']) {
            $(selector + ' ul.paginator li.previous a').attr('href','/' + app + '/page' + json_util['paginator_previous_page_number']);
            $(selector + ' ul.paginator li.previous a').show();
        }

        if(json_util['paginator_has_next']) {
            $(selector + ' ul.paginator li.next a').attr('href','/' + app + '/page' + json_util['paginator_next_page_number']);
            $(selector + ' ul.paginator li.next a').show();
        }
        
        $(selector + ' div.registers_available p.description b:first').text(json_util['paginator_actual_page']);
        $(selector + ' div.registers_available p.description b:last').text(json_util['paginator_num_pages']);
        $(selector + ' div.registers_available p.description span#object_length').text(json_util['object_length']);
        
}


/**
 * build itens list from JSON data
 */

function buildTableList(tableTR, selector, has_perm_read) {
    
    if(!selector)
        selector = 'div#list';

    /**
     * flush old list
     */
    
    $(selector + ' table#search_results tbody').html('');

    /**
     * display table if results or show 'no register available' dialog box
     */

    if(tableTR == '') {
        $(selector + ' div.no_registers_available').show();
        $(selector + ' div.registers_available').hide();
    } else {
        $(selector + ' div.no_registers_available').hide();
        $(selector + ' div.registers_available').show();
    }

    /**
     * populate table
     */
    $(selector + ' table#search_results tbody').html(tableTR);
    
    /**
     * remove links if dont have perms
     */

    if(has_perm_read != true) {
        $(selector + ' table#search_results tbody a').each(function() {
            $(this).parent('td').text($(this).text());
            $(this).remove();
        }); 
    }   

}




