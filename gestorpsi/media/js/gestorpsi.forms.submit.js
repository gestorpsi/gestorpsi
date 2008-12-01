
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
     * address book form
     *
     * _description:
     * validate and post address book form.
     *
     */

     $('.form_contact').each(function() {
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


}