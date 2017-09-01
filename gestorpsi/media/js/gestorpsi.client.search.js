<script>

/*
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


    function updateResults(url, initial) {
        if(!url) {
            if(!initial) {
                initial = ''
            }

            var admis;
            var url = '{{ list_url_base }}?search=' + encodeURIComponent($("#quick_search").val()) + "&initial=" + initial + '&service=' + $('select[name=service]').val() + '&subscribed=' + $('input[name=subscribed]').is(":checked") + '&discharged=' + $('input[name=discharged]').is(":checked") + '&queued=' + $('input[name=queued]').is(':checked') + '&nooccurrences=' + $('input[name=nooccurrences]').is(':checked');

            if ($('input#admissiondate').is(':checked') == true){
                var admis = "&admissiondate=true" + "&admissionStart=" + $('input[name=search_client_date_start]').val() + "&admissionEnd=" + $('input[name=search_client_date_end]').val();
            } else { 
                var admis = "&admissiondate=false";
            }

            var url = url + admis;
        }

        $('#page_results').load(url,function(responseTxt,statusTxt,xhr){
                if(statusTxt=="success") {
                    $('#pageof').text($('.pagination span.current').text());
                    $('#object_length').text($('input[name=result_count]').val());
                    }
                if(statusTxt=="error")
                    alert("Error: "+xhr.status+": "+xhr.statusText);
        });
    }


    $(function() {
        $('#quick_search').focus();
        $('#page_results .pagination a').click(function() {
            updateResults($(this).attr('href'));
            return false;
        });
        $('a.quick_search').click(function() {
            updateResults();
            return false;
        });
        $('a.initial').click(function() {
            updateResults(null, $(this).attr("initial"));
            return false;
        });
        $('select[name=service]').change(function() {
            updateResults();
            return false;
        });
        $('input[name=subscribed]').change(function() {
            updateResults();
            return false;
        });
        $('input[name=discharged]').change(function() {
            updateResults();
            return false;
        });
        $('input[name=queued]').change(function() {
            updateResults();
            return false;
        });
        $('input[name=nooccurrences]').change(function() {
            updateResults();
            return false;
        });

        $('a#cleanup').click(function() {
            updateResults();
            return false;
        });

        $('#quick_search').keydown(function(e) {
            if (e.keyCode == 13) {
                $('a.quick_search').click();
            }
        });

        /*
        * client search by adminission date section
        */
        // show and hide div search date
        $('input#admissiondate').click(function(){
            if (this.checked){
                $("div#search_client_admission").show();
            }else{
                $("div#search_client_admission").hide();
                updateResults();
                return false;
            }
        });

        // refresh search when out end date
        $('input.search_client_date_end').focusout(function(){ 
            updateResults();
            return false;
        });

        // load datepicker calendar
        $('input.search_client_date_end').datepicker({dateFormat:'dd/mm/yy', changeYear:true, "gotoCurrent":true});

        // update date end after choosen
        $('input.search_client_date_start, input.search_client_date_end').datepicker({
            dateFormat:'dd/mm/yy',
            changeYear:true,
            gotoCurrent:true,
            onSelect: function(dateText, inst){
                // update dateEnd calendar
                dtsplit = dateText.split("/");
                var enddate = new Date(dtsplit[2], dtsplit[1], dtsplit[0]);
                enddate.setMonth(enddate.getMonth() + 1);
                $("input.search_client_date_end").val(enddate.getDate() + "/" + enddate.getMonth() + "/" + enddate.getFullYear());
            },
        });
    }); // end function

</script>
