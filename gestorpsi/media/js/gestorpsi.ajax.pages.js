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
	
	$("#core a:not(.notajax)").click(function(){
		var link = $(this);
		//link.click(function() {
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
		//	 })
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
	 * load calendar
	 * 
	 */
	
	$('.birthdate').datepicker({ dateFormat: 'yy-mm-dd', changeYear: true, yearRange: '-120:+0', duration: 'fast' });
	
	
	
	/**
         *
         * open new tab when item is clicked (opened_tab)
         * 
         */
        
        $('#search_results.newtab tr td a').click(function() {
                $('#sub_menu ul li a').removeClass('active'); // unselect other tabs
		$("ul.opened_tabs").show(); // display tab
		$("ul.opened_tabs li div a:first").text($(this).attr('title')); // set newtab title
		$("ul.opened_tabs li div a:first").attr('href', $(this).attr('href')); // set url to new tab
	});
        
        /**
         *
         * hide opened extra tabs when close (or Cancel Button) is clicked
         *
         */
        
        $("ul.opened_tabs li div a.close, .edit_form input#cancel_button").click(function() {
		$("ul.opened_tabs").hide();
		$(".edit_form").hide();
		//loadURL('/client/', 'list');
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
	
});

	


	




