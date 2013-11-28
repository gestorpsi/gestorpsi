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

var occupied_css_class = 'occup';

$(document).ready(function() {

    // filters menu. toggle menu list options
    $('div.schedule a.option.toggle').unbind().click(function() {
        var filter = $($(this).attr('display'));
        $('div.schedule div.filter').not(filter).hide();
        $(filter).toggle();
    });

    // close all window filter when click out
    $(document).click(function(e) { 
        if ( e.target.id != 'schedule_filter_room' && e.target.id != 'schedule_filter_place' && e.target.id != 'schedule_filter_service' && e.target.id != 'schedule_filter_professional' ){ 
            $('div.schedule div.filter').hide();
        }
    });
    

    /**
     * occurrences filter
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
                    $('table.weekly div.place_ ' + $(this).attr('uuid')).show();
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
                        $('table.weekly div.place_ ' + $(this).attr('uuid')).hide();
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
                        // weekly
                        $('table.weekly div.' + el.attr('type') + '_' + el.attr('uuid')).hide();
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
                        $('table.weekly div.' + el.attr('type') + '_' + el.attr('uuid')).each(function() {
                                    $(this).hide();
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
                        // weekly
                        $('table.weekly div.' + el.attr('type') + '_' + el.attr('uuid')).show();
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
                        // weekly
                        $('table.weekly div.' + el.attr('type') + '_' + el.attr('uuid')).each(function() {
                                $(this).show();
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
                    // weekly
                    //$('table.weekly div.'+el.attr('type')+'_' + el.attr('uuid')).hide();
                } else {
                    // daily
                    $('table.schedule_results.daily tr ['+el.attr('type')+'=' + el.attr('uuid') + ']').not('.already_hided').show();
                    // weekly
                    //$('table.weekly div.'+el.attr('type')+'_' + el.attr('uuid')).show();
                }
            }
        });
    });

});
