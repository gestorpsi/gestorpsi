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

$(document).ready(function() {

    // switch time range select field
    $('div.schedule div.form select[name=repeat] option').click(function() {
        $(this).parents('label').siblings('.repeat').hide();
        $(this).parents('label').siblings('.' + $(this).attr('repeat')).show();
    });

    // open form
    $('div.schedule table.schedule  tr').click(function() {
		// set date
		var date = $(this).attr('date');
		var time = $(this).attr('time');
		$('div.schedule div.form input[name=time_date]').val(date);
		$('div.schedule div.form').show();
    });

});









