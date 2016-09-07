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
        	
         $("#loading").bind("ajaxStart", function(){
           $(this).show();
           $('#over').show();
         }).bind("ajaxStop", function(){
           $(this).hide();
           $('#over').hide();
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


        /**
         *  vertical main menu selection
         */
    
        $("#main_menu > ul > li > a.vertical").mouseover(function(){
            $('ul.myoffice').show();
        });
        $("ul.myoffice li").each(function(){ 
            var menu = $('ul.myoffice'); 
             
            $(this).hover(function(){ 
                menu.show();
                $('#main_menu a#myoffice').addClass('border_menu_active');
            }, function(){
                menu.hide();
                $('#main_menu a#myoffice').removeClass('border_menu_active');
            });
        });
        


        // organization menu
        $('ul#sub_organization li a.organization').click(function() {
                $('form .main_area fieldset.organization').hide();
                $('form .main_area div.organization').hide();
				$('form .main_area div.photo').hide();
				if($(this).hasClass('first')) $('.main_area div.photo').show();
                $('form .main_area fieldset.organization.' + $(this).attr('display')).show();
                $('form .main_area div.organization.' + $(this).attr('display')).show();
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

        /**
         * close message box 
         */

        $('.msg_area_top').effect('highlight', {}, 1000);
        $('.msg_area_top a.close_link').click(function() {
            $(this).parent('#msg_area').effect('blind');
            $('a.prev_day, a.next_day').removeClass('margin_top_fix');
        });
        
        /**
         * confirm dialog
         */
        
        $('a.confirm').click(function() {
                if(!confirm($(this).attr('msg'))) {
                    return false;
                }
        });

        // open mini-calendar
        $('a#calendar_link').click(function() {
            $("div#mini_calendar").toggle();
        });

        /**
         * display hide items in ehr
         */

        $('a.item_description').live('click', function() {
            $(this).parent('li').children('div.description:hidden').effect('blind', {'mode':'show'}, 100);
            $(this).parent('li').children('div.description:not(hidden)').hide();
        });

        $('a.item_description_all').click(function() {
            if(!$(this).hasClass('opened')) {
                $('li div.description').effect('blind', {'mode':'show'}, 300);
                $(this).addClass('opened');
            } else {
                $('li div.description').hide();
                $(this).removeClass('opened');                
            }
        });


});
