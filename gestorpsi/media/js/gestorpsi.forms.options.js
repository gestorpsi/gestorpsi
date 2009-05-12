
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

/**
 * move the content from the add form, to the edit form
 */

function cloneForms() {
    $('div#form').attr('id','tmp');
    $('div#edit_form').attr('id','form');
    $('div#tmp').attr('id','edit_form');
    $('div#form').html($('div#edit_form').html());
}

function commomPeople() {
      // show new options for people
      $('#edit_form .people_actions').show();
      
      // reset image from add form
      $('#form form div.photo img.img_people').attr('src','/media/img/male_generic_photo.gif.png');
      $('#form form div.photo input.photo').val('');

      // reset gender from add form
      $('#form form .gender').removeClass('active');
      $('#form form input.gender').val('');
}

function commomForm(response, request, form) {
    var editing = null;
    if($(form).parents('#edit_form').html()) {
        editing = true;
    }
    if(!editing)  {
        cloneForms();
    }

    // open TAB
    var new_title = openTab($('div#edit_form input.tabtitle').val());
    // display content
    displayContent('div#edit_form');
    // empty add form
    $('#form form:input').clearForm();
    // reload mask
    bindFieldMask();
    // reload form binds
    bindAjaxForms();
    bindFormActions();
}

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
 * form schedule form options
 */

var form_schedule_options = {
    success: function(response, request, form) {
    commomForm(response, request, form);
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
    // open right tab
    //openTab($('div#edit_form input.tabtitle').val());
    // display content
    $('.schedule #edit_form div.fast_content').hide();
    $('.schedule #edit_form div#schedule_occurrence_list').show();
    // show description
    $('.schedule #edit_form p.description').show();
    
    formSuccess();

    },

    error: function() {
        formError();
    }
};

/**
 * place form options
 */

var form_place_options = {
    success: function(response, request, form) {
        commomForm(response, request, form);
        $('div#edit_form .form_place').attr('action','place/' + response + '/save/');
        // show new options for place
        $('#place_actions').show();
        // empty room add fields
        $('div#edit_form #room_ input:text').val('');
        updatePlace('/place/page' + $('div#list ul.paginator').attr('actual_page'));
        formSuccess();
    },

    error: function() {
        formError();
    }
};

/**
 * service form options
 */

var form_service_options = {
    success: function(response, request, form) {
        commomForm(response, request, form);
        $('div#edit_form .form_service').attr('action','service/' + response + '/save/');
        updateService('/service/page' + $('div#list ul.paginator').attr('actual_page'));
        formSuccess();
    },

    error: function() {
        formError();
    }
};

/**
 * contact form options
 */

var form_contact_options = {
    success: function(response, request, form) {
        commomForm(response, request, form);
        $('div#edit_form .form_contact').attr('action','/contact/' + response + '/save/');
        updateContact('/contact/page' + $('div#list ul.paginator').attr('actual_page'));
        formSuccess();
    },

    error: function() {
        formError();
    }
};

/**
 * device form options
 */

var form_device_options = {
    success: function(response, request, form) {
        commomForm(response, request, form);
        $('div#edit_form .form_device').attr('action','device/' + response + '/save/');
        updateDevice('/device/page' + $('div#list ul.paginator').attr('actual_page'));
        formSuccess();
    },

    error: function() {
        formError();
    }
};

/**
 * device type form options
 */

var form_device_type_options = {
    success: function(response, request, form) {
        commomForm(response, request, form);
        $('div#edit_form .form_type_device').attr('action','device/type/' + response + '/save/');
        updateDeviceType('/device/type/page' + $('div#list_type ul.paginator').attr('actual_page'));
        formSuccess();
    },

    error: function() {
        formError();
    }
};

/**
 * client form options
 */

var form_client_options = {
    success: function(response, request, form) {
        commomForm(response, request, form);
        commomPeople();
        $('div#edit_form .form_client').attr('action','client/' + response + '/save/'); // client form save
        $('#edit_form .sidebar ul li a.print').attr('href','/client/' + response + '/print/'); // client print link
        $('div#edit_form .form_admission').attr('action','admission/' + response + '/save/'); // client admission form save
        
        /**
         * select client in referral form
         */
        
        if($('div#edit_form form.client_referral select[id=id_client] option:first').val() != undefined) {
            $('div#edit_form form.client_referral select[id=id_client] option:first').before('<option value="' + response + '" selected>' + $('div#edit_form input.tabtitle').val() + '</option>');
        } else {
            $('div#edit_form form.client_referral select[id=id_client]').html('<option value="' + response + '" selected>' + $('div#edit_form input.tabtitle').val() + '</option>');
        }

        updateClient('/client/page' + $('div#list ul.paginator').attr('actual_page'));
        formSuccess();
    },

    error: function() {
        formError();
    }
};

/**
 * employee form options
 */

var form_employee_options = {
    success: function(response, request, form) {
        commomForm(response, request, form);
        commomPeople();
        $('div#edit_form .form_employee').attr('action','employee/' + response + '/save/'); // client form save
        updateEmployee('/employee/page' + $('div#list ul.paginator').attr('actual_page'));
        formSuccess();
    },

    error: function() {
        formError();
    }
};

/**
 * user form options
 */

var form_user_options = {
    success: function(response, request, form) {
        commomForm(response, request, form);
        commomPeople();
        $('div#edit_form .form_user').attr('action','user/' + response + '/save/');
        updateUser('/user/page' + $('div#list ul.paginator').attr('actual_page'));
        formSuccess();
    },

    error: function() {
        formError();
    }
};

/**
 * professional form options
 */

var form_professional_options = {
    success: function(response, request, form) {
        commomForm(response, request, form);
        commomPeople();
        $('div#edit_form .form_careprofessional').attr('action','psychologist/' + response + '/save/'); // client form save
        updateProfessional('/careprofessional/page' + $('div#list ul.paginator').attr('actual_page'));
        formSuccess();
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
        $('ul.opened_tabs li a').attr('hide','div#schedule_header');
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
