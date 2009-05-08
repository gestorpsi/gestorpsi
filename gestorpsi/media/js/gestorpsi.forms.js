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

/**
 * floating save box
 */

var name = ".sidebar"; 
var menuYloc = null;



/** 
* 
* _automask and automaskme()
* automatic mask for all input, type text, fields.
* 
* _dependency and thanks to Masked Input Plugin
* 	url: http://digitalbush.com/projects/masked-input-plugin/
* 
* _description:
* 
* search for a 'mask' attribute in form text fields
* 
* you only must to define the 'mask' attribute to masked fields
* 
* eg.:
* 	<input type="text" name="phone" mask="((999) 9999-9999)" />
*                                      ^^^^  ^^^^^^ ^^^^^^^^^^
* 
* masks rules:
* ------------------
* a - Represents an alpha character (A-Z,a-z)
* 9 - Represents a numeric character (0-9)
* * - Represents an alphanumeric character (A-Z,a-z,0-9) 
* 
*/
      
function bindFieldMask() {
     $("form input:text[mask]").unbind().each(function(){
          $(this).mask($(this).attr('mask'));
     });
 }

 
/**
 *
 * delete fields in forms
 *
 * used in oneToMany relationships registers
 * eg. phones, address, emails, IMs ...
 *
 */

function bindDelete() {
     $('a.remove_from_form').unbind().click(function() {
          var fieldset = $(this).parents('fieldset');
          var total = 0;
          
          // count only visible div's
          $(fieldset).children('div').each(function() {
               if($(this).css('display') != 'none') {
                    total = total + 1;
               }
          });
          
          // remove border top before delete it
          $(fieldset).children('div').removeClass('multirow');

          var div = $(this).parent('label').parent('div');

          if(total>1) {
               $(div).children('label').children('input:text').val('');
               $(div).hide();
          } else {
               $(div).children('label').children('input:text').val('');
          }
          
          // re-draw top borders if exists
          if($(fieldset).hasClass('set_multirow')) {
               $(fieldset).children('div').not(':first').addClass('multirow');
          }

     });
}


function bindAutoCompleteForm() {
     
     // Reset value if city choices is blank
     $('input.city_search').unbind().keyup(function() {
            if($(this).val() == '') {
                $(this).parent().next().find("input:hidden").val('');
            }
       });

     /// autocomplete text field
     // we must to 'reload' auto-complete function, when a field text is drawed by some javascript function 
     $('input.city_search').autocomplete("/address/search/city/", {
             width: 355,
             selectFirst: true,
             minChars: 3
     });
     
     // set cityid to the hidden field
     $("input.city_search").result(function(event, data, formatted) {
             if (data) {
                     $(this).parent().next().find("input:hidden").val(data[1]);
             }
     });
     
     //other countries address, not registered in database
     //if another country is selected, change form fields ..
     
     $('form select.country').unbind().change(function() {
           if($(this).val() == 33) { // Brazil
               // reset oldvalues
               $(this).parents('div').children('label.noautocomplete').children('input').val('');
               $(this).parents('div').children('label.noautocomplete').hide();
               $(this).parents('div').children('label.autocomplete').show();
           } else {
               // reset oldvalues
               $(this).parents('div').children('label.autocomplete').children('input').val('');
               $(this).parents('div').children('label.autocomplete').hide();
               $(this).parents('div').children('label.noautocomplete').show();
           }
     });

     // VALID IF EXIST A SHORT NAME IN FORM ORGANIZATION
     $('input.short_search').unbind().keyup(function() {
	     $.ajax({
		   type: "GET",
		   url: "/organization/check/"+ $(this).val()+"/",
		   success: function(msg){
			if (msg == '1'){
			   $("div.check_available").hide();
			} else {
			   $("div.check_available").show();
			}
		   }
	     });
     });

}


function bindFormActions() {
    
     /** 
      * 
      * clone div content and append it to form
      * 
      */
     
     $('fieldset a.add_to_form').unbind().click(function() {
          $(this).before('<div>' + $(this).parents('fieldset:first').children('div:first').html() + '</div>');
          $(this).parents('fieldset').children('div:last').children('input').val('');
          $(this).parents('fieldset').children('div:last').children('label').children('input').val('');
          // draw top-border for multirows fieldsets (eg.: address fieldset)
          if($(this).parents('fieldset').hasClass('set_multirow')) {
               $(this).parents('fieldset').children('div').removeClass('multirow');
               $(this).parents('fieldset').children('div').not(':first').addClass('multirow');
          }
          bindAutoCompleteForm();
          bindDelete();
          bindFieldMask();
     });
     
     /**
     *
     * image upload
     * 
     * _description:
     *  
     * show upload box when clicked (close automatic, when file is selected).
     * 
     */
     
     $('a.clips').unbind().click(function() {
          $(this).parents('form').parents('div').children('div.photo_form_upload').show();
     });
     
      
     /** 
      * 
      * Place form
      * 
      * _description:
      * 
      * append Room add form
      * 
      */
     
     $('div#edit_form li#add_room a').unbind().click(function() {
          $('div#edit_form #place_form').hide();
          $('div#edit_form .form_room_box').hide();
          $('div#edit_form #fieldset_room_identification').show();
          var total = $("div#edit_form .form_room_box").length + 1;
          
          // add form
          $("div#edit_form #room_more").before('<div class="form_room_box" id="room_'+total+'"><div class="form_room">'+$(".form_room").html()+'</div></div>');
          // clean fields
          $('div#edit_form #room_'+total+' input').val('');
          $('div#edit_form #room_'+total+' textarea').text('');
          
     
          // auto insert new typing item, in the room list
          
          // first we need to clean item with empty names
          $('div#edit_form li.li_rooms').each(function() {
               li = $(this);
               if($(li).text()=='') {
                    li.remove();     
               }
          });
          // create new item in room list
          $('div#edit_form li.li_rooms:last').after('<li class="li_rooms"><a class="notajax" onclick="$(\'#place_form\').hide(); $(\'.form_room_box\').hide(); $(\'#fieldset_room_identification\').show(); $(\'#room_'+total+'\').show();"></a></li>');
          // update room name, in room list when new name is typing 
          $('div#edit_form #room_'+total+' input.update_name').unbind().keyup(function() {
              $('div#edit_form #div_list_rooms').show();
              $('div#edit_form li.li_rooms:last a').text($(this).val());
           });
             
     });
       
     /** show selected room fieldset  */ 
     $('div#edit_form li.li_rooms a').unbind().click(function() {
         $('div#edit_form #place_form').hide();
         $('div#edit_form .form_room_box').hide();
         $('div#edit_form #fieldset_room_identification').show();
         $('div#edit_form #room_' + $(this).attr('display')).show();
         $('div#edit_form #room_' + $(this).attr('display') + ' input.update_name').unbind().keyup(function() {
             $('div#edit_form #li_room_'+$(this).attr('display')+' a').text($(this).val());
         });
     });
     
     /**
      * 
      * gender are choiced by icons ..
      * 
      * _description:
      * listen from an image click, so ajust selected gender in
      * a hidden input with an attribute id="id_gender"
      * 
      */
     
     $('a.gender').unbind().click(function() {
          if($(this).hasClass('active')) {
               $('.gender').removeClass('active');
               $(this).siblings('input.gender').val('');
          } else {
               $('.gender').removeClass('active');
               $(this).addClass('active');
               $(this).siblings('input.gender').val($(this).attr('value'));
          }
     });

     /**
      * 
      * Device Restriction
      * 
      * _description:
      * listen from an select change, so hide/show professional area select
      * 
      */
      $('form select.device_restriction').unbind().change(function() {
         if ($(this).val() == 1) {  // not restricted
            $(this).parents('label').parents('fieldset').children('label.device_restriction').hide();
         } else {
            $(this).parents('label').parents('fieldset').children('label.device_restriction').show();
         }
      })
      


     /**
      * 
      * Device Mobility
      * 
      * _description:
      * listen from an select change, so hide/show selects place/room.
      * 
      */     

     $('form select.device_mobility').unbind().change(function() {
     	if ($(this).val() == 1) { // Fixed Device
     		//$(this).parents('label').parents('fieldset').children('label.device_place').show();
     		$(this).parents('label').parents('fieldset').children('label.device_room').show();
     	} else {
     		//$(this).parents('label').parents('fieldset').children('label.device_place').hide();
     		$(this).parents('label').parents('fieldset').children('label.device_room').hide();
     	}
     });
     
     $('form select.device_place').unbind().change(function() {
         $(this).parents('label').parents('fieldset').children('label.device_room').children('select').children('option').hide();
         //$(this).parents('label').parents('fieldset').children('label.device_room').children('select').text('');
         $(this).parents('label').parents('fieldset').children('label.device_room').children('select').children('option.place_'+$(this).val()).show();
         //$(this).parents('label').parents('fieldset').children('label.device_room').children('select').children('option:first').append('<option value="" selected="selected"></option>');
         $(this).parents('label').parents('fieldset').children('label.device_room').children('select').children('option:visible:first').attr('selected','selected');
         //$(this).parents('label').parents('fieldset').children('label.device_room').children('option:not(.place_'+$(this).val()).hide();
     });


     /**
     * service types and service areas
     */
     
     $('select.service_area').each(function() {
          select_area = $(this).val();
          // set initial service type     
          $(this).parents('fieldset').children('label').children('select.service_type').children('option').hide();
          $(this).parents('fieldset').children('label').children('select.service_type').children('option[area=' + select_area + ']').show();
          // set initial private areas
          $(this).parents('form').children('div').children('fieldset.service_areas').hide();
          $(this).parents('form').children('div').children('fieldset.area_' + select_area).show();
          // set initial service solicitation with selected area
          $(this).parents('fieldset').children('label').children('select.service_solicitation').children('option').hide();
          $(this).parents('fieldset').children('label').children('select.service_solicitation').children('option.' + 'area_'+ select_area ).show();
     });
     
     $('select.service_area').unbind().change(function() {
          var select = $(this);
          // switch service type
          $(select).parents('fieldset').children('label').children('select.service_type').children('option').hide();
          $(select).parents('fieldset').children('label').children('select.service_type').children('option[area=' + $(this).val() + ']').show();
          $(select).parents('fieldset').children('label').children('select.service_type').children('option[area=' + $(this).val() + ']:first').attr('selected', 'selected');
          // switch service solicitation
          $(select).parents('fieldset').children('label').children('select.service_solicitation').children('option').hide();
          $(select).parents('fieldset').children('label').children('select.service_solicitation').children('option.area_'+$(select).val()).show();
          // show privates areas
          $(select).parents('form').children('div').children('fieldset.service_areas').hide();
          $(select).parents('form').children('div').children('fieldset.area_' + $(this).val()).show();
     });
     
      // quick add
      
     $('div form input.cancel').click(function() {
          $(this).parent('label').parent('fieldset').children('label').children('input:text').val('');
		  $(this).parents('div.form_mini:first').hide();
		  $(this).parents('div.form:first').hide();
          return false;
     
     });
     
     $('a.form_mini').unbind().click(function() {
          var form_mini = $(this).parents('form').parents('div').children('div.'+$(this).attr('display')).show();
          $.form_mini_link = $(this);
          $(form_mini).children('form').validate({
               event:"submit",
               rules: {
                    label: {
                            required: true
                    }
               },
               messages: {
                    name: 'This field is required'
               },
               submitHandler: function(form) {
                    $(form).ajaxSubmit(form_mini_options);
               }
          });
     });
     
    /**
	* sidebar. cancel buttom if is a new register
	*/
	
	$('#sidebar input#cancel_button').click(function() {
	    $('div#form.fast_menu_content input:text').val('');
	    $('div#form.fast_menu_content').hide();
	    $('div#sub_menu ul li a').removeClass('active');
	    $('div#sub_menu ul li a:first').addClass('active');
	    $('div#list.fast_menu_content').show();
		$("ul.opened_tabs").hide();
		$("#edit_form").hide();
		$("#form").hide();
	});

     $('select.toggle_parent_label').change(function() {
         var select = $(this);
         $(select).parents('fieldset').children('label.hidden').hide();
         $(this).children('option').each(function() {
             if($(this).attr('selected')) {
                 if($(this).attr('label')) {
                     var class_name = $(this).attr('label');
                     $(select).parents('fieldset').children('label.'+class_name).show();
                 }
             }
         });
     });

     bindAutoCompleteForm();
   
}

function bindFormMisc() {

    /**
    * bind select itensselected
    * select itens from an available list options (used in Services)
    * copy itens from an select multiple box to first prev sibling
    */

    $('select.itens_available option').unbind().click(function() {
        $(this).parents('fieldset').children('label').children('select.itens_selected').append('<option value="'+$(this).attr('value')+'" selected="selected">'+$(this).text()+'</option>');
        $(this).hide();
        $('select.itens_selected option').unbind().click(function() {
            var select = $(this).parents('select');
            $(this).parents('fieldset').children('label').children('select.itens_available').children('option[value='+$(this).attr('value')+']').show();
            $(this).remove();
            // select itens again
            $(select).children('option').attr('selected','selected');
        });
     });



     /**
     * sidebar. floating box
     */
        
     /*
     menuYloc = parseInt($(name).css("top").substring(0,$(name).css("top").indexOf("px")))  
     $(window).scroll(function () {   
             var offset = menuYloc+$(document).scrollTop()+"px";  
             $(name).animate({top:offset},{duration:300,queue:false});  
     });
     */
     /**
      * scroll to top
      */
     /*
     $('.sidebar input.save_button, table.newtab tr td a').click(function() {
          $.scrollTo( $('body'),  {top:'1px', left:'1px'}, 50);
	  
     });
     */
     /**
     *
     * Message Area (#msg_area)
     *
     * hide msg area when cancel button is clicked
     * 
     */
     
     $('.sidebar input#cancel_button').click(function() {
          $('#msg_area').removeClass();
          $('#msg_area').hide();
          $('div#sub_menu ul li a').removeClass('active');
	  $('div#sub_menu ul li a:first').addClass('active');
	  $('div#list.fast_menu_content').show();
     });
     
     /**
      * hide list when item is clicked
      */
     
     $('table.newtab tr td a').click(function() {
          $('div#list.fast_menu_content').hide();
     });
     

     
     /**
      * hide all itens available select boxes, and show only the first
      */
     
     $('fieldset select.multiple.itens_available').parents('fieldset').each(function() {
          $(this).children('label').children('select.multiple.itens_available:not(:first)').hide();
     });

     $('fieldset label a.select_multiple_menu').each(function() { $(this).removeClass('active'); });
     $('fieldset label a.select_multiple_menu').parents('label').each(function() { $(this).children('a.select_multiple_menu').not(':first').addClass('active'); });
     
     $('label a.select_multiple_menu').click(function() {
          $(this).parents('fieldset').children('label').children('select.itens_available').hide();
          $(this).parents('fieldset').children('label').children('select.itens_available.' + $(this).attr('display')).show();
          $('fieldset label a.select_multiple_menu').removeClass('active');
          $(this).addClass('active');
     });
     
     
     /**
      * contact form
     */
     
     $('form.form_contact select[name=type]').change(function() {
          $(this).parents('fieldset').siblings('.contact').hide();
          $(this).parents('fieldset').siblings('.' + $(this).val()).show();
          
          // its necessary, because you can have two required fields, organization name OR professional name
          // reset name attribute, and rewrite it.
          $(this).parents('form').children('div').children('fieldset').children('label').children('input[type=text].cleanme').attr('name','');
          $(this).parents('form').children('div').children('fieldset').children('label').children('input[type=text].' + $(this).val() + '_name').attr('name','name');
                    
     });
     

     /**
      * referral service/professional select
      *
      * when select a service, display only professionals related
      * when select a professional, display only services related
      */

     $('select.referral[name=service] option').click(function() {
        var service = $(this);
        if($(service).hasClass('all')) {
            $('select.referral[name=professional] option').show();
        } else {
            $('select.referral[name=professional] option').hide();
            $('select.referral[name=professional] option').each(function() {
                if($(service).hasClass($(this).val())) {
                    $(this).show();
                }
            });
        }
     });


     $('select.referral[name=professional] option').click(function() {
        var professional = $(this);
        if($(professional).hasClass('all')) {
            $('select.referral[name=service] option').show();
        } else {
            $('select.referral[name=service] option').hide();
            $('select.referral[name=service] option').each(function() {
                if($(professional).hasClass($(this).val())) {
                    $(this).show();
                }
            });
        }
     });

    /**
     * hide and show weekly, monthly and yearly extra option in schedule form
     */
    
    $('.schedule div.switch input[type=radio]').unbind().click(function() {
        var div = $(this).parents('label').parents('div');
        var elements_to_show = '.' +$(div).attr('clean')+'_'+$(this).val();
        $('.' +$(div).attr('clean')).hide();
        $(elements_to_show).show();
    });

    $('.schedule div.switch input[type=checkbox]').unbind().click(function() {
        var div = $(this).parents('div');
        if(!$(this).attr('checked')) {
            $('.' +$(div).attr('clean')).hide();
        } else {
            $('.' +$(div).attr('clean')).show();
        }
    });

    /**
     * generic switch to display and hide form elements
     */
    
    $('.generic_switch').unbind().click(function() {
        var el = $(this);
        $(el.attr('hide')).hide();
        $(el.attr('show')).show();
    });
    
     /**
      * select multiple plugin
      */
     
     /*
     $("#form select[multiple].asm").asmSelect({
          animate: false
     });
     */
     
}
