$(document).ready(function() {
    $('.voting-results').progress();
    
    // add another choice functionality
    var fields_array = $('.more-fields').find("input");
    var fields_n = 1;
    
    $('.required').find('input').attr("required","");
    
    $('#more-btn').on('click', function(e) {
        $('#extra-field'+fields_n).show();
        fields_n += 1;
        if (fields_n > fields_array.length) {
            $('#choice-max-warning').show();
            $(this).hide();
        }
    });
    
});