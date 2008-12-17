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

var schedule_form = {
     success: function(response, request, form) {
          formSuccess();
		  $(form).parents('div:first').hide();
      },

     error: function() {
          formError();
     }
};

var schedule_options = {
    dateFormat: 'yymmdd',
    'onSelect': function(date) {
		year = date.substr(0,4);
		month = date.substr(4,2);
		day = date.substr(6,2);
		formated_date = new Date(year, month, day);

		// clean table
		$('table.schedule tr td.clean').text('');
		$('table.schedule tr').attr('date', day + '/' + month + '/' + year);
		$.getJSON('/schedule/'+date,
			function(json) {
					 jQuery.each(json,  function(i){
						 $('table.schedule tr[time=' + this.time_start +'] td.room').text(this.room);
						 $('table.schedule tr[time=' + this.time_start +'] td.service').text(this.service);
						 $('table.schedule tr[time=' + this.time_start +'] td.client').text(this.client);
						 $('table.schedule tr[time=' + this.time_start +'] td.professional').text(this.professional);
					});
			}
		);
		// change title
        $('p.description').text(day + '/' + month + '/' + year);
		// rewrite date attribute in table clickable lines
		$('table.schedule tr').attr('date', date);
    }
    //    ,firstDay: 1,
}

$(document).ready(function() {
     $('form.schedule').each(function() {
          $(this).validate({event:"submit",
          rules: {
               time_date: {
                      required: true
               }
          },
          messages: {
              name: 'Preenchimento Necessário'
          },
          submitHandler: function(form) {
               $(form).ajaxSubmit(schedule_form);

          }
          });
     });


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









