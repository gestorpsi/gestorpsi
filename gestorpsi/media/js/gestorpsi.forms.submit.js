
function bindAjaxForms() {

     /**
      *
      * client post form
      *
      * _description:
      * validate and post client form.
      *
      */

     $('form.form_client').each(function() {
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
                   $(form).ajaxSubmit(form_client_options);

              }
          });
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
     
     $('form.form_user').each(function() {
          $(this).validate({event:"submit",
              rules: {
                   email_send_user: {
                          required: true,
                          email: true
                   },

                   username: {
                          required: true
                   },

                   pwd_conf: {
                          required: true
                   },

                    password: {
                          required: true
                    }
                    
              },
              messages: {
                  username: 'Preenchimento Necessário',
                  password: 'Preenchimento Necessário',
                  pwd_conf: 'Necessário confirmar senha',
                  email_send_user: 'Preenchimento Necessário',
              },
              submitHandler: function(form) {
                    $(form).ajaxSubmit(form_user_options);
              }
          });
     });
     
     /**
      *
      * professional post form
      */

     $('form.form_careprofessional').each(function() {
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
                   $(form).ajaxSubmit(form_professional_options);

              }
          });
     });
     
     /**
      *
      * employee post form
      */

     $('form.form_employee').each(function() {
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
                   $(form).ajaxSubmit(form_employee_options);

              }
          });
     });
     
     /**
      *
      * contact post form
      */

     $('form.form_contact').each(function() {
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
                   $(form).ajaxSubmit(form_contact_options);

              }
          });
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

     $('form.schedule').each(function() {
          $(this).validate({event:"submit",
          //rules: {
               //service: { required: true },
               //client: { required: true },
               //professional: { required: true }
          //},
          submitHandler: function(form) {
               //$(form).ajaxSubmit(form_schedule_options);
               $(form).ajaxSubmit(form_schedule_options);
            }
          });
     });

     /**
      * schedule occurrence form
      */

     $('form.schedule_occurrence').each(function() {
          $(this).validate({event:"submit",
              rules: {
                   room: { required: true }
              },
              submitHandler: function(form) {
                   $(form).ajaxSubmit(form_schedule_occurrence_options);
                }
          });
     });

     /**
      * referral post form
      */

     $('form.client_referral').each(function() {
          $(this).validate({event:"submit",
              rules: {
                   referral: { required: true },
                   service: { required: true },
                   client: { required: true },
              },
              submitHandler: function(form) {
                   $(form).ajaxSubmit(form_client_referral_options);
                }
          });
     });
    
    /**
     *
     * rooms post form
     *
     * _description:
     * validate and post room form.
     *
     */


     $('form.form_room').each(function() {
          $(this).validate({event:"submit",
               rules: {
                    description: {
                            required: true
                    }
               },
               messages: {
                    name: 'Preenchimento Necessário'
               },
               submitHandler: function(form) {
                    $(form).ajaxSubmit(form_room_options);
                    
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


     $('form.form_place').each(function() {
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
                    $(form).ajaxSubmit(form_place_options);
                    
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

     $('form.form_service').each(function() {
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
                  $(form).ajaxSubmit(form_service_options);

              }
          });
     });
     
     /**
     *
     * device type  post form
     *
     * _description:
     * validate and post device type form.
     *
     */

     $('form.form_type_device').each(function() {
          $(this).validate({event:"submit",
              rules: {
                label: {
                        required: true
                }
              },
              messages: {
                label: 'Preenchimento Necessário'
              },
              submitHandler: function(form) {
                $(form).ajaxSubmit(form_device_type_options);

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

     $('form.form_device').each(function() {
          $(this).validate({event:"submit",
              rules: {
                brand: {
                        required: true
                },
                model: {
                        required: true
                }
              },
              messages: {
                brand: 'Preenchimento Necessário',
                model: 'Preenchimento Necessário',
              },
              submitHandler: function(form) {
                $(form).ajaxSubmit(form_device_options);

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

     $('form#form_organization').each(function() {
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

     $('form.form_contact').each(function() {
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
     * support form
     *
     * _description:
     * validate and post support form.
     *
     */

     $('form.form_support_ticket').each(function() {
          $(this).validate({event:"submit",
               rules: {
                    contact_name: {
                            required: true
                    },
                    contact_email: {
                            required: true
                    },
                    contact_phone: {
                            required: true
                    },
                    question: {
                            required: true
                    },
                    
                    },
                    messages: {
                      contact_name: 'Preenchimento Necessário',
                      contact_email: 'Preenchimento Necessário',
                      contact_phone: 'Preenchimento Necessário',
                      question: 'Preenchimento Necessário',
                      
                    },
               submitHandler: function(form) {
                 $(form).ajaxSubmit(form_support_ticket_options);
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

     /**
      *
      * user post form
      *
      * _description:
      * post user form, with validate verification
      *
      */

     $('form.user').each(function() {
          $(this).validate({event:"submit",
              rules: {
                   username: { required: true },
                   password: { required: true },
                   pwd_conf: { required: true }
              },
              submitHandler: function(form) {
                   $(form).ajaxSubmit(form_schedule_options);
                }
          });
     });
}
