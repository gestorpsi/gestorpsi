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
    dateFormat: 'yymmdd',
    'onSelect': function(date) {
        $("div#mini_calendar").hide();
        return updateGrid('/schedule/occurrences/' + date.substr(0,4) + '/' + date.substr(4,2) + '/' + date.substr(6,2) + '/');
    }
}

var dialog_options = {
    modal: true,
    overlay: {
        background: "url(/media/img/transp75.png) repeat"
    },
    autoOpen: false,
    height: "350px",
    width: "500px"
    
}

var occupied_css_class = 'occup';

var increment_end_time = '3600'; // in seconds

/** 
* daily and events
* get data from json vand put on the schedule daily grid
*/

function updateGrid(url) {

    $('table.schedule_results.daily tr td.clean').attr('class','clean'); // remove class from lastest event
    $('table.schedule_results.daily tr td.clean a.booked').remove(); // remove booked events
    $('table.schedule_results.daily tr td.clean').attr('rowspan', '1'); // reset rowspans
    
    // hide elements if some filter is activated BEFORE data loaded
    // places and rooms (cols)
    $('div.filter.incols a.filter_by').each(function() {
        var el = $(this);
        if(el.attr('status') == 'on' && el.attr('type')) {
            $('table.schedule_results.daily tr [room=' + el.attr('uuid') + ']').show(); // display hided td's by rowspans
        }
    });
    
    $('table.schedule_results.daily tr td.clean a.book').show(); // reset grid to free slots on all
    $('div.schedule_events table.events tr:not(:first)').remove(); // clean events

    $.getJSON(url, function(json) {
        $('div.schedule span.date_selected').text(json['util']['str_date']); // switch selected date
        $('table.schedule_results.daily tr td.clean a.book').each(function() { // update date ins url
            hour = $(this).parent('td').parent('tr').attr('hour');
            room = $(this).parent('td').attr('room');
            $(this).attr('href', '#');
            $(this).attr('date', json['util']['date']);
            $(this).attr('hour', hour);
            $(this).attr('room_id', room);
            //$(this).attr('href', '/schedule/events/add/?dtstart=' + json['util']['date'] + 'T' + hour + '&room='+ room);
            $(this).attr('title', json['util']['str_date']);
        });
        $('div.schedule a.prev_day').attr('href','/schedule/occurrences/'+json['util']['prev_day']+'/');
        $('div.schedule a.next_day').attr('href','/schedule/occurrences/'+json['util']['next_day']+'/');
        jQuery.each(json,  function(){
            if(this.start_time) {
                
                var str_client = '';
                var str_client_inline = ''; 
                var str_professional = ''; 
                var str_professional_inline = ''; 
                var str_service = '';
                var str_service_inline = '';
                
                /** 
                 * start daily occurrence
                 */
                
                var col = $('table.schedule_results.daily tr[hour=' + this.start_time +'] td[room='+this.room+']');
                
                /** 
                 * start occurrence event
                 */
                
                event_line = '<tr><td>'+this.room_name+'</td><td><span class="time">' + this.start_time.substr(0, (this.start_time.length-3)) + '</span></td><td><div></div></td></tr>';
                $('div.schedule_events table.events tr:last').after(event_line);
                event = $('div.schedule_events table.events tr:last');
                
                //append client list
                jQuery.each(this.client,  function(){
                    str_client = str_client + this.name + "<br />";
                    str_client_inline = str_client_inline + this.name + ", ";
                });
                str_client_inline = str_client_inline.substr(0, (str_client_inline.length-2))
                
                //append professional list
                jQuery.each(this.professional,  function(){
                    str_professional = str_professional + this.name + "<br />" ;
                    str_professional_inline = str_professional_inline + this.name + ", " ;
                    col.addClass('professional_' + this.id); // professionals in cell
                    event.addClass('professional_' + this.id); // professionals in events
                });
                str_professional_inline = str_professional_inline.substr(0, (str_professional_inline.length-2))
                
                //append service
                str_service = '>>' + this.service + '<br />';
                str_service_inline = ' >> ' + this.service;
                
                label = str_client + str_service + str_professional;
                label_inline = str_client_inline + str_service_inline + '(' + str_professional_inline + ')';

                /**
                 * populate daily view
                 */
                
                col.addClass('clean'); // required
                col.addClass('color' + this.css_color_class); // service color
                col.addClass('service_' + this.service_id); // service from cell
                
                // for occurrences greater than half-hour, change table rowspan
                if (this.rowspan > 1) {
                    // we need to remove next TD's if last rowspan is greater than 1
                    next_tds = $('table.schedule_results.daily tr[hour=' + this.start_time +']').nextAll().find('td[room='+this.room+']').slice(0, (parseInt(this.rowspan)-1));
                    next_tds.hide();
                    next_tds.addClass('already_hided');
                    // increase rowspan size 
                    $('table.schedule_results.daily tr[hour=' + this.start_time +'] td[room='+this.room+']').attr('rowspan', this.rowspan);
                }

                $('table.schedule_results.daily tr[hour=' + this.start_time +'] td[room='+this.room+'] a.book').hide(); // hide free slot 
                $('table.schedule_results.daily tr[hour=' + this.start_time +'] td[room='+this.room+'] a.book').after('<a title="'+json['util']['str_date']+'" occurrence="' + this.id + '" class="booked">' + label + '</a>'); // show booked event
                

                /**
                 * populate events view
                 */
                
                event.children('td').children('div').addClass('color' + this.css_color_class); // service color
                event.addClass('room_' + this.room); // service color
                event.addClass('place_' + this.place); // service color
                event.addClass('service_' + this.service_id); // service from cell
                $(event).children('td').children('div').html('<a title="'+json['util']['str_date']+'" occurrence="' + this.id + '" class="booked">' + label_inline + '</a>');
                
                $('table.zebra tr:odd').addClass('zebra_0');
                $('table.zebra tr:even').addClass('zebra_1');
                }
            });
            
            if($('div.schedule_events table.events tr td:first').size() < 1) {
                $('div.schedule_events table.events div.msg_area').show();
                $('div.schedule_events table.events tr').hide();
            } else {
                $('div.schedule_events table.events div.msg_area').hide();
                $('div.schedule_events table.events tr').show();
            }
            
            // hide elements if some filter is activated AFTER data loaded
            var count = 0;
            var class_name = '';
            
            // service and professional
            $('div.filter:not(.incols) a.filter_by').each(function() {
                var el = $(this);
                if(el.attr('status') == 'off' && el.attr('type')) {
                    class_name = el.attr('type') + '_' + el.attr('uuid');
                    $('table.schedule_results.daily tr td.'+class_name + ' a.booked').hide();
                    $('table.schedule_results.daily tr td.'+class_name).addClass(occupied_css_class);
                    $('table.schedule_results.events tr.'+class_name).hide();
                }
            });
        }
    );
    
    /**
     * bind dialog box
     */

    $('table.schedule_results a.booked').unbind().click(function() {
        $.getJSON('/schedule/occurrence/abstract/'+ $(this).attr('occurrence') +'/', function(json) {
            
            var str_client = ''; var str_professional = '';
            //append client list
            jQuery.each(json.client,  function(){
            str_client = str_client + this.name + ' ' +this.phone+ '<br />' ;
            });

            //append professional list
            jQuery.each(json.professional,  function(){
                str_professional = str_professional + this.name + ' ' +this.phone+ '<br />' ;
            });
            
            $('div#dialog h1[key=date]').text(json['date']);
            $('div#dialog div[key=room]').text(json['room']);
            $('div#dialog div[key=service]').text(json['service']);
            $('div#dialog div[key=client]').html(str_client);
            $('div#dialog div[key=professional]').html(str_professional);
            $('div#dialog a[key=edit_link]').attr('href','/schedule/events/' + json['event_id'] + '/' + json['id'] + '/');
            $('div#dialog a[key=edit_link]').attr('title', json['client'][0].name);
            $('div#edit_form form.schedule .sidebar .bg_blue input[name=day_clicked]').val(json['day']);
        });
        $('div#dialog').dialog('open');
    });
    
    return false;
}

/**
 * load data from inserted event (referral) with occurrences
 */

function updateScheduleReferralDetails(url) {
    
    $('.schedule #edit_form div#schedule_occurrence_list table .clean').html(''); // clean old data
    
    $.getJSON(url, function(json) {
        
        var str_professional_inline = ''; 
        var str_client_inline = ''; 
        var description = ''; 
        var tableTR = '';
    
        /**
         * Referral infos
         */

        str_client_inline = personInLine(json['client']);
        str_professional_inline = personInLine(json['professional']);
        
        $('.schedule #edit_form h2.title_schedule, ul.opened_tabs li div a:first').text(str_client_inline); // set title (h2 and opened tab)
        $('.schedule #edit_form p.description').text(json['service'] + ' - ' + str_professional_inline); // set description
        
        /**
         * Occurrences list
         */
                
        jQuery.each(json['occurrences'],  function(){
            tableTR = tableTR + '<tr><td class="title">' + this.date + ' ' + this.start_time + ' - ' + this.end_time + '<br>' + this.place + ' - ' + this.room + '</td></tr>';
        });

        $('.schedule #edit_form div#schedule_occurrence_list div.occurrence_list table tbody').html(tableTR);
        
        $('table.zebra tr:odd').addClass('zebra_0');
        $('table.zebra tr:even').addClass('zebra_1');

        }
    );
  
    
    return false;
}

/** 
 * schedule form
 * bind form functions
 */

function bindScheduleForm() {
    // bind links in table
    $('div.schedule table.schedule_results a.book').click(function() {
        var link = $(this);

        year = link.attr('date').substring(0,4);
        month = link.attr('date').substring(5,7);
        day = link.attr('date').substring(8,11);
        hour = link.attr('hour').substring(0,2);
        minutes = link.attr('hour').substring(3,5);

        var zero_hour = new Date(year, month, day, 0, 0, 0);
        var due = new Date(year, month, day, hour, minutes);
        var start_time_delta = (due - zero_hour) / 1000;
        var end_time_delta = (parseInt(start_time_delta) + parseInt(increment_end_time));

        // set initial data in add form
        $('div.schedule #form select[name=day_month] option[value=' + parseFloat(month) + ']').attr('selected', 'selected');
        $('div.schedule #form select[name=day_day] option[value=' + parseFloat(day) + ']').attr('selected', 'selected');
        $('div.schedule #form select[name=day_year] option[value=' + parseInt(year) + ']').attr('selected', 'selected');
        $('div.schedule #form select[name=start_time_delta] option[value=' + start_time_delta + ']').attr('selected', 'selected');
        $('div.schedule #form select[name=end_time_delta] option[value=' + end_time_delta + ']').attr('selected', 'selected');
        $('div.schedule #form select[name=room] option[value=' + link.attr('room_id') + ']').attr('selected', 'selected');
        $('div.schedule #form input[name=tabtitle]').val(link.attr('title'));
        $('div#form form.schedule .sidebar input[name=day_clicked]').val(year + '/' + month + '/' + day);
    
    });

    // if start time is changed, increment 'increment_end_time' value to end time
    $('div.schedule select[name=start_time_delta] option').click(function() {
        var option = $(this);
        var end_time = (parseInt(increment_end_time) + parseInt(option.attr('value')));

        $(this).parents('fieldset').children('label').children('select[name=end_time_delta]').children('option').attr('selected','');
        $(this).parents('fieldset').children('label').children('select[name=end_time_delta]').children('option[value=' + end_time + ']').attr('selected','selected');
    });

    // get clients json list and draw flexbox
    $('div.schedule div#form div#fb_client').flexbox('/client/organization_clients/',{
         allowInput: true,  
         paging: true,  
         maxVisibleRows: 12,
         width: 385,
         autoCompleteFirstMatch: true,
         onSelect: function() {  
            $.getJSON('/referral/client/' + this.getAttribute('hiddenValue') + '/', function(json) {
                $('#form select[name=referral]').html('');
                var line = '';
                var str_professional_inline = '';
                jQuery.each(json,  function(){
                    str_professional_inline = '';
                    //append professional list
                    jQuery.each(this.professional,  function(){
                        str_professional_inline = str_professional_inline + this.name + ", " ;
                    });
                    str_professional_inline = str_professional_inline.substr(0, (str_professional_inline.length-2))
                
                    line = line + '<option value="' + this.id + '">' + this.service + ' (' + str_professional_inline + ')</option>';
                }); 
                $('#form select[name=referral]').html(line); // rebuild referral select
            });
            $('#form div.client_referrals').show();
            $('#form input[name=tabtitle]').val(this.value); // set title, to use in TAB
        }
    });

}

/**
 * schedule:
 * bind all schedule functions
 */

function bindSchedule() {
    // dialog box
    $('div#dialog').dialog(dialog_options);
    
    // load today daily occurrences and mini-calendar
    $('div.schedule table.schedule_results').unbind().ready(function() {
        $("div#mini_calendar").datepicker(schedule_options);
        updateGrid('/schedule/occurrences/');
    });
   
    // open mini-calendar
    $('a#calendar_link').unbind().click(function() {
        $("div#mini_calendar").toggle();
    });

    // bind click daily occurrences
    $('div.schedule a.json_ocorrences').unbind().click(function() {
        return updateGrid($(this).attr('href'));
    });
    
    // filters menu. toggle menu list options
    $('div.schedule a.option.toggle').unbind().click(function() {
        var filter = $($(this).attr('display'));
        $('div.schedule div.filter').not(filter).hide();
        $(filter).toggle();
    });
    
    
    /**
     * filter links:
     * Re-draw the filter menu if item clicked
     */

    $('div.schedule a.filter_by').unbind().click(function() {
        var all_selected = $(this).parents('table').children('tbody').children('tr').children('td.all').children('a');
        var all = $(this).parents('table').children('tbody').children('tr').children('td').children('a');
        var all_visible = $(this).parents('table').children('tbody').children('tr:visible').children('td').not('.all').children('a');
        var visible_turned_on = $(this).parents('table').children('tbody').children('tr:visible').children('td').not('.all').children('a[status=on]');
        
        //var col = 'div.schedule table.schedule_results tr td.' + $(this).attr('type') + '_' + $(this).attr('uuid');
        var img = $(this).parents('table').children('tbody').children('tr').children('td').children('a').children('img');
        
        if ($(this).hasClass('all')) {
            // buttom all
            if(all_selected.attr('status') == 'off') {
                all.children('img').attr('src','/media/img/chk.png');
                all.attr('status','on');
            } else {
                all.children('img').attr('src','/media/img/chk_off.png');
                all.attr('status','off');
            }
        } else {
            // show and hide
            
            // it's the first click. 'all itens' button still selected yet. let's hide all, and show only clicked
            if (all_selected.attr('status') == 'on') {
                img.attr('src','/media/img/chk_off.png');
                $(this).children('img').attr('src','/media/img/chk.png');
                all.attr('status','off');
                $(this).attr('status','on');
            } else {
                // single toggle
                if($(this).attr('status') == 'on') {
                    $(this).attr('status','off');
                    $(this).children('img').attr('src','/media/img/chk_off.png');
                } else {
                    $(this).attr('status','on');
                    $(this).children('img').attr('src','/media/img/chk.png');
                    if(($(all_visible).size() == (parseInt($(visible_turned_on).size()) + 1))) {
                        // turn on all buttom if all itens are selected
                        all_selected.attr('status','on');
                        all_selected.children('img').attr('src','/media/img/chk.png');
                    }
                }
            }
        }
        
        
        /**
         * filter links:
         * filter rooms when if select place in filter menu
         */
        
        if($(this).attr('type') == 'place') {
            $('div.schedule div.place a.filter_by').each(function() {
                if($(this).hasClass('all') && $(this).attr('status') == 'on') {
                    // turn on ALL rooms
                    $('div.schedule div.room tr.room_itens').show();
                    $('div.schedule div.room tr td.all a.filter_by').attr('status','on');
                    $('div.schedule div.room tr td.all a.filter_by').children('img').attr('src','/media/img/chk.png');
                 } else {
                    if($(this).attr('status') == 'on') {
                        // turn on rooms from this place
                        $('div.schedule div.room tr.room_itens[place='+$(this).attr('uuid')+'] a.filter_by').attr('status','on');
                        $('div.schedule div.room tr.room_itens[place='+$(this).attr('uuid')+'] a.filter_by img').attr('src','/media/img/chk.png');
                        $('div.schedule div.room tr.room_itens[place='+$(this).attr('uuid')+']').show();
                    } else {
                        // turn off rooms from this place
                        $('div.schedule div.room tr.room_itens[place='+$(this).attr('uuid')+'] a.filter_by').attr('status','off');
                        $('div.schedule div.room tr.room_itens[place='+$(this).attr('uuid')+'] a.filter_by img').attr('src','/media/img/chk_off.png');
                        $('div.schedule div.room tr.room_itens[place='+$(this).attr('uuid')+']').hide();
                    }
                }
            });
        }
        
        
        /**
         * daily and events view:
         * read the filter menu status, and rebuild the data grid (service and professional)
         */
        
        var count = 0;
        var class_name = '';
        $('table.schedule_results.daily tr td').attr('norewrite','false');
        $('table.schedule_results.events tr').attr('norewrite','false');

        $(this).parents('div').children('table').children('tbody').children('tr').children('td').children('a').each(function() {
            var el = $(this);
            if(el.attr('status') && el.attr('type') && el.attr('uuid')) {
                class_name = el.attr('type') + '_' + el.attr('uuid');
                if(el.attr('status') == 'off') { // switch off
                    if(el.attr('type') == 'service') { // service can overwrite other filters ..
                        // daily
                        $('table.schedule_results.daily tr td.' + class_name + ' a.booked').hide();
                        $('table.schedule_results.daily tr td.' + class_name).addClass(occupied_css_class);
                        $('table.schedule_results.daily tr td.' + class_name).attr('locked', 'on');
                        // events
                        $('table.schedule_results.events tr.' + el.attr('type') + '_' + el.attr('uuid')).hide();
                        $('table.schedule_results.events tr.' + el.attr('type') + '_' + el.attr('uuid')).attr('locked', 'on');
                    } else {
                        // daily
                        $('table.schedule_results.daily tr td.' + class_name).each(function() {
                                if($(this).attr('locked') != 'on' && $(this).attr('norewrite') != 'true') {
                                    $(this).children('a.booked').hide();
                                    $(this).addClass(occupied_css_class);
                                }
                            });
                        // events
                        $('table.schedule_results.events tr.' + el.attr('type') + '_' + el.attr('uuid')).each(function() {
                                if($(this).attr('locked') != 'on' && $(this).attr('norewrite') != 'true') {
                                    $(this).hide();
                                }
                            });
                    }
                } else { // switch on
                    if(el.attr('type') == 'service') { // service can overwrite other filters ..
                        // daily
                        $('table.schedule_results.daily tr td.' + class_name + ' a.booked').show();
                        $('table.schedule_results.daily tr td.' + class_name).removeClass(occupied_css_class);
                        $('table.schedule_results.daily tr td.' + class_name).attr('locked', 'off');
                        // events
                        $('table.schedule_results.events tr.' + el.attr('type') + '_' + el.attr('uuid')).show();
                        $('table.schedule_results.events tr.' + el.attr('type') + '_' + el.attr('uuid')).attr('locked', 'off');
                    } else {
                        // daily
                        $('table.schedule_results.daily tr td.' + class_name).each(function() {
                            if($(this).attr('locked') != 'on') {
                                $(this).children('a.booked').show();
                                $(this).removeClass(occupied_css_class);
                                $(this).attr('norewrite','true');
                            }
                        });
                        // events
                        $('table.schedule_results.events tr.' + el.attr('type') + '_' + el.attr('uuid')).each(function() {
                            if($(this).attr('locked') != 'on') {
                                $(this).show();
                                $(this).attr('norewrite','true');
                            }
                        });
                    }
                }
            }
        });
        
        
        /**
         *  daily view: 
         *  read rooms and places filter menu, and hide (or show) cols
         */
     
        $('div.room tr.room_itens a.filter_by').each(function() {
            var el = $(this);
            if(el.attr('status') && el.attr('type') && el.attr('uuid')) {
                if(el.attr('status') == 'off') { // switch off
                    // daily
                    $('table.schedule_results.daily tr ['+el.attr('type')+'=' + el.attr('uuid') + ']').hide();
                    // events
                    $('table.schedule_results.events tr.'+el.attr('type')+'_' + el.attr('uuid')).hide();
                } else {
                    // daily
                    $('table.schedule_results.daily tr ['+el.attr('type')+'=' + el.attr('uuid') + ']').not('.already_hided').show();
                }
            }
        });
        
    
        
    });
    
    bindScheduleForm();

    
}
