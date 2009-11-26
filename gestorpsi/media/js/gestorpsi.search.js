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

    /**
     * contact quick filter
     */

    $('div#search_header.contact_search table#letter_menu tr td a, div#search_header.contact_search a#letter_back, div#search_header.contact_search a#letter_fwd').click(function() {
        updateContact('/contact/initial/' + $(this).attr('initial') + '/page1/', false, 'contact/initial/'+$(this).attr('initial'));
    });

    /**
    * contact quick search
    */

    $('div#search_header.contact_search a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateContact('/contact/filter/' + $(this).prev().val() + '/page1/', false, 'contact/filter/' + $(this).prev().val()) : updateContact('/contact/page1');
    });

    /**
     * contact clean up
     */

    $('div#search_header.contact_search a#cleanup').click(function() {
        updateContact('/contact/page1');
    });

    /**
     * client quick filter active
     */

    $('div#search_header.client_search.active table#letter_menu tr td a, div#search_header.client_search.active a#letter_back, div#search_header.client_search.active a#letter_fwd').click(function() {
        updateClient('/client/initial/' + $(this).attr('initial') + '/page1/', false, 'client/initial/'+$(this).attr('initial'));
    });

    /**
     * client quick filter deactive
     */

    $('div#search_header.client_search.deactive table#letter_menu tr td a, div#search_header.client_search.deactive a#letter_back, div#search_header.client_search.deactive a#letter_fwd').click(function() {
        updateClient('/client/initial/' + $(this).attr('initial') + '/page1/deactive/', true, 'client/initial/'+$(this).attr('initial'));
    });

    /**
    * client quick search active
    */

    $('div#search_header.client_search.active a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateClient('/client/filter/' + $(this).prev().val() + '/page1/', false, 'client/filter/'+$(this).prev().val()) : updateClient('/client/page1');
    });

    /**
    * client quick search deactive
    */

    $('div#search_header.client_search.deactive a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateClient('/client/filter/' + $(this).prev().val() + '/page1/deactive/', true, 'client/filter/'+$(this).prev().val()) : updateClient('/client/page1/deactive/', true);
    });

    /**
     * client clean up active
     */

    $('div#search_header.client_search.active a#cleanup').click(function() {
        updateClient('/client/page1');
    });

    /**
     * client clean up deactive
     */

    $('div#search_header.client_search.deactive a#cleanup').click(function() {
        updateClient('/client/page1/deactive/', true);
    });

    /**
     * employee quick filter active
     */

    $('div#search_header.employee_search.active table#letter_menu tr td a, div#search_header.employee_search.active a#letter_back, div#search_header.employee_search.active a#letter_fwd').click(function() {
        updateEmployee('/employee/initial/' + $(this).attr('initial') + '/page1/', false, 'employee/initial/'+$(this).attr('initial'));
    });

    /**
    * employee quick search active
    */

    $('div#search_header.employee_search.active a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateEmployee('/employee/filter/' + $(this).prev().val() + '/page1/', false, 'employee/filter/'+$(this).prev().val()) : updateEmployee('/employee/page1');
    });

    /**
     * employee clean up active
     */

    $('div#search_header.employee_search.active a#cleanup').click(function() {
        updateEmployee('/employee/page1');
    });

    /**
     * employee quick filter deactive
     */

    $('div#search_header.employee_search.deactive table#letter_menu tr td a, div#search_header.employee_search.deactive a#letter_back, div#search_header.employee_search.deactive a#letter_fwd').click(function() {
        updateEmployee('/employee/initial/' + $(this).attr('initial') + '/page1/deactive/', true, 'employee/initial/'+$(this).attr('initial'));
    });

    /**
    * employee quick search deactive
    */

    $('div#search_header.employee_search.deactive a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateEmployee('/employee/filter/' + $(this).prev().val() + '/page1/deactive/', true, 'employee/filter/'+$(this).prev().val()) : updateEmployee('/employee/page1/deactive/', true);
    });

    /**
     * employee clean up deactive
     */

    $('div#search_header.employee_search.deactive a#cleanup').click(function() {
        updateEmployee('/employee/page1/deactive/', true);
    });

    /**
     * careprofessional quick filter deactive
     */

    $('div#search_header.careprofessional_search.deactive table#letter_menu tr td a, div#search_header.careprofessional_search.deactive a#letter_back, div#search_header.careprofessional_search.deactive a#letter_fwd').click(function() {
        updateProfessional('/careprofessional/initial/' + $(this).attr('initial') + '/page1/deactive/', true, 'careprofessional/initial/'+$(this).attr('initial'));
    });

    /**
    * careprofessional quick search deactive
    */

    $('div#search_header.careprofessional_search.deactive a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateProfessional('/careprofessional/filter/' + $(this).prev().val() + '/page1/deactive/', true, 'careprofessional/filter/'+$(this).prev().val()) : updateProfessional('/careprofessional/page1/deactive/', true);
    });

    /**
     * careprofessional clean up deactive
     */

    $('div#search_header.careprofessional_search.deactive a#cleanup').click(function() {
        updateProfessional('/careprofessional/page1/deactive/', true);
    });

    /**
     * careprofessional quick filter active
     */

    $('div#search_header.careprofessional_search.active table#letter_menu tr td a, div#search_header.careprofessional_search.active a#letter_back, div#search_header.careprofessional_search.active a#letter_fwd').click(function() {
        updateProfessional('/careprofessional/initial/' + $(this).attr('initial') + '/page1/', false, 'careprofessional/initial/'+$(this).attr('initial'));
    });


    /**
    * careprofessional quick search active
    */

    $('div#search_header.careprofessional_search.active a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateProfessional('/careprofessional/filter/' + $(this).prev().val() + '/page1/', false, 'careprofessional/filter/'+$(this).prev().val()) : updateProfessional('/careprofessional/page1');
    });

    /**
     * careprofessional clean up active
     */

    $('div#search_header.careprofessional_search.active a#cleanup').click(function() {
        updateProfessional('/careprofessional/page1');
    });

    /**
     * student quick filter deactive
     */

    $('div#search_header.student_search.deactive table#letter_menu tr td a, div#search_header.student_search.deactive a#letter_back, div#search_header.student_search.deactive a#letter_fwd').click(function() {
        updateStudent('/careprofessional/student/initial/' + $(this).attr('initial') + '/page1/deactive/', true, 'careprofessional/student/initial/'+$(this).attr('initial'));
    });

    /**
    * student quick search deactive
    */

    $('div#search_header.student_search.deactive a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateStudent('/careprofessional/student/filter/' + $(this).prev().val() + '/page1/deactive/', true, 'careprofessional/student/filter/'+$(this).prev().val()) : updateStudent('/careprofessional/student/page1/deactive/', true);
    });

    /**
     * student clean up deactive
     */

    $('div#search_header.student_search.deactive a#cleanup').click(function() {
        updateStudent('/careprofessional/student/page1/deactive/', true);
    });

    /**
     * student quick filter active
     */

    $('div#search_header.student_search.active table#letter_menu tr td a, div#search_header.student_search.active a#letter_back, div#search_header.student_search.active a#letter_fwd').click(function() {
        updateStudent('/careprofessional/student/initial/' + $(this).attr('initial') + '/page1/', false, 'careprofessional/student/initial/'+$(this).attr('initial'));
    });


    /**
    * student quick search active
    */

    $('div#search_header.student_search.active a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateStudent('/careprofessional/student/filter/' + $(this).prev().val() + '/page1/', false, 'careprofessional/student/filter/'+$(this).prev().val()) : updateStudent('/careprofessional/student/page1');
    });

    /**
     * student clean up active
     */

    $('div#search_header.student_search.active a#cleanup').click(function() {
        updateStudent('/careprofessional/student/page1');
    });


    /**
     * device quick filter active
     */

    $('div#search_header.device_search.active table#letter_menu tr td a, div#search_header.device_search.active a#letter_back, div#search_header.device_search.active a#letter_fwd').click(function() {
        updateDevice('/device/initial/' + $(this).attr('initial') + '/page1/', false, 'device/initial/'+$(this).attr('initial'));
    });

    /**
    * device quick search active
    */

    $('div#search_header.device_search.active a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateDevice('/device/filter/' + $(this).prev().val() + '/page1/', false, 'device/filter/'+$(this).prev().val()) : updateDevice('/device/page1');
    });

    /**
     * device clean up active
     */

    $('div#search_header.device_search.active a#cleanup').click(function() {
        updateDevice('/device/page1');
    });

    /**
     * device quick filter deactive
     */

    $('div#search_header.device_search.deactive table#letter_menu tr td a, div#search_header.device_search.deactive a#letter_back, div#search_header.device_search.deactive a#letter_fwd').click(function() {
        updateDevice('/device/initial/' + $(this).attr('initial') + '/page1/deactive/', true, 'device/initial/'+$(this).attr('initial'));
    });


    /**
    * device quick search deactive
    */

    $('div#search_header.device_search.deactive a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateDevice('/device/filter/' + $(this).prev().val() + '/page1/deactive/', true, 'device/filter/'+$(this).prev().val()) : updateDevice('/device/page1/deactive/');
    });

    /**
     * device clean up deactive
     */

    $('div#search_header.device_search.deactive a#cleanup').click(function() {
        updateDevice('/device/page1/deactive/', true);
    });

    /**
     * user quick filter active
     */

    $('div#search_header.user_search.active table#letter_menu tr td a, div#search_header.user_search.active a#letter_back, div#search_header.user_search.active a#letter_fwd').click(function() {
        updateUser('/user/initial/' + $(this).attr('initial') + '/page1/', false, 'user/initial/' + $(this).attr('initial'));
    });

    /**
    * user quick search active
    */

    $('div#search_header.user_search.active a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateUser('/user/filter/' + $(this).prev().val() + '/page1/', false, 'user/filter/' + $(this).prev().val()) : updateUser('/device/page1');
    });

    /**
     * user clean up active
     */

    $('div#search_header.user_search.active a#cleanup').click(function() {
        updateUser('/device/page1');
    });

    /**
     * user quick filter deactive
     */

    $('div#search_header.user_search.deactive table#letter_menu tr td a, div#search_header.user_search.deactive a#letter_back, div#search_header.user_search.deactive a#letter_fwd').click(function() {
        updateUser('/user/initial/' + $(this).attr('initial') + '/page1/deactive/', true, 'user/initial/' + $(this).attr('initial'));
    });

    /**
    * user quick search deactive
    */

    $('div#search_header.user_search.deactive a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateUser('/user/filter/' + $(this).prev().val() + '/page1/deactive/', true, 'user/filter/' + $(this).prev().val()) : updateUser('/user/page1/deactive/');
    });

    /**
     * user clean up deactive
     */

    $('div#search_header.user_search.deactive a#cleanup').click(function() {
        updateUser('/user/page1/deactive/', true);
    });

    /**
     * service - client list - quick filter active
     */

    service = $('table#search_results input[name=service_id]').val();

    $('div#search_header.service_client_search.active table#letter_menu tr td a, div#search_header.service_client_search.active a#letter_back, div#search_header.service_client_search.active a#letter_fwd').click(function() {
        updateClientService('/service/'+ service +'/initial/' + $(this).attr('initial') + '/page1/', false, 'service/'+ service +'/initial/' + $(this).attr('initial'));
    });

    /**
    * service - client list - quick search active
    */

    $('div#search_header.service_client_search.active a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateClientService('/service/' + service + '/filter/' + $(this).prev().val() + '/page1/', false, 'service/' + service + '/filter/' + $(this).prev().val()) : updateClientService('/service/' + service + '/page1');
    });

    /**
     * service - client list - clean up active
     */

    $('div#search_header.service_client_search.active a#cleanup').click(function() {
        updateClientService('/service/'+ service + '/page1', false);
    });

    /**
     * place quick filter active
     */

    $('div#search_header.place_search.active table#letter_menu tr td a, div#search_header.place_search.active a#letter_back, div#search_header.place_search.active a#letter_fwd').click(function() {
        updatePlace('/place/initial/' + $(this).attr('initial') + '/page1/', false, 'place/initial/'+$(this).attr('initial'));
    });

    /**
    * place quick search active
    */

    $('div#search_header.place_search.active a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updatePlace('/place/filter/' + $(this).prev().val() + '/page1/', false, 'place/filter/'+$(this).prev().val()) : updatePlace('/place/page1');
    });

    /**
     * place clean up active
     */

    $('div#search_header.place_search.active a#cleanup').click(function() {
        updatePlace('/place/page1');
    });

    /**
     * place quick filter deactive
     */

    $('div#search_header.place_search.deactive table#letter_menu tr td a, div#search_header.place_search.deactive a#letter_back, div#search_header.place_search.deactive a#letter_fwd').click(function() {
        updatePlace('/place/initial/' + $(this).attr('initial') + '/page1/deactive/', true, 'place/initial/'+$(this).attr('initial'));
    });

    /**
    * place quick search deactive
    */

    $('div#search_header.place_search.deactive a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updatePlace('/place/filter/' + $(this).prev().val() + '/page1/deactive/', true, 'place/filter/'+$(this).prev().val()) : updatePlace('/place/page1/deactive/', true);
    });

    /**
     * place clean up deactive
     */

    $('div#search_header.place_search.deactive a#cleanup').click(function() {
        updatePlace('/place/page1/deactive/', true);
    });


    /**
     * room quick filter active
     */

    $('div#search_header.room_search.active table#letter_menu tr td a, div#search_header.room_search.active a#letter_back, div#search_header.room_search.active a#letter_fwd').click(function() {
        updateRoom('/place/room/initial/' + $(this).attr('initial') + '/page1/', false, 'place/room/initial/'+$(this).attr('initial'));
    });

    /**
    * room quick search active
    */

    $('div#search_header.room_search.active a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateRoom('/place/room/filter/' + $(this).prev().val() + '/page1/', false, 'place/room/filter/'+$(this).prev().val()) : updateRoom('/place/room/page1');
    });

    /**
     * room clean up active
     */

    $('div#search_header.room_search.active a#cleanup').click(function() {
        updateRoom('/place/room/page1');
    });

    /**
     * room quick filter deactive
     */

    $('div#search_header.room_search.deactive table#letter_menu tr td a, div#search_header.room_search.deactive a#letter_back, div#search_header.room_search.deactive a#letter_fwd').click(function() {
        updateRoom('/place/room/initial/' + $(this).attr('initial') + '/page1/deactive/', true, 'place/room/initial/'+$(this).attr('initial'));
    });

    /**
    * room quick search deactive
    */

    $('div#search_header.room_search.deactive a.quick_search').click(function() {
        ($(this).prev().val().length >= 1) ? updateRoom('/place/room/filter/' + $(this).prev().val() + '/page1/deactive/', true, 'place/room/filter/'+$(this).prev().val()) : updateRoom('/place/room/page1/deactive/', true);
    });

    /**
     * room clean up deactive
     */

    $('div#search_header.room_search.deactive a#cleanup').click(function() {
        updateRoom('/place/room/page1/deactive/', true);
    });

    /**
     * commom quick filter events
     */

    $('table#letter_menu tr td a, div#search_header a#letter_back, div#search_header a#letter_fwd').click(function() {

            var previous = ''
            var next = ''

            $('div#search_header a.arrow').show();
            $('table#letter_menu tr td a').removeClass('active');

            $('div.registers_available > h2 > span > span').html('"' + $(this).attr('initial').toUpperCase() + '"');
            $('div.registers_available > h2 > span').show();

            $(this).addClass('active');
            $('div#search_header div.capital_letter').text($(this).attr('initial').toUpperCase());

            if(!$(this).hasClass('arrow')) { // arrows < A - C >
                previous = $(this).parent('td').prev().children('a').text();
                next = $(this).parent('td').next().children('a').text();
            } else { // A,B,C,D,E etc
                var selected = $('table#letter_menu tr td a[initial=' + $(this).attr('initial') + ']').addClass('active');
                previous = selected.parent('td').prev().children('a').text();
                next = selected.parent('td').next().children('a').text()
            }

            $('div#search_header a#letter_back').text(previous);
            $('div#search_header a#letter_back').attr('initial', previous.toLowerCase());

            $('div#search_header a#letter_fwd').text(next);
            $('div#search_header a#letter_fwd').attr('initial', next.toLowerCase());

            if(!previous)
                $('div#search_header a.arrow#letter_back').hide();
            if(!next)
                $('div#search_header a.arrow#letter_fwd').hide();

            $('div#search_header input[type=text].quick_search').val('');

    });

    /**
    * commom quick search events
    */

    $('div#search_header a.quick_search').click(function() {
        if($(this).prev().val().length >= 1) {
            $('div.registers_available > h2 > span > span').html('"' + $(this).prev().val().toUpperCase() + '"');
            $('div.registers_available > h2 > span').show();
            $('div.registers_available > h2 > span > span').show();
        } else {
            $('h2.title_clients span').hide();
        }
    });

    /**
     * commom clean up
     */

    $('div#search_header a#cleanup').click(function() {
        $('div#search_header input[type=text].quick_search').val('');
        $('table#letter_menu tr td a').removeClass('active');
        $('div.registers_available > h2 span span').html('');
        $('div.registers_available > h2 span').hide();
    });

});
