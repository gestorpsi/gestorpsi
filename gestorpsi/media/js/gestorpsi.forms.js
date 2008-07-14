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

});
