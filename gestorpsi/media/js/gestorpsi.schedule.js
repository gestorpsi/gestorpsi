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
var schedule_options = {
    dateFormat: 'dd/mm/yy',
    'onSelect': function(date) {
		// change title
        $('p.description').text(date);
		// rewrite date attribute in table clickable lines
		$('table.schedule tr').attr('date', date);
    }
    //    ,firstDay: 1,
}

$(document).ready(function() {

	$("div.schedule_month").datepicker(schedule_options);

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
		// set clicked date
		$('div.schedule div.form input[name=time_date]').val(date);
		// set clicked time
		$('div.schedule div.form select[name=hour] option').each(function() {  if($(this).val() == time) { $(this).attr('selected', 'selected'); } });
		//display form
		$('div.schedule div.form').show();
    });
});









