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

$(function(){
    // show and hide search by matrix year
    $('input#filter_student_matrix_year').click(function(){
        if (this.checked){
            $("div#div_student_matrix_year_input").show();
        }else{
            $("div#div_student_matrix_year_input").hide();
            $("input[name=search_student_matrix_year]").val('');
        }
    });

    /**
     * student deactive filter by name and/or matrix year deactive
     */
    $('div#search_header.student_search.deactive table#letter_menu tr td a, div#search_header.student_search.deactive a#letter_back, div#search_header.student_search.deactive a#letter_fwd').click(function(){
        var matrix_year='';
        if ($("input[name=search_student_matrix_year]").val().length > 0) { 
            matrix_year = '?matrixyear=' + $("input[name=search_student_matrix_year]").val();
        }

        ($(this).attr('initial').length >= 1) ? updateStudent('/careprofessional/student/initial/' + $(this).attr('initial') + '/page1/deactive/' + matrix_year, true, 'careprofessional/student/initial/' + $(this).attr('initial'), matrix_year) : updateStudent('/careprofessional/student/page1/deactive/' + matrix_year, true, 'careprofessional/student/page1/', matrix_year);
    });

    /**
    * student quick search deactive
    */
    $('div#search_header.student_search.deactive a.quick_search').click(function() {
        var val = $('input.quick_search').val();

        var matrix_year='';
        if ($("input[name=search_student_matrix_year]").val().length > 0) { 
            matrix_year = '?matrixyear=' + $("input[name=search_student_matrix_year]").val();
        }

        (val.length >= 1) ? updateStudent('/careprofessional/student/filter/' + val + '/page1/deactive/' + matrix_year, true, 'careprofessional/student/filter/' + val, matrix_year) : updateStudent('/careprofessional/student/page1/deactive/' + matrix_year, true, 'careprofessional/student', matrix_year);
    });
    
    /**
     * student clean up deactive
     */
    $('div#search_header.student_search.deactive a#cleanup').click(function() {
        // clean matrix year
        $("div#div_student_matrix_year_input").hide();
        $("input[name=search_student_matrix_year]").val('');
        $("input#filter_student_matrix_year").prop("checked",false);
        // update list
        updateStudent('/careprofessional/student/page1/deactive/', true);
    });

    /**
     * student filter by part of name and/or matrix year active
     */
    $('div#search_header.student_search.active table#letter_menu tr td a, div#search_header.student_search.active a#letter_back, div#search_header.student_search.active a#letter_fwd').click(function() {
        var matrix_year='';
        if ($("input[name=search_student_matrix_year]").val().length > 0) { 
            matrix_year = '?matrixyear=' + $("input[name=search_student_matrix_year]").val();
        }

        ($(this).attr('initial').length >= 1) ? updateStudent('/careprofessional/student/initial/' + $(this).attr('initial') + '/page1/' + matrix_year, false, 'careprofessional/student/filter/' + $(this).prev().val(), matrix_year) : updateStudent('/careprofessional/student/page1/' + matrix_year, false, 'careprofessional/student/page1/', matrix_year);
    });

    /**
    * student quick search active
    */
    $('div#search_header.student_search.active a.quick_search, div#sidebar a.quick_search').click(function() {
        var val = $('input.quick_search').val();

        var matrix_year='';
        if ($("input[name=search_student_matrix_year]").val().length > 0) { 
            matrix_year = '?matrixyear=' + $("input[name=search_student_matrix_year]").val();
        }
        (val.length >= 1) ? updateStudent('/careprofessional/student/filter/' + val + '/page1/' + matrix_year, false, 'careprofessional/student/filter/' + val, matrix_year) : updateStudent('/careprofessional/student/page1/' + matrix_year, false, 'careprofessional/student', matrix_year);
    });

    /**
     * student clean up active
     */
    $('div#search_header.student_search.active a#cleanup').click(function() {
        // clean matrix year
        $("div#div_student_matrix_year_input").hide();
        $("input[name=search_student_matrix_year]").val('');
        $("input#filter_student_matrix_year").prop("checked",false);
        // update list
        updateStudent('/careprofessional/student/page1');
    });

});
