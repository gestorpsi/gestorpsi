<script>
    $(function() {
        $('#page_results').load('{{ list_url_base }}',function(responseTxt,statusTxt,xhr){
            if(statusTxt=="success") {
                $('#pageof').text($('.pagination span.current').text());
                $('#object_length').text($('input[name=result_count]').val());
            }
            if(statusTxt=="error")
                alert("Error: "+xhr.status+": "+xhr.statusText);
            });
    });
</script>
