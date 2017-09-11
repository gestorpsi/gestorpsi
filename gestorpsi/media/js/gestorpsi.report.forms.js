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


$(function() {
    $('form.report_save input[name=submit]').live('click', function() {
        $(this).parents('form.report_save').validate({
            /**
             * validate then submit form to save dashboard view
             */

            event:"submit",
                rules: {
                    label: {
                        required: true
                    }
                },
            messages: {
                label: 'Este campo é obrigatório'
            },
            submitHandler: function(form) {
                $(form).ajaxSubmit({
                    success: function(response, message, form) {
                        $(form).parents('div:first').hide();
                        $('div.saved_successfully b').text(response);
                        $('div.saved_successfully').fadeIn();
                        
                        /**
                         * reload saved report list
                         */
                        updateSavedReports();
                    },
                    error: function() {
                        alert('Erro inserindo registro');
                    }
                });
            }
        });
    });

});
