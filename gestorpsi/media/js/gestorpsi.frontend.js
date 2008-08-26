$(document).ready(function(){
	
	/** global ajax events */
	
        $.ajaxSetup( { timeout: 5000 } );
        	
        $("#loading p").bind("ajaxSend", function(){
                $(this).show();
        }).bind("ajaxComplete", function(){
                $(this).hide();
        });
        
        $('#msg_area').ajaxError(function(event, request, settings, thrownError){
                // show success alert
               $(this).show();
               $(this).removeClass('alert');
               $(this).addClass('error');
               $('#msg_area').html('<b>Error on Ajax request</b><br /><b>url called:</b> '+settings.url+"<br /><b>reason:</b> unknown");
        });
          
        /**
         *
         * Message Area (#msg_area)
         *
         * hide msg area in ever click
         * 
         */
        
        $('a').click(function() {
                $('#msg_area').removeClass();
                $('#msg_area').hide();
                
        });
        
        
	/** ajax_link: load content inside div core */
	$("#menus a:not(.notajax)").each(function(){
                var link = $(this);
                link.click(function() {
                        // only reload, if it is not a fastmenu or a mainmenu link
                        if($('#already_loaded').val() != 'True' || $(this).hasClass('main_menu')) {
                                $("#core").load(link.attr('href'));
                                
                                // if is defined page to display, show it
                                $.ajax({
                                complete: function(){
                                        if(link.attr('display')) {
                                                $('#'+link.attr('display')).show();
                                        }   
                                }
                                });
                        }
			return false;
		})
	});
		
	/** menu selection */
	$("#main_menu > ul > li > a").each(function(){
	       var link = $(this);
	       link.click(function() {
                        //alert($(this).attr('id'));
                        $('#already_loaded').val('False');
                        
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
				
                        // hide vertical submenu an item is selected
                        
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
	
	$("#sub_menu ul li a:not(.close)").each(function(){
	       var link = $(this);
	       link.click(function() {
		       	// remove active classes from sub_menu itens 
	       		$('#sub_menu ul li a').removeClass('active');
	       		// make active on clicked menu item
	       		link.addClass('active');
			})
		});	
	
	/**
         *
         * fast menu itens
         *
         * display content,  that already has been loaded (like client_list, client add form)
         *
         */
        
        
        $('#sub_menu a.fastmenu').click(function() {
                //alert('clicou?');
                // hide all opened content        
                $('.fast_menu_content').hide();
                
                // display choiced item and set it to already loaded
                if(!$(this).attr('display'))
                        display = 'list';
                else
                        display = $(this).attr('display');
                
                $('#' + display).show();
                                
                //$('#already_loaded').val('True');
                return false;
        });
        
        
        /**
	 * ajaxable
	 *
	 * function used to re-bind an URL (used in opened tabs, when a new link is added by JavaScript)
	 *
	 */
	
	
	$(".ajaxable").click(function(){
		$.get($(this).attr('href'),
			function(data) {
				$("#core").html(data);
		});
	});
      

});



function loadURL(URL, showID) {
        $.ajax({
                url: URL,
                type: 'GET',
                dataType: 'html',
                timeout: 1000,
                
                success: function(data){
                        $("#core").html(data);
                        $('#'+showID).show();
        
                },
                 error: function(data){
                        alert('Error loading URL ' +URL);
                },
                
        });
}
