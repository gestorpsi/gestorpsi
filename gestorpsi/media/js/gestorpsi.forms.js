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


// ajax form options
var form_options = { 
     success: function(response, request, form) {
          var editing = null;
          if($(form).parents('#edit_form').html()) {
               editing = true;
          }

          var phone_number = '';
          var email_address = '';
          
          // adding new register!
          if(!editing)  {
               // move the content from the add form, to the edit form
               $('div#form').attr('id','tmp');
               $('div#edit_form').attr('id','form');
               $('div#tmp').attr('id','edit_form');
               $('div#form').html($('div#edit_form').html());
               
               $('div.fast_menu_content').hide();
               bindAjaxForms();
               bindFormActions();
               $('div#edit_form').show();
               
               // append new list iten
               if($('div#edit_form input[name=phoneNumber]:first') && $('div#edit_form input[name=phoneNumber]:first').val() != '' && $('div#edit_form input[name=email_email]:first').val() != undefined) {
                    phone_number = '(' + $('div#edit_form input[name=area]:first').val() + ') ' + $('div#edit_form input[name=phoneNumber]:first').val();
               }
               
               if($('div#edit_form input[name=email_email]:first').val() != undefined && $('div#edit_form input[name=email_email]:first').val() != '') {
                    email_address = $('div#edit_form input[name=email_email]:first').val();
               }
               
               var line = '<tr id="' + response + '"><td class="title"><a href="/' + $('input#app_name').val() + '/' + response + '" title="' + $('div#edit_form input.tabtitle').val() + '">' + $('div#edit_form input.tabtitle').val() + '</a>';
               
               if($('div#edit_form label .object_description').val() != undefined)
                    line += '<br /><span>' + $('div#edit_form label .object_description').val() + '</span>';
               
               line += '</td><td><span class="phone">' + phone_number + '</span><br><span class="email">' + email_address + '</span></td></tr>';
               $('#list #search_results').append(line);
               
               $('div.no_registers_available').hide();
               $('div.registers_available').show();
               bindList();
               
               // increment count
               $('span#object_length').text(parseInt($('span#object_length').text())+1);
               
          }
          

          // change action atribute to update it, not insert a new one
          $('div#edit_form .form_client').attr('action','client/' + response + '/save/'); // client form save
          $('#edit_form a.admission').attr('href','client/admission/' + response); // client admission
          $('div#edit_form .form_employee').attr('action','employee/' + response + '/save/');
          $('div#edit_form .form_place').attr('action','place/' + response + '/save/');
          $('div#edit_form .form_service').attr('action','service/' + response + '/save/');
          $('div#edit_form .form_device').attr('action','device/' + response + '/save/');
         
          // open new tab
          $('#sub_menu ul li a').removeClass('active'); // unselect other tabs
          $("ul.opened_tabs").show(); // display tab
          
          
          // update infos in tab and listing
          
          // get new title
          var new_title = $('div#edit_form input.tabtitle').val();

          // new title in tab
          $("ul.opened_tabs li div a:first, div#edit_form h2.title").text(new_title); // update titles in TAB and page title
          
          // update infos in listing 
          $("#list #search_results tr[id="+response+"] td.title a").text(new_title); // update title in listing
          $("#list #search_results tr[id="+response+"] td.title a").attr('title', new_title); // update title in listing title attribute
          
          if(editing)  {
               // get phone and mail
               if($('div#edit_form input[name=phoneNumber]:first') && $('div#edit_form input[name=phoneNumber]:first').val() != '' && $('div#edit_form input[name=phoneNumber]:first').val() != undefined) {
                    phone_number = '(' + $('div#edit_form input[name=area]:first').val() + ') ' + $('div#edit_form input[name=phoneNumber]:first').val();
               }
               
               if($('div#edit_form input[name=email_email]:first').val() != undefined && $('div#edit_form input[name=email_email]:first').val() != '') {
                    email_address = $('div#edit_form input[name=email_email]:first').val();
               }
               
               // update it
               $("#list #search_results tr[id="+response+"] td span.phone").text(phone_number); // update phone 
               $("#list #search_results tr[id="+response+"] td span.email").text(email_address); // update email
               
               if($('div#edit_form label .object_description').val() != undefined)
                    $("#list #search_results tr[id="+response+"] td.title span").text($('div#edit_form label .object_description').val());

          }
          
          // hide description
          $('div#edit_form p.description').hide();
          
          // re-sort list
          $('#list #search_results').tablesorter({sortList: [[0,0], [1,0]]});
          
          // re-draw zebra
          bindTableZebra();
          
          // reload mask
          bindFieldMask();
          
          // reload loadLinks
          bindAdmission();
          
          // set new tab opened to closeable when clicked
          $('div#form').addClass('edit_form');
         
          // show new options for people
          $('#edit_form .people_actions').show();
          
          // show new options for place
          $('#place_actions').show();
          
          // empty add form
          $('#form form:input').clearForm();
          
          // reset image from add form
          $('#form form div.photo img.img_people').attr('src','/media/img/male_generic_photo.gif.png');
          $('#form form div.photo input.photo').val('');
          
          // reset gender from add form
          $('#form form .gender').removeClass('active');
          $('#form form input.gender').val('');
          
          // empty room add fields
          $('div#edit_form #room_ input:text').val('');
          
          // show last update info
          $('div#edit_form span.editing span.last').hide();
          $('div#edit_form span.editing span.now').show();
          
          // show success alert
          $('#msg_area').removeClass('error');
          $('#msg_area').addClass('alert');
          $('#msg_area').text('Register saved successfully!');
          $('#msg_area').fadeTo(0, 1);
          $('#msg_area').show();
          $('#msg_area').fadeTo(2500, 0.40);

          // increment padding-top for blue save box
          $('.sidebar').css('padding-top','239px');
      },
     
     error: function() {
          // show error alert
          $('#msg_area').removeClass('alert');
          $('#msg_area').addClass('error');
          $('#msg_area').text('Error saving register!');
          $('#msg_area').fadeTo(0, 1);
          $('#msg_area').show();
          $('.sidebar').css('padding-top','234px');
     }
}; 


var form_organization_options = { 
     success: function(response, request, form) {
          var new_title = $('#form_organization input.tabtitle').val();
         // new title in tab
          $(".edit_form h2.title").text(new_title); // update titles page title
          
          // show success alert
          $('#msg_area').removeClass('error');
          $('#msg_area').addClass('alert');
          $('#msg_area').text('Register saved successfully!');
          $('#msg_area').fadeTo(0, 1);
          $('#msg_area').show();
          $('#msg_area').fadeTo(2500, 0.40);

          // increment padding-top for blue save box
          $('.sidebar').css('padding-top','239px');
      },
     
     error: function() {
          // show error alert
          $('#msg_area').removeClass('alert');
          $('#msg_area').addClass('error');
          $('#msg_area').text('Error saving register!');
          $('#msg_area').fadeTo(0, 1);
          $('#msg_area').show();
          $('.sidebar').css('padding-top','234px');
     }
}; 



/**
 * mini forms to quick add options
 */

var form_mini_options = {
     success: function(response, message, form) {
          
               // get option label
               var text = $(form).children('fieldset').children('label').children('input:text').val();
               
               // add <option> to asmselect select box
               $.form_mini_link.parents('fieldset').children('label').children('select.asmSelect:first').append('<option value='+response+' disabled="disabled">'+text+'</option>');
               
               // add <option> to real multiselect 
               $.form_mini_link.parents('fieldset').children('label').children('select.multiple').append('<option value='+response+' selected="selected">'+text+'</option>');
               
               // append it to list
               $.form_mini_link.parents('fieldset').children('label').children('ol').append('<li style="display: list-item;" class="asmListItem"><span class="asmListItemLabel">'+text+'</span><a class="asmListItemRemove dyn_added">remove</a></li>');
                         
               $('a.asmListItemRemove.dyn_added').unbind().click(function() {
                    $(this).parents("li").remove();
               }); 
               
               // clean form and hide it
               $(form).children('label').children('input:text').val('');
               $(form).parents('div.form_mini').hide();
               
          },
     error: function() {
          // show error alert
          $('#msg_area').show();
          $('#msg_area').removeClass('alert');
          $('#msg_area').addClass('error');
          $('#msg_area').text('Error saving register!');
          $('.sidebar').css('padding-top','234px');
     }
}; 


function bindAjaxForms() {
     
     /**
      * 
      * people post form
      * 
      * _description:
      * validate and post people (person) form.
      * 
      */

     $('.form_people').each(function() {
          $(this).validate({event:"submit",
          rules: {
               name: {
                      required: true
               }
          },
          messages: {
              name: 'Preenchimento Necessário'
          },
          submitHandler: function(form) {
               $(form).ajaxSubmit(form_options);
          
          }
          });
     });


    /**
     * 
     * places post form
     * 
     * _description:
     * validate and post places form.
     * 
     */

     
     $('.form_place').each(function() {
          $(this).validate({event:"submit",
           rules: {
                label: {
                        required: true
                }
           },
           messages: {
                name: 'Preenchimento Necessário'
           },
           submitHandler: function(form) {
                $(form).ajaxSubmit(form_options);
          
           }
          });
      });
    
    
    /**
     * 
     * service post form
     * 
     * _description:
     * validate and post places form.
     * 
     */    
    
     $('.form_service').each(function() {
          $(this).validate({event:"submit",
          rules: {
              service_name: {
                      required: true
              }
          },
          messages: {
              service_name: 'Preenchimento Necessário'
          },
          submitHandler: function(form) {
              $(form).ajaxSubmit(form_options);
          
          }
          });  
     });
    
    
     /**
     * 
     * device post form
     * 
     * _description:
     * validate and post devices form.
     * 
     */    
    
     $('.form_device').each(function() {
          $(this).validate({event:"submit",
          rules: {
            brand: {
                    required: true
            }
          },
          messages: {
            brand: 'Preenchimento Necessário'
          },
          submitHandler: function(form) {
            $(form).ajaxSubmit(form_options);
          
          }
          });
     });
    
     /**
     * 
     * organization config form
     * 
     * _description:
     * validate and post organization form.
     * 
     */    
    
     $('#form_organization').each(function() {
          $(this).validate({event:"submit",
          rules: {
            name: {
                    required: true
            }
          },
          messages: {
            name: 'Preenchimento Necessário'
          },
          submitHandler: function(form) {
            $(form).ajaxSubmit(form_organization_options);
          
          }
          });
     });
    
    
    /**
     * 
     * fileupload
     * 
     * _description:
     * validate and post people picture from a form.
     * 
     */
        
     $('.form_file').each(function() {
          $(this).validate({event:"submit",
            submitHandler: function(form) {
                 var form_file_options = { 
                      success:    function(filename) {
                         $(form).parent('div').siblings('form:first').children('div').children('div.photo').children('img.img_people').attr('src', '/media/img/organization/' + filename);
                         $(form).parent('div').siblings('form:first').children('div').children('div.photo').children('input.photo').val(filename);
                      }
                 }; 
                 $(form).ajaxSubmit(form_file_options);
                 $(form).parents('div.photo_form_upload').hide();
            }
          });  
     });


}

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
      * jQuery UI DatePicker
      * 
      * _description:
      * 
      * load Birthdate's style calendar 
      * 
      */

     $('input.birthdate').datepicker({ dateFormat: 'yy-mm-dd', changeYear: true, yearRange: '-120:+0', duration: 'fast' });
          
     /** 
      * jQuery UI DatePicker
      * 
      * _description:
      * 
      * load Care Professional
      * 
      */	

     $('input.initialActivities').datepicker({ dateFormat: 'yy-mm', changeYear: true, yearRange: '-100:+0', duration: 'fast' });

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
      
     $('div.form_mini input.cancel').click(function() {
          $(this).parents('div.form_mini:first').hide();
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
     
     
     bindAutoCompleteForm();
     
}


/**
 * select itens from an available list options (used in Services)
 * copy itens from an select multiple box to first prev sibling
 */

// available -> selected
function bind_select_itens_available() {
     $('select.itens_available option').unbind().click(function() {
          $(this).parents('fieldset').children('label').children('select.itens_selected').append('<option value="'+$(this).attr('value')+'" selected="selected">'+$(this).text()+'</option>');
          $(this).hide();
          bind_select_itens_selected();
     });
     
}

// selected -> available
function bind_select_itens_selected() {
     $('select.itens_selected option').unbind().click(function() {
          var select = $(this).parents('select');
          $(this).parents('fieldset').children('label').children('select.itens_available').children('option[value='+$(this).attr('value')+']').show();
          $(this).remove();
          bind_select_itens_available();
          // select itens again
          $(select).children('option').attr('selected','selected');
     });

}


$(document).unbind().ready(function(){
     
     bindAjaxForms();
     bindDelete();
     bindFormActions();
     bind_select_itens_selected();
     bind_select_itens_available();
     bindFieldMask();
     
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
      * select multiple plugin
      */
     
     /*
     $("#form select[multiple].asm").asmSelect({
          animate: false
     });
     */
     

     
});
