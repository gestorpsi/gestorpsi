$(document).unbind().ready(function(){

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
	* 
	* apeend edit form
	* 
	* _description:
	* 
	* append form content inside the div "core"
	* 
	*/
	
	$("#core table.zebra tr td a").click(function(){
		var link = $(this);
		$('ul.opened_tabs').hide();
		$("#core div#edit_form").load(link.attr('href'));
		$.ajax({
			complete: function(){
				$('ul.opened_tabs').show();
				$("#core div#edit_form").show();
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
	 * jQuery UI DatePicker
	 * 
	 * _description:
	 * 
	 * load Birthdate's style calendar 
	 * 
	 */
	
	$('.birthdate').datepicker({ dateFormat: 'yy-mm-dd', changeYear: true, yearRange: '-120:+0', duration: 'fast' });
	
	/** 
	 * jQuery UI DatePicker
	 * 
	 * _description:
	 * 
	 * load Care Professional
	 * 
	 */	

	$('.initialActivities').datepicker({ dateFormat: 'yy-mm', changeYear: true, yearRange: '-100:+0', duration: 'fast' });
	
	
	/**
         *
         * open new tab when item is clicked (opened_tab)
         * 
         */
        
        $('#search_results.newtab tr td a').click(function() {
                $('#sub_menu ul li a').removeClass('active'); // unselect other tabs
		$("ul.opened_tabs").show(); // display tab
		$("ul.opened_tabs li div a:first").text($(this).attr('title')); // set newtab title
		
		$("ul.opened_tabs li div a:first").unbind().click(function() {
			$('#core .fast_menu_content').hide();
			$('#core div#edit_form').show();
			$('#sub_menu ul li a').removeClass('active');
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


	
	
});

	


	




