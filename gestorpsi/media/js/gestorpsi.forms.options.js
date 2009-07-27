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
 * user form options
 */
var form_user_options_mini = {
    beforeSubmit: function() {
        if($("#edit_form div.pwd_mini form input[name=password_mini]").val() != $("#edit_form div.pwd_mini form input[name=password_mini_conf]").val()) {
            $("#edit_form div.pwd_mini div#msg_area").show();
            return false;
        }
    },

    success: function(response, request, form) {
        $(form).parent('div').hide();
        formSuccess('Senha alterada com sucesso');
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
