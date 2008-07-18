$(document).ready(function(){

    $('#form_people').validate({event:"submit",
		   rules: {
				name: {
					required: true
					
				}
			  },
			  messages: {
					name: 'Please enter a valid Name'
			  },
			  submitHandler: function(form) {
					$(form).ajaxSubmit();
					$('#msg_area').show();
					$('#people_actions').show();
					
				  
					
			  }
		   });
                               
                               
	$('#form_file').validate({event:"submit",
		   rules: {
				file: {
					required: true
					
				}
			  },
			  messages: {
					name: 'Please enter a valid file'
			  },
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

	$('#photo_form_upload_dragplace').Draggable( 
        { 
            zIndex:    20, 
            ghosting:false, 
            opacity: 0.7, 
            handle:    '#photo_form_upload' 
        } 
    ); 


	/**
		sex choice by icons
		set value in input hidden name "sex"
		Male as Default for insert
	*/
	
	$('.gender').click(function() { 
		$('.gender').removeClass('active');
		$(this).addClass('active');
		$('#id_gender').val($(this).attr('value'));
	});


	/**
		image upload
		display/hide upload box
	*/

	// show box and over (transparency) when clicked
	$('a.clips').click(function() {
		//alert('haehiehah');
		$('#photo_form_upload_dragplace').show();
	});
	
	
		
	/** 
		add address form 
	 */
	
	$('#address_more a').click(function() {
		total = $(".form_address_box").length + 1;
		$("#address_more").before('<div class="form_address_box" id="address_'+total+'">'+$(".form_address").html()+'<label><a class="notajax address_less" onclick="$(\'#address_'+total+'\').hide();">Delete Address</a></label></div>');
		$('#address_'+total+' input:text').val('');
		
	});

	/** 
		add phone form
	 */
	
	$('#phone_more a').click(function() {
		total = $(".form_phone_box").length + 1;
		$("#phone_more").before('<div class="form_phone_box" id="phone_'+total+'">'+$(".form_phone").html()+'<label><a class="notajax phone_less" onclick="$(\'#phone_'+total+'\').remove();">Delete Phone</a></label></div>');
		$('#phone_'+total+' input:text').val('');
		
	});

						   
	                                                             

});
