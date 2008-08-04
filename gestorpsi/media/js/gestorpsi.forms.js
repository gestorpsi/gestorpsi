$(document).ready(function(){

	/**
	 * 
	 * people post form
	 * 
	 * _description:
	 * validate and post people (person) form.
	 * 
	 */
     
    $('#form_people').validate({event:"submit",
		rules: {
			name: {
				required: true
			}
		},
		messages: {
				name: 'This field is required'
		},
		submitHandler: function(form) {
			var options = { 
				success:    function(response) { 
					// show success alert
					$('#msg_area, #msg_area .alert').show();
					$('#msg_area').addClass('alert');
					// show new options for clients
					$('#people_actions').show();
                                        // change action atribute to update it, not insert a new one
                                        $('#form_people').attr('action','client/' + response + '/save/');
                                   },
				error: function(){
					// show error alert
					$('#msg_area, #msg_area .error').show();
					$('#msg_area').addClass('error');
				}
			}; 
			$(form).ajaxSubmit(options);

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
			var options = { 
				success:    function(response) { 
					// show success alert
					$('#msg_area, #msg_area .alert').show();
					$('#msg_area').addClass('alert');
					// show new options for place
					$('#place_actions').show();
                                        // change action atribute to update it, not insert a new one
                                        $('#form_place').attr('action','place/' + response + '/save/');
                                        // set id, in add rooms link
                                        $('#place_actions a#add_room').attr('href','place/add_room/' + response);
                                   },
				error: function(){
					// show error alert
					$('#msg_area, #msg_area .error').show();
					$('#msg_area').addClass('error');
				}
			}; 
			$(form).ajaxSubmit(options);

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
	
	$('#form_file').validate({event:"submit",
		submitHandler: function(form) {
			var options = { 
				success:    function(filename) { 
					$('#id_photo').val('/media/img/client/' + filename);
					$('img#img_people').attr('src', '/media/img/client/' + filename); 
				} 
			}; 
			$(form).ajaxSubmit(options);
			$('#photo_form_upload_dragplace').hide();
		}
	});
		   
		   
	/**
	 * 
	 * file upload box
	 * 
	 * _description:
	 * make upload box moveable, as a 'draggable' box.
	 * 
	 */

	$('#photo_form_upload_dragplace').Draggable(
        {
            zIndex:    20,
            ghosting:false,
            opacity: 0.7,
            handle:    '#photo_form_upload'
        }
    );


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
		$('.gender').removeClass('active');
		$(this).addClass('active');
		$('#id_gender').val($(this).attr('value'));
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
	
	function reloadmask(pattern) {
		$("form "+pattern+" input:text").each(function(){
			var field = $(this);
			if(field.attr('mask')) {
				$(field).mask(field.attr('mask'));
			}
			});
	}

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
		$("#document_more").before('<div class="form_document_box" id="document_'+total+'"><div class="form_document">'+$(".form_document").html()+'<label><a class="notajax remove_from_form" onclick="$(\'#document_'+total+'\').remove();">Delete</a></label></div></div>');
		reloadmask('#document_'+total);
		$('#document_'+total+' input:text').val('');
		
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
		$("#address_more").before('<div class="form_address_box" id="address_'+total+'"><div class="form_address">'+$(".form_address").html()+'<label><a class="notajax remove_from_form" onclick="$(\'#address_'+total+'\').remove();">Delete Address</a></label></div></div>');
		reloadmask('#address_'+total);
		reloadautocomplete();
		reloadCountries()
		$('#address_'+total+' input:text').val('');
		
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
		$("#phone_more").before('<div class="form_phone_box" id="phone_'+total+'"><div class="form_phone">'+$(".form_phone").html()+'<label><a class="notajax remove_from_form" onclick="$(\'#phone_'+total+'\').remove();">Delete Phone</a></label></div></div>');
		reloadmask('#phone_'+total);
		$('#phone_'+total+' input:text').val('');
		
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
		$("#email_more").before('<div class="form_email_box" id="email_'+total+'"><div class="form_email">'+$(".form_email").html()+'<label><a class="notajax remove_from_form" onclick="$(\'#email_'+total+'\').remove();">Delete Email</a></label></div></div>');
		reloadmask('#email_'+total);
		$('#email_'+total+' input:text').val('');
		
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
		$("#im_more").before('<div class="form_im_box" id="im_'+total+'"><div class="form_im">'+$(".form_im").html()+'<label><a class="notajax remove_from_form" onclick="$(\'#im_'+total+'\').remove();">Delete IM</a></label></div></div>');
		reloadmask('#im_'+total);
		$('#im_'+total+' input:text').val('');
		
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
		$("#website_more").before('<div class="form_website_box" id="website_'+total+'"><div class="form_website">'+$(".form_website").html()+'<label><a class="notajax remove_from_form" onclick="$(\'#website_'+total+'\').remove();">Delete Website</a></label></div></div>');
		reloadmask('#website_'+total);
		$('#website_'+total+' input:text').val('');
		
	});

        

        
	/**
	 * 
	 * autocomplete text field
	 * 
	 */
	
	
	// we must to 'reload' auto-complete function, when a field text is drawed by some javascript function 
	
	function reloadautocomplete() {
		$('.city_search').unbind().autocomplete(); // necessary for IE6
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
			//alert($('#id_city').val());
		});
	}
        	
	reloadautocomplete() // load auto-complete for the first tag address
        
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
	   
	

  


});
