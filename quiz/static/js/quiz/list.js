$(document).ready(function() {
    $('.ui.segment.quiz .edit').on('click', function(e) {
        var quiz_id = $(this).attr('data-value');
        
        $.ajax({
            url: '/quiz/ajax/quiz_data/',
            data: {
                'id': quiz_id
            },
            dataType: 'json',
            success: function (data) {
                var url = '../quiz/' + quiz_id + '/edit/';
                
                $('.ui.modal.quiz form').attr('action', url);
                $('.ui.modal.quiz > .header').html('Edit quiz');
                $('.ui.modal.quiz #quiz_title').val(data.quiz_title);
                $('.ui.modal.quiz #quiz_description').val(data.quiz_description);
                $('.ui.modal.quiz #quiz_start_date').val(data.start_date);
                $('.ui.modal.quiz #quiz_start_date_time').val(data.start_date_time);
                $('.ui.modal.quiz #quiz_end_date').val(data.end_date);
                $('.ui.modal.quiz #quiz_end_date_time').val(data.end_date_time);
                
                $('.ui.modal.quiz').modal('show');
            }
        });
    }); 
    
    $('#add-quiz').on('click', function(e) {
        var url = '../quiz/new/';

        $('.ui.modal.quiz form').attr('action', url);
        $('.ui.modal.quiz > .header').html('Create a new quiz');
        $('.ui.modal.quiz #quiz_title').val('');
        $('.ui.modal.quiz #quiz_description').val('');
        $('.ui.modal.quiz #quiz_start_date').val('');
        $('.ui.modal.quiz #quiz_start_date_time').val('');
        $('.ui.modal.quiz #quiz_end_date').val('');
        $('.ui.modal.quiz #quiz_end_date_time').val('');

        $('.ui.modal.quiz').modal('show');
        
    }); 
    
    $('.ui.segment.quiz .delete').on('click', function(e) {
        var quiz_id = $(this).attr('data-value');
        var url = '../quiz/' + quiz_id + '/delete/';
        
        $('.ui.modal.action form').attr('action', url);
        $('.ui.modal.action').modal('show');
    }); 
});