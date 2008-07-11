$(document).ready(function(){
	
	/** ajax_link: load content inside div core */
	$("#core a.ajax_link").each(function(){
	       var link = $(this);
	       link.click(function() {
	       		$.get(link.attr('url'),
				function(data) {
					if(!link.attr('url')) {
						alert('I am a ajaxlink, but i dont have the "url" atributte defined in the "<a>" tag');
						exit();
						return false;
					} else {
						$("#core").html(data);
					}
					
			});
			})
		});
		


		
});






