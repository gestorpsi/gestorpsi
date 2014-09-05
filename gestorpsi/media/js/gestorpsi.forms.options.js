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
 * mini forms to quick add options
 */

var form_mini_options = {
     success: function(response, message, form) {

                if (response == 'True') {
                    alert('Já existe uma organização com esse nome, tente outro por favor.');

                } else {
                    var id = response.split("|")[1]
                    var name = response.split("|")[2]

                    // add <option> to asm select - referral form new 

                    // add <option> to asmselect select box
                    $.form_mini_link.parents('fieldset').children('label').children('select.asmSelect:first').append('<option value=' + id + ' disabled="disabled">' + name + '</option>');

                    // add <option> to asm select box
                    $.form_mini_link.parents('label').children('select.asm:first').append('<option value=' + id + ' selected="selected">' + name + '</option>');

                    // add <option> to real multiselect
                    $.form_mini_link.parents('fieldset').children('label').children('select.multiple').append('<option value=' + id + ' selected="selected">' + name + '</option>');

                    // append it to list
                    $.form_mini_link.parents('fieldset').children('label').children('ol').append('<li style="display: list-item;" class="asmListItem"><span class="asmListItemLabel">' + name +'</span><a class="asmListItemRemove dyn_added">remove</a></li>');

                    // clean form and hide it
                    $('form fieldset label input[name="label"]').val('');
                    $('div.form_mini').hide();
                }
          },
     error: function() {
          alert('Erro inserindo registro');
     }
}; 
