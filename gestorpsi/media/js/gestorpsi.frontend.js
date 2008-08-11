$(document).ready(function(){
	
	/** global ajax events */
	/*
	$("#loading p").ajaxSend(function(evt, request, settings){
  		 $(this).show();
 		});
	$("#loading p").ajaxStop(function(evt, request, settings){
  		 $(this).hide();
 		}); 		
	*/
	
        $("#loading p").bind("ajaxSend", function(){
                $(this).show();
        }).bind("ajaxComplete", function(){
                $(this).hide();
        });

        
        
	/** ajax_link: load content inside div core */
	$("#menus a:not(.notajax)").each(function(){
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
	$("#main_menu > ul > li > a").each(function(){
	       var link = $(this);
	       link.click(function() {
                        //alert($(this).attr('id'));
                        
                        if(!$(this).nextAll("ul:first").find("li > a").attr('id')) {
                                // i am NOT a vertical menu
                                // so lets, hide all sub_menu menu
                                // ** for vertical menu, sub_menus will hide, just when itens clicked
                                $('#sub_menu ul').hide();
                        }
	       		
	       		
	       		// remove active from main_menu
	       		$('.main_menu').removeClass('active');
	       		// make active on clicked menu item
	       		link.addClass('active');
	       		// show only selected
	       		$('#sub_'+link.attr('id')).show();
	       		// reset submenu to first option
	       		$('#sub_menu ul li a').removeClass('active');
	       		$('#sub_menu ul li a.first').addClass('active');
	       		
                        /**
                         * Vertical Menu
                         */
                        
	       		// show VERTICAL submenu  (used in 'organization') if exists
	       		submenu = link.next('ul');
	       		submenu.show().fadeIn();
				
                        // hide VERTICAL submenu when mouse is out of sub-menu range
                        submenu_li = link.next('ul li');
                        
                        submenu_li.mouseover(function(){
                                submenu.show();
                        })
                        submenu_li.mouseout(function(){
                                submenu.hide();
                        })
				
                        // hide submenu horizontal an item is selected
                        
                        array = submenu.children().children();
                        array.each(function() { $(this).click(function() {
                                // hide Vertical menu
                                submenu.hide();
                                
                                // hide sub menu horizontal menu
                                $('#sub_menu ul').hide();
                                
                                // show assigned div
                                idToShow = $(this).attr('id');
                                $('#sub_menu #sub_'+idToShow).show();
                                
                                } ); });
				
			})
		});
		
	/** sub menu selection */
	
	$("#sub_menu ul li a").each(function(){
	       var link = $(this);
	       link.click(function() {
		       	// remove active classes from sub_menu itens 
	       		$('#sub_menu ul li a').removeClass('active');
	       		// make active on clicked menu item
	       		link.addClass('active');
			})
		});	
	
		
});






