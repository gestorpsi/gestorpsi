
function formSuccess() {
     // show success alert
     $('#msg_area').removeClass('error');
     $('#msg_area').addClass('alert');
     $('#msg_area').text('Register saved successfully!');
     $('#msg_area').fadeTo(0, 1);
     $('#msg_area').show();
     $('#msg_area').fadeTo(2500, 0.40);

     // increment padding-top for blue save box
     $('.sidebar').css('padding-top','239px');
}

function formError() {
     // show error alert
     $('#msg_area').removeClass('alert');
     $('#msg_area').addClass('error');
     $('#msg_area').text('Error saving register!');
     $('#msg_area').fadeTo(0, 1);
     $('#msg_area').show();
     $('.sidebar').css('padding-top','234px');
}

function openTab(title) {
    // open new tab
    $('#sub_menu ul li a').removeClass('active'); // unselect other tabs
    $("ul.opened_tabs").show(); // display tab

    // set title 
    $("ul.opened_tabs li div a:first, div#edit_form h2.title").text(title); // update titles in TAB and page title
    
    // set new tab opened to closeable when clicked
    $('div#form').addClass('edit_form');

    return title
}

function displayContent(selector) {
    $('div.fast_menu_content').hide();
    $(selector).show();
    //$('div#edit_form').show();
}

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

               // reload form binds
               bindAjaxForms();
               bindFormActions();
               
               // append new list item
               if($('div#edit_form input[name=phoneNumber]:first') && $('div#edit_form input[name=phoneNumber]:first').val() != '' && $('div#edit_form input[name=email_email]:first').val() != undefined) {
                    phone_number = '(' + $('div#edit_form input[name=area]:first').val() + ') ' + $('div#edit_form input[name=phoneNumber]:first').val();
               }

               if($('div#edit_form input[name=email_email]:first').val() != undefined && $('div#edit_form input[name=email_email]:first').val() != '') {
                    email_address = $('div#edit_form input[name=email_email]:first').val();
               }

               var line = '<tr id="' + response + '"><td class="title"><a href="/' + $('input#app_name').val() + '/' + response + '/" title="' + $('div#edit_form input.tabtitle').val() + '">' + $('div#edit_form input.tabtitle').val() + '</a>';

               if($('div#edit_form label .object_description').val() != undefined)
                    line += '<br /><span>' + $('div#edit_form label .object_description').val() + '</span>';

               line += '</td><td><span class="phone">' + phone_number + '</span><br><span class="email">' + email_address + '</span></td></tr>';
               $('#list #search_results').append(line);

               $('div.no_registers_available').hide();
               $('div.registers_available').show();
               bindList();

               // increment count
               $('span#object_length').text(parseInt($('span#object_length').text())+1);
               
          } else { // editing
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


          // open TAB
          var new_title = openTab($('div#edit_form input.tabtitle').val());
          // display content
          displayContent('div#edit_form');

          // change action atribute to update it, not insert a new one
          $('div#edit_form .form_client').attr('action','client/' + response + '/save/'); // client form save
          $('div#edit_form .form_admission').attr('action','admission/' + response + '/save/'); // client admission form save
          $('#edit_form .sidebar ul li a.print').attr('href','/client/' + response + '/print/'); // client print link
          $('div#edit_form .form_employee').attr('action','employee/' + response + '/save/');
          $('div#edit_form .form_place').attr('action','place/' + response + '/save/');
          $('div#edit_form .form_service').attr('action','service/' + response + '/save/');
          $('div#edit_form .form_device').attr('action','device/' + response + '/save/');
          $('div#edit_form .form_user').attr('action','user/' + response + '/save/');
          
          // update infos in listing
          $("#list #search_results tr[id="+response+"] td.title a").text(new_title); // update title in listing
          $("#list #search_results tr[id="+response+"] td.title a").attr('title', new_title); // update title in listing title attribute

          // hide description
          $('div#edit_form p.description').hide();

          // try to sort new table
          $('#list #search_results').tablesorter({sortList: [[0,0], [1,0]]});

          // reload mask
          bindFieldMask();

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

          /**
           * client referral options
           */
           
          if($(form).hasClass('form_client')) {
              if(!editing) {
                 // add new client in new referral form and selected it
                 if($('div#edit_form form.client_referral select[id=id_client] option:first').val() != undefined) {
                    $('div#edit_form form.client_referral select[id=id_client] option:first').before('<option value="' + response + '" selected>' + new_title + '</option>');
                } else {
                    $('div#edit_form form.client_referral select[id=id_client]').html('<option value="' + response + '" selected>' + new_title + '</option>');
                }
                 // set client id in a hidden field
                 $('div#edit_form input[name=object_id]').val(response)
             }
           }


        /** 
         * schedule options 
         */
        
        if($(form).hasClass('schedule')) {
                var day_clicked = $('form.schedule').children('.sidebar').children('.bg_blue').children('.day_clicked').val();
                updateGrid('/schedule/occurrences/' + day_clicked);
                
                /** removed flexbox to addit again */
                $('div#form form.schedule div#fb_client input[id=fb_client_hidden]:first').remove();
                $('div#form form.schedule div#fb_client input[id=fb_client_input]:first').remove();
                $('div#form form.schedule div#fb_client span[id=fb_client_arrow]:first').remove();
                $('div#form form.schedule fieldset.existing_referral div.client_referrals').hide();
                bindScheduleForm();

                // load inserted data
                updateScheduleReferralDetails('/schedule/events/' + response + '/');
                // display success message
                formSuccess();
                // open right tab
                openTab($('div#edit_form input.tabtitle').val());
                // display content
                $('.schedule #edit_form div.fast_content').hide();
                $('.schedule #edit_form div#schedule_occurrence_list').show();
                // show description
                $('.schedule #edit_form p.description').show();
        }

          // display success message
          formSuccess();
      },

     error: function() {
          formError();
     }
};

/**
 * organization submit form options
 */

var form_organization_options = {
     success: function(response, request, form) {

	if ( response == "false" ){
	  	alert("Short name not available!");
	  	return false;
	} else {
      	var new_title = $('#form_organization input.tabtitle').val();
      	// new title in tab
     	 $(".edit_form h2.title").text(new_title); // update titles page title
      	formSuccess();
	}
      },

     error: function() {
          formError();
     }
};

/**
 * client referral submit form options
 * submit client referral form and update referral list
 */

var form_client_referral_options = {
    success: function(response, request, form) {
        formSuccess();
        // update list
        updateReferral('/referral/client/' + $('div#edit_form input[name=object_id]').val() + '/');
        $('div#edit_form div#client_referral_list table div.msg_area').hide();
    },

    error: function() {
        formError();
    }
};

/**
 * schedule form submit
  */

var form_schedule_occurrence_options = {
    success: function(response, request, form) {
        // update list
        var day_clicked = $('form.schedule').children('.sidebar').children('.bg_blue').children('.day_clicked').val();

        updateGrid('/schedule/occurrences/' + day_clicked);
        bindScheduleForm();
        //$('ul.opened_tabs li a').attr('hide','div#schedule_header');
        // load inserted data
        //updateScheduleReferralDetails('/schedule/events/' + response + '/');
        // display success message
        formSuccess();
    },

    error: function() {
        formError();
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

               // add <option> to asm select box
               $.form_mini_link.parents('label').children('select.asm:first').append('<option value='+response+' selected="selected">'+text+'</option>');

               // add <option> to real multiselect
               $.form_mini_link.parents('fieldset').children('label').children('select.multiple').append('<option value='+response+' selected="selected">'+text+'</option>');

               // append it to list
               $.form_mini_link.parents('fieldset').children('label').children('ol').append('<li style="display: list-item;" class="asmListItem"><span class="asmListItemLabel">'+text+'</span><a class="asmListItemRemove dyn_added">remove</a></li>');

               $('a.asmListItemRemove.dyn_added').unbind().click(function() {
                    $(this).parents("li").remove();
               });

               // clean form and hide it
               $(form).children('fieldset').children('label').children('input:text').val('');
               $(form).parents('div.form_mini').hide();

          },
     error: function() {
          formError();
     }
}; 
