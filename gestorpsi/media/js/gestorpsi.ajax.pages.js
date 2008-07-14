$(document).ready(function(){
	
	/**
	 * table itens change class (zebra)
	 */
	
	$('table.zebra tr:odd').addClass('zebra_0');
	$('table.zebra tr:even').addClass('zebra_1');
	
	
	/**
	* GLOBAL: AjaxLink: load content inside div core
	*/
	
	$("#core a").each(function(){
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
	 * client (customers): show menu options
	 */
	
	$("#main_area span#client_add_infotypes").each(function(){
		var link = $(this);
		link.click(function() {
			 $('#main_area ul#form_options').toggle();
		 });
	});
	

});

	


	





