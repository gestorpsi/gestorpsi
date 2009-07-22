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

$(function(){
	
	/** global ajax events */
	
        $.ajaxSetup({
			timeout: 10000,
			async:false
		});
        	
        $("#loading p").bind("ajaxSend", function(){
				//$('#disable_menu').show();
                $(this).show();
        }).bind("ajaxComplete", function(){
                $(this).hide();
				//$('#disable_menu').hide();
        });


		/**
         * msg_area get global events
         */
        
        $('#msg_area').ajaxError(function(event, request, settings, thrownError){
                // show success alert
               $(this).show();
               $(this).removeClass('alert');
               $(this).addClass('error');

                var error_details = '';
                
                if(!request.statusText) {
                    error_details = 'Could not establish connection to server. Please, check your connection, and try again.';
                } else {
                    error_details = $(request.responseText).children("#summary h1").html();
                    error_details += "<br />";
                    error_details += $(request.responseText).children(".exception_value").html();
                }

               $('#msg_area').html('<b>Error on Ajax request</b><br /><b>url called:</b> '+settings.url+'<br /><b>error details:</b> '+error_details+'<br /><br />Submit a <a target=\"#blank\" href=\"http://suporte.gestorpsi.com.br\">suport request</a>');
               $('#core').html('');
               return false;
        });

		
	/** horizontal menu selection */
	$("#main_menu > ul > li > a:not(.vertical), div#menu_log a:not(.logout)").click(function(){
                
                // reset vertical menu to original size
                var vertical_menu = $('#main_menu > ul > li > a.vertical');
                vertical_menu.removeClass('main_menu_big');
                vertical_menu.addClass('main_menu');
                vertical_menu.children('span').remove();
               // $('#main_menu ul li ul').addClass('main_menu_listing'); 
				$('#main_menu ul li ul').removeClass('main_menu_listing_big'); 
                
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

                //link.addClass('active');
                // show only selected
                $('#sub_'+link.attr('id')).show();
                
                // show VERTICAL submenu  (used in 'organization') if exists
                submenu = link.next('ul');
                submenu.show().fadeIn();
                        
                // hide VERTICAL submenu when mouse is out of sub-menu range
                submenu_li = link.next('ul li');
                
                submenu_li.mouseover(function(){
                        submenu.show();
                        link.addClass('hover');
                });
                link.parent('li').mouseout(function(){
                        submenu.hide();
                        //link.removeClass('active');
						link.removeClass('hover');
                });
                        
                // hide vertical submenu an item is selected
                
                array = submenu.children().children();
                array.click(function() {
                        link.parent('li').mouseout(function(){
                                //link.addClass('active');
                        });

                        $('.main_menu').removeClass('active');
                        link.addClass('active');
                        link.removeClass('main_menu');
                        //link.addClass('main_menu_big');
                        //$('#main_menu ul li ul').removeClass('main_menu_listing');
                        //$('#main_menu ul li ul').addClass('main_menu_listing_big');
                        
                        link.children('span').remove();
                        //link.append('<span>&nbsp;-&nbsp;'+$(this).text()+'</span>');
                        // hide Vertical menu
                        submenu.hide();
                        
                        // hide sub menu horizontal menu
                        $('#sub_menu ul').hide();
                        
                        // show assigned div
                        idToShow = $(this).attr('id');
                        $('#sub_menu #sub_'+idToShow).show();
                        
                        // reset submenu to first option
                        $('#sub_menu ul li a').removeClass('active');
                        $('#sub_menu ul li a.first').addClass('active');

                });
	});


        // organization menu
        $('ul#sub_organization li a.organization').click(function() {
                $('form .main_area fieldset.organization').hide();
				$('form .main_area div.photo').hide();
				if($(this).hasClass('first')) $('.main_area div.photo').show();
                $('form .main_area fieldset.organization.' + $(this).attr('display')).show();
                if($('form .main_area fieldset.organization.' + $(this).attr('display')).hasClass('comment')) {
                        $('form .main_area fieldset.comment_form').show();
                } else {
                        $('form .main_area fieldset.comment_form').hide();
                }
                /**
                 * select submenu
                 */
                $('ul#sub_organization li a.organization').removeClass('active');
                $(this).addClass('active');
                
        });
	

});




