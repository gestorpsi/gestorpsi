$(document).ready(function(){



$('#people_form').validate({event:"submit",
           rules: {
		id_nome: {
		    required: true,
		    minLength: 2
              	},
		},
              submitHandler: function(form) {
		    $(form).ajaxSubmit();
			$('#notifications').html('Registro adicionado com sucesso.');
			$('#notifications').css('display', 'block');
			
			
                    
              }
           });

});
