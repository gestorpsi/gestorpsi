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
	
	$("#core a:not(.notajax)").each(function(){
		var link = $(this);
		link.click(function() {
			 $.get(link.attr('href'),
				 function(data) {
					 if(!link.attr('href')) {
						 alert('I am a ajaxlink, but i dont have the "href" atributte defined in the "<a>" tag');
						 exit();
					 } else {
						 $("#core").html(data);
					 }
					 
			 });
			 return false;
			 })
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
	
	$('.birthdate').datepicker({ dateFormat: 'dd/mm/yy', changeYear: true, yearRange: '-120:+0', duration: 'fast' });
	

});

	


	





