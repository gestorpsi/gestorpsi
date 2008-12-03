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
	$("#search_results.newtab tr td a").unbind().click(function(){
		var link = $(this);
		$('#core .fast_menu_content').hide();
		$('ul.opened_tabs').hide();
		$("#core div#edit_form").load(link.attr('href'));
		$.ajax({
			complete: function(){
				$('ul.opened_tabs').show();
				$("#core div#edit_form").show();
			}
		});
		
		$('#sub_menu ul li a').removeClass('active'); // unselect other tabs
		$("ul.opened_tabs").show(); // display tab
		$("ul.opened_tabs li div a:first").text(link.attr('title')); // set newtab title
		
		$("ul.opened_tabs li div a:first").unbind().click(function() {
			$('#core .fast_menu_content').hide();
			$('#core div#edit_form').show();
			$('#sub_menu ul li a').removeClass('active');
		});

		return false;
	});
	
	
	$("ul.paginator a").unbind().click(function(){
		var link = $(this);
		$("div#list").load(link.attr('href'));
		$('div#list').show();
		return false;
	});
}


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

function bindTableZebra() {
	$('table.zebra tr:odd').addClass('zebra_0');
	$('table.zebra tr:even').addClass('zebra_1');
}

function bindAdmission() {
	$('a.admission').unbind().click(function() {
		link = $(this);
		$('#edit_form').load(link.attr('href'));
		$.ajax({
			complete: function(){
				$('#core .fast_menu_content').hide();
				$('div#edit_form').show();
				$('div#edit_form .form_client').hide();
				$('#edit_form').show();
				
				$('#sub_menu ul li a').removeClass('active'); // unselect other tabs
				$("ul.opened_tabs").show(); // display tab
				$("ul.opened_tabs li div a:first").text(link.attr('title')); // set newtab title
			}
		});
		$('#msg_area').removeClass();
                $('#msg_area').hide();
                $('.sidebar').css('padding-top','165px');
		return false;	
	});
}

$(document).unbind().ready(function(){

	bindList();
	bindTableZebra();
	bindAdmission();
	
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
            $(".edit_form").hide();
            $('div#sub_menu li a[display="list"]').addClass('active');
            $('div#list.fast_menu_content').show();
        });
	
	/**
	* sidebar. cancel buttom if is a new register
	*/
	
	$('#sidebar input#cancel_button').click(function() {
	    $('div#form.fast_menu_content input:text').val('');
	    $('div#form.fast_menu_content').hide();
	    $('div#sub_menu ul li a').removeClass('active');
	    $('div#sub_menu ul li a:first').addClass('active');
	    $('div#list.fast_menu_content').show();
	});
	
	

	$("table.devices td.item").click(function(){
		var class_name_to_display = $(this).attr('display');
		$('.' + class_name_to_display).toggle();
	});
	
	
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
			$('div#sub_menu ul#'+link.attr('sub_menu')+' li a[display="'+link.attr('display')+'"]').addClass('active');
		}
	
		return false;
        });

	// organization menu
	$('#form_organization .main_area fieldset.organization:not(.first)').hide();


    $('a.notajax').click(function() {
        return false;
    });
	
});

	


	




