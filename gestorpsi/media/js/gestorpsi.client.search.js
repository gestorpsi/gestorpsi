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

$(document).ready(function(){

    function updateResults(url, initial){
        if (!initial){
            var initial = ''
        }

        var url = '{{ list_url_base }}?search=' + encodeURIComponent($("#quick_search").val()) + "&initial=" + initial + '&service=' + $('select[name=service]').val() + '&subscribed=' + $('input[name=subscribed]').is(":checked") + '&discharged=' + $('input[name=discharged]').is(":checked") + '&queued=' + $('input[name=queued]').is(':checked') + '&nooccurrences=' + $('input[name=nooccurrences]').is(':checked') + '&noreferral=' + $('input[name=noreferral]').is(":checked");

        // filter by admission date
        if ($('input#admissiondate').is(':checked') == true){
            var url = url + "&admissiondate=true" + "&admissionStart=" + $('input[name=search_client_date_start]').val() + "&admissionEnd=" + $('input[name=search_client_date_end]').val();
        } else {
            var url = url + "&admissiondate=false";
        }

        // filter by date subscribe a service
        if ($('input#servicedate').is(':checked') == true){
            var url = url + "&servicedate=true" + "&serviceStart=" + $('input[name=search_client_servicestart]').val() + "&serviceEnd=" + $('input[name=search_client_serviceend]').val();
        } else {
            var url = url + "&servicedate=false";
        }

        // export to PDF, exp
        exp = $('input[name="export_pdf_list"]').is(':checked');
        if (exp == true){
            var url = url + '&exp=pdf';
            window.open(url, '_blank', 'toolbar=0');
            return false;
        }

        // itens per page, ipp
        ipp = $('select[name="item_per_page_selected"]').val();
        var url = url + '&ipp=' + ipp;

        // reload result
        $('#page_results').load(url,function(responseTxt,statusTxt,xhr){
            if(statusTxt=="success"){
                $('#pageof').text($('.pagination span.current').text());
                $('#object_length').text($('input[name=result_count]').val());
            }

            if(statusTxt=="error"){
                alert("Error: "+xhr.status+": "+xhr.statusText);
            }
        });

    } // end updateResults


    // bind functions
    $(function(){
        $('#quick_search').focus();

        // paginator link ?
        $('#page_results .pagination a').click(function(){
            updateResults($(this).attr('href'), null);
            return false;
        });

        // submit procura buttom
        $('a.quick_search').click(function(){
            updateResults();
            return false;
        });

        // initial letter of name
        $('a.initial').click(function(){
            updateResults(null, $(this).attr("initial"));
            return false;
        });

        // name or part of name
        $('#quick_search').keydown(function(e){
            if (e.keyCode == 13){
                $('a.quick_search').click();
            }
        });

        // clean up
        $('a#cleanup').click(function(){
            updateResults();
            return false;
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
            }
        });

        // filter by a service
        $('select[name=service]').change(function(){
            // show service checkbox filter
            if ($('select[name=service]').val()){ 
                $('label[for=servicedate_label]').show();
                $('input#noreferral').attr('checked', false);
            } else { 
                $('label[for=servicedate_label]').hide();
            }
        });

        // show and hide input field for start/end date.
        $('input#servicedate').click(function(){
            if (this.checked){
                $("div#search_client_servicedate").show();
            }else{
                $("div#search_client_servicedate").hide();
            }
        });

        // reset noreferral not any other checkbox
        $('input:checkbox').click(function(){ 
            if (this.name != 'noreferral'){ 
                $('input#noreferral').attr('checked', false);
            }
        });

        // show and hide input field for start/end date.
        $('input#noreferral').click(function(){
            if (this.checked){
                // reset another checkbox
                $("input[name=subscribed]").attr('checked', false);
                $("input[name=discharged]").attr('checked', false);
                $("input[name=queued]").attr('checked', false);
                $("input[name=nooccurrences]").attr('checked', false);
                $("input[name=admissiondate]").attr('checked', false);
                $("input[name=servicedate]").attr('checked', false);
                // hide input date
                $("div#search_client_admission").hide();
                $("div#search_client_servicedate").hide();
                $('label[for=servicedate_label]').hide();
                // select service
                $("select[name=service]").val("");
            }
        });

        // update date end after choosen for admission filter
        $('input.search_client_date_start, input.search_client_date_end').datepicker({
            dateFormat:'dd-mm-yy',
            changeYear:true,
            gotoCurrent:true,
            onSelect: function(dateText, inst){
                // update dateEnd calendar
                dtsplit = dateText.split("-");
                var enddate = new Date(dtsplit[2], dtsplit[1], dtsplit[0]);
                enddate.setMonth(enddate.getMonth() + 1);
                $("input.search_client_date_end").val(enddate.getDate() + "-" + enddate.getMonth() + "-" + enddate.getFullYear());
            },
        });

        // update date end after choosen for service subscribe date filter
        $('input.search_client_servicestart, input.search_client_serviceend').datepicker({
            dateFormat:'dd-mm-yy',
            changeYear:true,
            gotoCurrent:true,
            onSelect: function(dateText, inst){
                // update dateEnd calendar
                dtsplit = dateText.split("-");
                var enddate = new Date(dtsplit[2], dtsplit[1], dtsplit[0]);
                enddate.setMonth(enddate.getMonth() + 1);
                $("input.search_client_serviceend").val(enddate.getDate() + "-" + enddate.getMonth() + "-" + enddate.getFullYear());
            },
        });

    }); // end function

    // unbind function, avoid duplicate action and request.
    $('a.quick_search').unbind();

}); // end ready
</script>
