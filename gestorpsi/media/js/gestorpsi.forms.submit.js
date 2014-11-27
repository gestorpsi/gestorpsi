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
      *  My Record - Profile
      * _description:
      * change password of loged user
      *
      */

$(function() {

     /**
      *
      * generic people post form
      *
      * _description:
      * validate and post client form.
      *
      */


    $('form.form_people').validate({
        rules: {
            name: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });


     /**
      *
      * user post form
      *
      * _description:
      * validate and post user form.
      *
      */
     $('form.pwd').each(function() {
          $(this).validate({event:"submit",
              rules: {
                   password_mini: {
                          required: true
                   },

                    password_mini_conf: {
                          required: true
                   }
              },

              messages: {
                  password_mini: 'Preenchimento Necessário',
                  password_mini_conf: 'Necessário confirmar senha',
              },

              submitHandler: function(form) {
                    $(form).ajaxSubmit(form_user_options_mini);
              }
          });
     });

    $('form.form_user').validate({
        rules: {
            id_person: "required",
            email_send_user: {
                required: true,
                email: true
            },
            username: "required",
            pwd_conf: "required",
            password: "required",
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });
    
     
     /**
      *
      * contact post form
      */

    $('form.form_contact_organization').validate({
        rules: {
            name: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });

    $('form.form_contact_professional').validate({
        rules: {
            organization: "required",
            name: "required"
        },
        messages: {
            organization: 'Preenchimento Necessário',
            name: 'Preenchimento Necessário'
        }
    });


     /**
      *
      * generic post form
      *
      * _description:
      * post any form, without validate verification
      *
      */

     $('form.ajax').each(function() {
          $(this).validate({event:"submit",
          submitHandler: function(form) {
               $(form).ajaxSubmit(form_options);
            }
          });
     });

     /**
      * schedule post form
      */

    /*
    $('form.schedule').validate({
        rules: {
            referral: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });
    */

     /**
      * schedule occurrence form
      */

    $('form.schedule_occurrence').validate({
        rules: {
            room: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });
    
    /**
     *
     * rooms post form
     *
     * _description:
     * validate and post room form.
     *
     */

    $('form.form_room').validate({
        rules: {
            description: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
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


    $('form.form_place').validate({
        rules: {
            label: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });


    /**
     *
     * service post form
     *
     * _description:
     * validate and post places form.
     *
     */

    $('form.form_service').validate({
        rules: {
            service_name: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });
     
     /**
     *
     * device type  post form
     *
     * _description:
     * validate and post device type form.
     *
     */

    $('form.form_type_device').validate({
        rules: {
            label: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });

     /**
     *
     * device post form
     *
     * _description:
     * validate and post devices form.
     *
     */


    $('form.form_device').validate({
        rules: {
            brand: "required",
            model: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });



     /**
     *
     * address book form
     *
     * _description:
     * validate and post address book form.
     *
     */

    $('form.form_contact').validate({
        rules: {
            name: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });

    /**
     *
     * attach form of referral
     *
     */

    $('form.upload_referral').validate({
        rules: {
            file: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });

    /**
     *
     * admission form
     *
     * _description:
     * validate admission form.
     *
     */

    $('form.form_admission').validate({
        rules: {
            admission_date: "required"//,
        },
        messages: {
            admission_date: 'Preenchimento Necessário'
        }
    });

    /**
     *
     * referral form
     *
     * _description:
     * validate referral form.
     *
     */

    $('form.client_referral').validate();

     /**
      *
      * client family post form
      *
      * _description:
      * validate and post family client form.
      *
      */


    $('form.form_family').validate({
        rules: {
            name: "required",
            relation_level: "required"
        },
        messages: {
            name: 'Preenchimento Necessário',
            relation_level: 'Preenchimento Necessário'
        }
    });

     /**
      *
      * client company related
      *
      * _description:
      * validate and post client company related
      *
      */


    $('form.form_client_related').validate({
        rules: {
            name: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });


     /**
     *
     * support form
     *
     * _description:
     * validate and post support form.
     *
     */
    $('form.form_support_ticket').validate({
        rules: {
            contact_name: "required",
            contact_email: {
                required: true,
                email: true
            },
            contact_phone: "required",
            question: "required"
        },
        messages: {
            name: 'Preenchimento Necessário'
        }
    });

     /**
     *
     * message topic form
     *
     * _description:
     * validate and post new topic message form.
     *
     */
    $('form.message_newtopic').validate({
        rules: {
            topic: "required"
        },
        messages: {
            topic: 'Preenchimento Necessário'
        }
    });

     /**
     *
     * message topic form
     *
     * _description:
     * validate and post message form.
     *
     */
    $('form.message_sendmessages').validate({
        rules: {
            message: "required"
        },
        messages: {
            message: 'Preenchimento Necessário'
        }
    });
    
     /**
     *
     * ehr session form
     *
     * _description:
     * validate and post session form.
     *
     */

    $('form.form_session').validate({
        rules: {
            occurrence: "required"
        },
        messages: {
            occurrence: 'Preenchimento Necessário'
        }
    });
    
     /**
     *
     * ehr diagnosis form
     *
     * _description:
     * validate and post diagnosis form.
     *
     */

    $('form.form_diagnosis').validate({
        rules: {
            diagnosis: "required"
        },
        messages: {
            diagnosis: 'Preenchimento Necessário'
        }
    });
    
     /**
     *
     * ehr demand form
     *
     * _description:
     * validate and post demand form.
     *
     */

    $('form.form_demand').validate({
        rules: {
            demand: "required"
        },
        messages: {
            demand: 'Preenchimento Necessário'
        }
    });

    /**
     *
     * fileupload
     *
     * _description:
     * attach referral
     *
     */

     $('form.form_file_attach').each(function() {
          $(this).validate({event:"submit",
            submitHandler: function(form) {
                 var form_file_options = {
                      success:    function(file) {
                         $('form.client_referral div.main_area div.attach input.attach').attr("value", file);
                      }
                 };
                 $(form).ajaxSubmit(form_file_options);
                 $(form).parents('div.attach_form_upload').hide();
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

     $('form.form_file').each(function() {
          $(this).validate({event:"submit",
            submitHandler: function(form) {
                 var form_file_options = {
                      success:    function(filename) {
                         var img = $(form).parent('div').siblings('form:first').children('div').children('div.photo').children('img.img_people');
                         $(img).attr('src', '/media/img/organization/'  + $(img).attr('organization') + '/.thumb/' + filename);
                         $(form).parent('div').siblings('form:first').children('div').children('div.photo').children('input.photo').val(filename);
                      }
                 };
                 $(form).ajaxSubmit(form_file_options);
                 $(form).parents('div.photo_form_upload').hide();
            }
          });
     });



     /*
      * covenant valid form
      */
     $('form.form_covenant').validate();

});
