$(document).ready(function(){
	
	/** global ajax events */
	$("#loading p").ajaxSend(function(evt, request, settings){
  		 $(this).show();
 		});
	$("#loading p").ajaxStop(function(evt, request, settings){
  		 $(this).hide();
 		}); 		
	
	/** ajax_link: load content inside div core */
	$("#menus a").each(function(){
	       var link = $(this);
	       link.click(function() {
				$.ajax({
					url: link.attr('href'),
					type: 'GET',
					dataType: 'html',
					timeout: 1000,
					error: function(){
						alert('Error loading template '+link.attr('href'));
					},
					success: function(data){
						if(!link.attr('href')) {
							//alert('I am a ajaxlink, but i dont have an "url" atributte defined in my "<a>" tag =[');
						} else {
							$("#core").html(data);
						}
					},
					send: function(data) {
						alert('enviado');
					}
				});
				return false;
			})
		});
		
	/** menu selection */
	$("#main_menu li a").each(function(){
	       var link = $(this);
	       link.click(function() {
	       		/** hide all sub_menu menu */
	       		$('#sub_menu ul').hide();
	       		/** remove active from main_menu */
	       		$('.main_menu').removeClass('active');
	       		/** make active on clicked menu item */
	       		link.addClass('active');
	       		/** show only selected */
	       		$('#sub_'+link.attr('id')).show();
	       		/** reset submenu to first option */
	       		$('#sub_menu ul li a').removeClass('active');
	       		$('#sub_menu ul li a.first').addClass('active');
			})
		});
		
	/** sub menu selection */
	$("#sub_menu ul li a").each(function(){
	       var link = $(this);
	       link.click(function() {
		       	/** remove active classes from sub_menu itens */
	       		$('#sub_menu ul li a').removeClass('active');
	       		/** make active on clicked menu item */
	       		link.addClass('active');
			})
		});	

		
});






