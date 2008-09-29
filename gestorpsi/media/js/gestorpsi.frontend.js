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

$(document).ready(function(){
	
	/** global ajax events */
	
        $.ajaxSetup( { timeout: 5000 } );
        	
        $("#loading p").bind("ajaxSend", function(){
                $(this).show();
        }).bind("ajaxComplete", function(){
                $(this).hide();
        });
        


        
        
        /**
         * msg_area get global events
         */
        
        $('#msg_area').ajaxError(function(event, request, settings, thrownError){
                // show success alert
               $(this).show();
               $(this).removeClass('alert');
               $(this).addClass('error');
               
               var error_details = $(request.responseText).children("#summary h1").html();
               error_details += "<br />";
               error_details += $(request.responseText).children(".exception_value").html();

               $('#msg_area').html('<b>Error on Ajax request</b><br /><b>url called:</b> '+settings.url+'<br /><b>error details:</b> '+error_details+'<br /><br />Submit a <a target=\"#blank\" href=\"http://suporte.gestorpsi.com.br\">suport request</a>');
               $('#core').html('');
               return false;
        });
          
        /**
         *
         * Message Area (#msg_area)
         *
         * hide msg area in ever click
         * 
         */
        
        $('#menus a, #sub_menu a').click(function() {
                $('#msg_area').removeClass();
                $('#msg_area').hide();
                $('#sidebar').css('padding-top','165px');
                
        });
        
        
	/** ajax_link: load content inside div core */
	$("#menus a:not(.notajax, .fastmenu)").click(function(){
                var link = $(this);
                
                //if($('#already_loaded').val() != 'True' || $(this).hasClass('main_menu'))  {
                        $("#core").load(link.attr('href'),'',function() {
                                $.ajax({
                                success: function() {
                                                $('#core div.fast_menu_content').hide();
                                                $('#core #'+link.attr('display')).show()
        ;
                                        }
                                });
                        });
                //}
                return false;
		});
		
	/** horizontal menu selection */
	$("#main_menu > ul > li > a:not(.vertical)").click(function(){
                
                // reset vertical menu to original size
                var vertical_menu = $('#main_menu > ul > li > a.vertical');
                vertical_menu.removeClass('main_menu_big');
                vertical_menu.addClass('main_menu');
                vertical_menu.children('span').remove();
                $('#main_menu ul li ul').addClass('main_menu_listing'); 
                
	        var link = $(this);
                $('#already_loaded').val('False');
                
                $('#sub_menu ul').hide();

                // remove active from main_menu
                $('.main_menu').removeClass('active');
                // make active on clicked menu item
                link.addClass('active');
                // show only selected
                $('#sub_'+link.attr('id')).show();
                // reset submenu to first option
                $('#sub_menu ul li a').removeClass('active');
                $('#sub_menu ul li a.first').addClass('active');
        });


	/** vertical menu selection */
	$("#main_menu > ul > li > a.vertical").mouseover(function(){
               var link = $(this);

                link.addClass('active');
                // show only selected
                $('#sub_'+link.attr('id')).show();
                // reset submenu to first option
                $('#sub_menu ul li a').removeClass('active');
                $('#sub_menu ul li a.first').addClass('active');
                
                // show VERTICAL submenu  (used in 'organization') if exists
                submenu = link.next('ul');
                submenu.show().fadeIn();
                        
                // hide VERTICAL submenu when mouse is out of sub-menu range
                submenu_li = link.next('ul li');
                
                submenu_li.mouseover(function(){
                        submenu.show();
                        link.addClass('active');
                });
                link.parent('li').mouseout(function(){
                        submenu.hide();
                        link.removeClass('active');
                });
                        
                // hide vertical submenu an item is selected
                
                array = submenu.children().children();
                array.click(function() {
                        link.parent('li').mouseout(function(){
                                link.addClass('active');
                        });

                        $('.main_menu').removeClass('active');
                        link.addClass('active');
                        link.removeClass('main_menu');
                        link.addClass('main_menu_big');
                        $('#main_menu ul li ul').removeClass('main_menu_listing');
                        $('#main_menu ul li ul').addClass('main_menu_listing_big');
                        
                        link.children('span').remove();
                        link.append('<span>&nbsp;-&nbsp;'+$(this).text()+'</span>');
                        // hide Vertical menu
                        submenu.hide();
                        
                        // hide sub menu horizontal menu
                        $('#sub_menu ul').hide();
                        
                        // show assigned div
                        idToShow = $(this).attr('id');
                        $('#sub_menu #sub_'+idToShow).show();

                });
	});


		
	/** sub menu selection */
	
	$("#sub_menu ul li a:not(.close)").click(function(){
	        var link = $(this);

                // remove active classes from sub_menu itens 
                $('#sub_menu ul li a').removeClass('active');
                // make active on clicked menu item
                link.addClass('active');
	});

	
	/**
         *
         * fast menu itens
         *
         * display content,  that already has been loaded (like client_list, client add form)
         *
         */
        
        
        $('#sub_menu a.fastmenu').click(function() {
                // hide all opened content
                $('#core .fast_menu_content').hide();

                // display choiced item and set it to already loaded
                if(!$(this).attr('display'))
                        display = 'list';
                else
                        display = $(this).attr('display');

                $('#' + display).show();
                
                $('.sidebar').css('padding-top','167px');
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
                timeout: 5000,
                
                success: function(data){
                        $("#core").html(data);
                        $('#'+showID).show();
        
                },
                 error: function(data){
                        alert('Error loading URL ' +URL);
                }
                
        });
}


