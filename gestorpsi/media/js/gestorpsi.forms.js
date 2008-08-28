var name = "#sidebar"; 
var menuYloc = null;

$(document).ready(function(){

     var form_options = { 
          success: function(response) { 
               
               // change action atribute to update it, not insert a new one
               $('#form_client').attr('action','client/' + response + '/save/');
               $('#form_employee').attr('action','employee/' + response + '/save/');
               $('#form_place').attr('action','place/' + response + '/save/');
              
               // open new tab
               $('#sub_menu ul li a').removeClass('active'); // unselect other tabs
               $("ul.opened_tabs").show(); // display tab
               $("ul.opened_tabs li div a:first").text($('input.tabtitle').val()); // set newtab title
               $("ul.opened_tabs li div a:first").attr('href', $('form:first').attr('action').replace("/save/", "")); // set url to new tab
               
               // set ADD tab to reload the form on the next click
               $('#already_loaded').val('False');
               
               // set new tab opened to closeable when clicked
               $('div#form').addClass('edit_form');
               
               // show new options for people
               $('#people_actions').show();
               
               // show new options for place
               $('#place_actions').show();
               
               // empty room add fields
               $('#room_ input:text').val('');
               
               // show success alert
               $('#msg_area').show();
               $('#msg_area').removeClass('error');
               $('#msg_area').addClass('alert');
               $('#msg_area').text('Register saved successful!');
               // increment padding-top for blue save box
               $('#sidebar').css('padding-top','234px');
               
               
          
           },
          
          error: function() {
               // show error alert
               $('#msg_area').show();
               $('#msg_area').removeClass('alert');
               $('#msg_area').addClass('error');
               $('#msg_area').text('Error saving register!');
               $('#sidebar').css('padding-top','234px');
          }
     }; 
     
     
     /**
     * sidebar. floating box
     */
        

     menuYloc = parseInt($(name).css("top").substring(0,$(name).css("top").indexOf("px")))  
     $(window).scroll(function () {   
             var offset = menuYloc+$(document).scrollTop()+"px";  
             $(name).animate({top:offset},{duration:300,queue:false});  
     });

     /**
      * scroll to top
      */
     
     $('#sidebar input.save_button, table.newtab tr td a').click(function() {
          $.scrollTo( $('body'),  {top:'1px', left:'1px'}, 50);
	  
     });
     
     /**
     *
     * Message Area (#msg_area)
     *
     * hide msg area when cancel button is clicked
     * 
     */
     
     $('#sidebar input#cancel_button').click(function() {
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
          $('div#list.fast_menu_content').hide('slow');
     });
     
     /**
      * 
      * people post form
      * 
      * _description:
      * validate and post people (person) form.
      * 
      */

    $('.form_people').validate({event:"submit",
          rules: {
               name: {
                      required: true
               }
          },
          messages: {
              name: 'This field is required'
          },
          submitHandler: function(form) {
               $(form).ajaxSubmit(form_options);
          
          }
	});
    

    /**
     * 
     * places post form
     * 
     * _description:
     * validate and post places form.
     * 
     */
 
    $('#form_place').validate({event:"submit",
          rules: {
               label: {
                       required: true
               }
          },
          messages: {
               name: 'This field is required'
          },
          submitHandler: function(form) {
               $(form).ajaxSubmit(form_options);

          }
	});
    
    
    /**
     * 
     * fileupload
     * 
     * _description:
     * validate and post people picture from a form.
     * 
     */
	
     $('.form_file').validate({event:"submit",
          submitHandler: function(form) {
               var form_file_options = { 
                    success:    function(filename) {
                         $('#id_photo').val('/media/img/people/' + filename);
                         $('img#img_people').attr('src', '/media/img/people/' + filename); 
                    } 
               }; 
               $(form).ajaxSubmit(form_file_options);
               $('#photo_form_upload_dragplace').hide();
          }
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
     
     $('.gender').click(function() {
          if($(this).hasClass('active')) {
               $('.gender').removeClass('active');
               $('#id_gender').val($(this).attr(''));
          } else {
               $('.gender').removeClass('active');
               $(this).addClass('active');
               $('#id_gender').val($(this).attr('value'));
          }
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
     
     $('a.clips').click(function() {
          $('#photo_form_upload_dragplace').show();
     });
     
     
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
     
     // search for input texts when BODY is loaded
     
     $("form input:text").each(function(){
          var field = $(this);
          if(field.attr('mask')) {
               $(field).mask(field.attr('mask'));
          }
     });
     
     // we must to 'reload' mask function, when a field text is drawed by some javascript function 
     // see: address form, phone form
     
     function reloadMask(pattern) {
          $("form "+pattern+" input:text").each(function(){
               var field = $(this);
               if(field.attr('mask')) {
                    $(field).mask(field.attr('mask'));
               }
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
     
     function reloadDelete() {
          $('a.remove_from_form').unbind();
          $('a.remove_from_form').click(function() {
               $('#' + $(this).attr('delete') + ' input:text').val(''); // clean input fields
               $('#' + $(this).attr('delete')).hide("slow"); // hide it
               $($(this)).hide(); // so, hide me =)
          });
     }
     reloadDelete();
     
     /** 
      * 
      * address form
      * 
      * _description:
      * 
      * append address tag
      * 
      */
     
     $('#document_more a').click(function() {
          total = $(".form_document_box").length + 1;
          $("#document_more").before('<div class="form_document_box" id="document_'+total+'"><div class="form_document">'+$(".form_document").html()+'<label><br /><a class="notajax remove_from_form" delete="document_'+total+'"><span>Delete</span></a></label></div></div>');
          reloadMask('#document_'+total);
          reloadDelete();
          $('#document_'+total+' input').val('');
             
     });
     
             
             
     /** 
      * 
      * address form
      * 
      * _description:
      * 
      * append address tag
      * 
      */
     
     $('#address_more a').click(function() {
          total = $(".form_address_box").length + 1;
          $("#address_more").before('<div class="form_address_box" id="address_'+total+'"><div class="form_address">'+$(".form_address").html()+'<label><br /><a class="notajax remove_from_form" delete="address_'+total+'"><span>Delete</span></a></label></div></div>');
          reloadMask('#address_'+total);
          reloadAutoComplete();
          reloadCountries()
          reloadDelete();
          $('#address_'+total+' input').val('');
     });
     
     /** 
      * 
      * phone form
      * 
      * _description:
      * 
      * append phone form
      * 
      */
     
     $('#phone_more a').click(function() {
          total = $(".form_phone_box").length + 1;
          $("#phone_more").before('<div class="form_phone_box" id="phone_'+total+'"><div class="form_phone">'+$(".form_phone").html()+'<label><br /><a class="notajax remove_from_form" delete="phone_'+total+'"><span>Delete</span></a></label></div></div>');
          reloadMask('#phone_'+total);
          reloadDelete();
          $('#phone_'+total+' input').val('');
     });
     
             
     /** 
      * 
      * email form
      * 
      * _description:
      * 
      * append email form
      * 
      */
     
     $('#email_more a').click(function() {
          total = $(".form_email_box").length + 1;
          $("#email_more").before('<div class="form_email_box" id="email_'+total+'"><div class="form_email">'+$(".form_email").html()+'<label><br /><a class="notajax remove_from_form" delete="email_'+total+'"><span>Delete</span></a></label></div></div>');
          reloadMask('#email_'+total);
          reloadDelete();
          $('#email_'+total+' input').val('');
     });
     
             
     /** 
      * 
      * IM form
      * 
      * _description:
      * 
      * append IM form
      * 
      */
     
     $('#im_more a').click(function() {
             total = $(".form_im_box").length + 1;
             $("#im_more").before('<div class="form_im_box" id="im_'+total+'"><div class="form_im">'+$(".form_im").html()+'<label><br /><a class="notajax remove_from_form" delete="im_'+total+'"><span>Delete</span></a></label></div></div>');
             reloadMask('#im_'+total);
             reloadDelete();
             $('#im_'+total+' input').val('');
     });
     
     
     /** 
      * 
      * Website form
      * 
      * _description:
      * 
      * append Website form
      * 
      */
     
     $('#website_more a').click(function() {
          total = $(".form_website_box").length + 1;
          $("#website_more").before('<div class="form_website_box" id="website_'+total+'"><div class="form_website">'+$(".form_website").html()+'<label><br /><a class="notajax remove_from_form" delete="website_'+total+'"><span>Delete</span></a></label></div></div>');
          reloadMask('#website_'+total);
          reloadDelete();
          $('#website_'+total+' input').val('');
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
     
     $('li#add_room a').click(function() {
          $('#place_form').hide();
          $('.form_room_box').hide();
          $('#fieldset_room_identification').show();
          total = $(".form_room_box").length + 1;
          
          // add form
          $("#room_more").before('<div class="form_room_box" id="room_'+total+'"><div class="form_room">'+$(".form_room").html()+'</div></div>');
          // clean fields
          $('#room_'+total+' input').val('');
          $('#room_'+total+' textarea').text('');
          
     
          // auto insert new typing item, in the room list
          
          // first we need to clean item with empty names
          $('li.li_rooms').each(function() {
               li = $(this);
               if($(li).text()=='') {
                    li.remove();     
               }
          });
          // create new item in room list
          $('li.li_rooms:last').after('<li class="li_rooms"><a class="notajax" onclick="$(\'#place_form\').hide(); $(\'.form_room_box\').hide(); $(\'#fieldset_room_identification\').show(); $(\'#room_'+total+'\').show();"></a></li>');
          // update room name, in room list when new name is typing 
          $('#room_'+total+' input.update_name').keyup(function() {
              $('#div_list_rooms').show();
              $('li.li_rooms:last a').text($(this).val());
           });
             
     });
       
     /** show selected room fieldset  */ 
     $('li.li_rooms a').click(function() {
         $('#place_form').hide();
         $('.form_room_box').hide();
         $('#fieldset_room_identification').show();
         $('#room_' + $(this).attr('display')).show();
         $('#room_' + $(this).attr('display') + ' input.update_name').keyup(function() {
             $('#li_room_'+$(this).attr('display')+' a').text($(this).val());
         });
     });
     
   
     /**
      * 
      * autocomplete text field
      * 
      */
     
     
     // we must to 'reload' auto-complete function, when a field text is drawed by some javascript function 
     
     function reloadAutoComplete() {
             $('.city_search').unbind().autocomplete(); // !!IMPORTANT: necessary for IE6 when you have multiple fields
             $('.city_search').autocomplete("/address/search/city/", {
                     width: 355,
                     selectFirst: true,
                     minChars: 3
             });
             $(".city_search").result(function(event, data, formatted) {
                     // set city id to the hidden field
                     if (data) {
                             $(this).parent().next().find("input:hidden").val(data[1]);
                     }
             });
     }
             
     reloadAutoComplete() // load auto-complete for the first tag address
     
     // Reset value if city choices is blank
     $('.city_search').keyup(function() {
            if($(this).val() == '') {
                $(this).parent().next().find("input:hidden").val('');
            }
       });
             
     
     /** 
      * other countries address, not registered in database
      * 
      * if another country is selected, change form fields ..
      * 
      */
      
     function reloadCountries() {
             $('form select.country').change(function() {
                     selectField = $(this);
                     var form_address_div_id = selectField.parents("div.form_address_box:first").attr("id");
                                             
                     if(selectField.val() == 33) { // Brazil
                             $('#'+form_address_div_id+' div.address_noautocomplete').hide();
                             $('#'+form_address_div_id+' div.address_autocomplete').show();
                     } else {
                             $('#'+form_address_div_id+' div.address_autocomplete').hide();
                             $('#'+form_address_div_id+' div.address_noautocomplete').show();
                     }
                     });
     }
     
     reloadCountries(); // load countries select for the first tag address 
     
      /** 
      * 
      * Care Professional Agreements
      * 
      * _description:
      * 
      * append agreement select
      * 
      */
     
     
     
     function reloadDestroyLabel() {
          $('a.destroy_parent_label').unbind();
          $('a.destroy_parent_label').click(function() {
               $(this).parent('label:first').empty().fadeOut("slow");
          });
     }
     
     
     function reloadProfessionalAgreement() {
          $('#fieldset_professional_agreement select:last').change(function() {
               total = $('#fieldset_professional_agreement select').length;
              if($('#fieldset_professional_agreement select:last').val()) { // add only if last is not null
                    $("#professional_agreement_more").before('<label class="professional_agreement">'+$('#fieldset_professional_agreement label span:first').html()+'<a class="remove_from_form destroy_parent_label inline"><span>Delete</span></a></label>');
                    reloadProfessionalAgreement();
                    reloadDestroyLabel();
                    
               }
          });
     }
     
     reloadProfessionalAgreement();
     
     
     
     function reloadProfessionalWorkPlace() {
          $('#fieldset_professional_workplace select:last').change(function() {
               total = $('#fieldset_professional_workplace select').length;
              if($('#fieldset_professional_workplace select:last').val()) { // add only if last is not null
                    $("#professional_workplace_more").before('<label class="professional_workplace">'+$('#fieldset_professional_workplace label span:first').html()+'<a class="remove_from_form destroy_parent_label inline"><span>Delete</span></a></label>');
                    reloadProfessionalWorkPlace();
                    reloadDestroyLabel();
                    
               }
          });
     }
     
     reloadProfessionalWorkPlace();
     
     
});
