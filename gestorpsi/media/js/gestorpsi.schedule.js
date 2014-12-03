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
        return updateGrid('/schedule/occurrences/' + date.substr(0,4) + '/' + date.substr(4,2) + '/' + date.substr(6,2) + '/place/' + $('input[name="current_place_id"]').val() );
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

function findReserve(occurrences, param){

    var str_index = occurrences.search(param);

    if(str_index!=-1){
        return true;
    }else{
        return false;
    }
}

/** 
* daily and events
* get data from json vand put on the schedule daily grid
*/

function updateGrid(url) {

    $('table.schedule_results.daily tr td.clean').attr('class','clean'); // remove class from lastest event
    $('table.schedule_results.daily tr td.clean a.booked').remove(); // remove booked events
    $('table.schedule_results.daily tr td.clean').attr('rowspan', '1'); // reset rowspans
    $('table.schedule_results.daily tr td.clean').attr('style', ''); // reset columns style 
    
    
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
        $('div.schedule div#schedule_header p.description span#occurrences_total').text(json['util']['occurrences_total']); // total of occurrences
        $('table.schedule_results.daily tr td.clean a.book').each(function() { // update date ins url
            var hour = $(this).parent('td').parent('tr').attr('hour');
            var referral = $('input[name=referral]').val()
            var client = $('input[name=client]').val()
            var room = $(this).parent('td').attr('room');
            
            if(referral && client) {
                href = '/client/schedule/add/?dtstart=' + json['util']['date'] + 'T' + hour + '&room='+ room + '&referral=' + referral + '&client=' + client;
            } else {
                href = '/schedule/events/add/?dtstart=' + json['util']['date'] + 'T' + hour + '&room='+ room;
            }
            $(this).attr('href',  href);
        });

        // - - CHECKED 
        
        /*$('div.schedule a.prev_day').attr('href','/schedule/occurrences/'+json['util']['prev_day']+'/');*/
        /*$('div.schedule a.next_day').attr('href','/schedule/occurrences/'+json['util']['next_day']+'/');*/
        $('div.schedule a.next_day').attr('href','/schedule/occurrences/'+json['util']['next_day']+'/place/'+json['util']['place']+'/');
        $('div.schedule a.prev_day').attr('href','/schedule/occurrences/'+json['util']['prev_day']+'/place/'+json['util']['place']+'/');
        jQuery.each(json,  function(){
    
            $('table.zebra tr:odd').addClass('zebra_0');
            $('table.zebra tr:even').addClass('zebra_1');
            if(this.start_time) {

                var str_client = '';
                var str_client_inline = ''; 
                var str_professional = ''; 
                var str_professional_inline = ''; 
                var str_service = '';
                var str_service_inline = '';
                var str_device_inline = '';
                var label = '';
                var label_inline = '';
                
                
                /** 
                 * start daily occurrence
                 */
                
                var col = $('table.schedule_results.daily tr[hour="' + this.start_time + '"] td[room="' + this.room + '"]');
                
                /** 
                 * start occurrence event
                 */
                
                event_line = '<tr><td>'+this.room_name+'</td><td><span class="time">' + this.start_time.substr(0, (this.start_time.length-3)) + '&nbsp;' + this.end_time.substr(0, (this.end_time.length-3)) + '</span></td><td><div></div></td></tr>';
                $('div.schedule_events table.events tr:last').after(event_line);
                event = $('div.schedule_events table.events tr:last');
                
                /**
                 * append rows titles if NOT in client view
                 */
                
                if(!$('input[name=referral]').val() && !$('input[name=client]').val()) {
                
                    //append group name or client list
                    if(this.group != '') {
                        str_client = this.group + "<br />";
                        str_client_inline = this.group;
                    } else {
                        jQuery.each(this.client,  function(){
                            str_client += this.name + "<br />";
                            str_client_inline += this.name + ", ";
                        });
                        str_client_inline = str_client_inline.substr(0, (str_client_inline.length-2));
                    }
                    
                    
                    //append professional list
                    jQuery.each(this.professional,  function(){
                        str_professional += this.name + "<br />" ;
                        str_professional_inline += this.name + ", " ;
                        col.addClass('professional_' + this.id); // professionals in cell
                        event.addClass('professional_' + this.id); // professionals in events
                    });
                    str_professional_inline = str_professional_inline.substr(0, (str_professional_inline.length-2))
                    
                    //append service
                    str_service = '>>' + this.service + '<br />';
                    str_service_inline = ' >> ' + this.service;
                    
                    label = str_client + str_service + str_professional;
                    label_inline = str_client_inline + str_service_inline;
                    
                    label_inline += (str_professional_inline) ? ' (' + str_professional_inline + ')' : '';
                    
                                        
                    //append device list
                    jQuery.each(this.device,  function(){
                        str_device_inline += this.name + ", " ;
                        col.addClass('device_' + this.id); // device in cell
                        event.addClass('device_' + this.id); // devices in events
                    });
                    str_device_inline = str_device_inline.substr(0, (str_device_inline.length-2))
                    if(str_device_inline) {
                        label += str_device_inline;
                        label_inline += ' >> ' + str_device_inline;
                    }
                    
                    
                } else {
                    label = '<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reservado';
                }

                /**
                 * populate daily view
                 */

                col.addClass('clean'); // required
                col.addClass('tag'); // required
                col.css('background-color', '#' + this.color); // service color
                col.addClass('service_' + this.service_id); // service from cell
                
                // for occurrences greater than half-hour, change table rowspan
                if (this.rowspan > 1) {
                    // we need to remove next TD's if last rowspan is greater than 1
                    next_tds = $('table.schedule_results.daily tr[hour="' + this.start_time + '"]').nextAll().find('td[room="' + this.room + '"]').slice(0, (parseInt(this.rowspan)-1));
                    next_tds.hide();
                    next_tds.addClass('already_hided');
                    // increase rowspan size 
                    $('table.schedule_results.daily tr[hour="' + this.start_time +'"] td[room="' + this.room + '"]').attr('rowspan', this.rowspan);
                }

                $('table.schedule_results.daily tr[hour="' + this.start_time +'"] td[room="' + this.room + '"] a.book').hide(); // hide free slot 
                
                url = (this.group != '')?'/schedule/events/group/' +  this.group_id + '/occurrence/' + this.id + '/':'/schedule/events/' + this.id + '/confirmation/';
                
                if ($('input[name=restrict_schedule]').val() == "True") {
                    label = "Reservado";
                    label_inline = "Reservado";
                }

                if($('input[name=occurrences]').val() && findReserve($('input[name=occurrences]').val(), this.start_time.slice(0, 5) + " True")){
                    url = '/schedule/events/add/?dtstart=' + json['util']['date'] + 'T' + this.start_time + '&room='+ this.room;
                    $('table.schedule_results.daily tr[hour="' + this.start_time + '"] td[room="' + this.room + '"] a.book').after('<a title="'+json['util']['str_date']+'" href="' + url + '" class="booked" style="color:#'+this.font_color+'">' + label + '</a>'); // show booked event
                }
                else if(!$('input[name=referral]').val() && !$('input[name=client]').val()) {

                    $('table.schedule_results.daily tr[hour="' + this.start_time + '"] td[room="' + this.room + '"] a.book').after('<a title="'+json['util']['str_date']+'" href="' + url + '" class="booked" style="color:#'+this.font_color+'">' + label + '</a>'); // show booked event
                } else {
                    $('table.schedule_results.daily tr[hour="' + this.start_time +'"] td[room="' + this.room + '"] a.book').after('<a class="booked" style="color:#'+this.font_color+'">' + label + '</a>'); // show booked event in Client View
                }
                

                /**
                 * populate events view
                 */
                
                event.children('td').children('div').css('background-color', '#' + this.color); // service color
                event.children('td').children('div').addClass('tag'); // tag styles
                event.addClass('room_' + this.room); // service color
                event.addClass('place_' + this.place); // service color
                event.addClass('service_' + this.service_id); // service from cell
                $(event).children('td').children('div').html('<a title="'+json['util']['str_date']+'" href="' + url + '" class="booked" style="color:#'+this.font_color+'">' + label_inline + '</a>');
                }
            });
            
            if($('div.schedule_events table.events tr td:first').size() < 1) {
                $('div.schedule_events div.msg_area').show();
                $('div.schedule_events table.events tr').hide();
            } else {
                $('div.schedule_events div.msg_area').hide();
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
    
    return false;
}

/** 
 * schedule form
 * bind form functions
 */

$(function() {

    // if start time is changed, increment 'increment_end_time' value to end time
    $('div.schedule select[name=start_time_delta] option, div.schedule select[name=start_time1] option').click(function() {
        var option = $(this);
        var end_time = (parseInt(increment_end_time) + parseInt(option.attr('value')));

        $(this).parents('fieldset').children('label').children('select[name=end_time_delta]').children('option').attr('selected','');
        $(this).parents('fieldset').children('label').children('select[name=end_time_delta]').children('option[value=' + end_time + ']').attr('selected','selected');
        
        //$(this).parents('fieldset').children('label').children('select[name=end_time_delta]').children('option').attr('disabled',false)
        $(this).parents('fieldset').children('label').children('select[name=end_time_delta]').children('option').show();

        $(this).parents('fieldset').children('label').children('select[name=end_time_delta]').children('option').each(function(){
            if (parseInt($(this).val()) <= parseInt(option.val()) ){
                $(this).hide();
            }  
        });
    });

    // get clients json list and draw flexbox
    $('div.schedule div#form div#fb_client').html('')
    $('div.schedule div#form div#fb_client').flexbox('/client/organization_clients/',{
         allowInput: true,  
         paging: true,  
         maxVisibleRows: 12,
         width: 385,
         queryDelay: 500,
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
                        str_professional_inline += this.name + ", " ;
                    });
                    str_professional_inline = str_professional_inline.substr(0, (str_professional_inline.length-2))
             
                    // if service is on 
                    if (this.status == "01"){ 
                            if ( str_professional_inline != ''){ 
                                line = line + '<option value="' + this.id + '">' + this.service + ' (' + str_professional_inline + ')</option>';
                            } else {
                                line = line + '<option value="' + this.id + '">' + this.service + '</option>';
                            }
                    } 
                }); 
                $('#form select[name=referral]').html(line); // rebuild referral select
            });
            $('#form div.client_referrals').show();
            $('#form input[name=tabtitle]').val(this.value); // set title, to use in TAB
        }
    });

        /**
         *  show devices of the room when select or change to other room
         */

        $("form.schedule div.main_area select#id_room").change(function(){ 
        $('select[name=device] option').remove();
        if (this.value != ''){
            $.getJSON("/device/" + $(this).attr("value") + "/listdevice/", function(json) {
                jQuery.each(json,  function(){
                    $('select[name=device]').append(new Option(this.name, this.id));
                });
            });
        }
    });

});

/**
 * schedule:
 * bind all schedule functions
 */

$('div.schedule').ready(function() {

    // load today daily occurrences and mini-calendar
    $('div.schedule table.schedule_results').unbind().ready(function() {
        $("div#mini_calendar").datepicker(schedule_options);
        updateGrid('/schedule/occurrences/');
    });

    // bind click daily occurrences
    $('div.schedule a.json_ocorrences').unbind().click(function() {
        return updateGrid($(this).attr('href'));
    });
    
});
