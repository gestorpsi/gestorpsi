$(document).ready(function(){

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
                                        if(link.attr('display')) {
                                                $('#'+link.attr('display')).show();
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
         * hide opened extra tabs when clicked
         *
         */
        
        $("ul.opened_tabs li div a.close").click(function() {
		$("ul.opened_tabs").hide();
		$(".edit_form").hide();
		//loadURL('/client/', 'list');
	});
	
	
});

	


	




