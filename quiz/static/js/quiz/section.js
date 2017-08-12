function ChoiceHTML (index, choice_text, correct, id) {
    if (correct == true) 
        var checked = "checked"
    else
        var checked = ""
    var result = `<div class="field">
                <div class="fields">
                    <div class="thirteen wide field">
                        <input type="text" name="`+ id +`_value" id="`+ id +`_value" value="`+ choice_text +`" />
                    </div>
                    <div class="two wide field" style="display: flex; align-items: center;">
                        <div class="ui checkbox">
                          <input type="checkbox" id="`+ id +`_correct" name="`+ id +`_correct" value="correct" `+ checked +`>
                          <label for="`+ id +`">Correct</label>
                        </div>
                    </div>
                    <div class="one wide field">
                        <div class="circular negative ui icon button"><i class="icon trash"></i></div>
                    </div>
                </div>
            </div>`
    return result;
}


// Keep scroll position
$(window).scroll(function () {
    //set scroll position in session storage
    sessionStorage.scrollPos = $(window).scrollTop();
});
var init = function () {
    //get scroll position in session storage
    $(window).scrollTop(sessionStorage.scrollPos || 0)
};
window.onload = init;

var qtype = 'm';

$(document).ready(function() {
    
    // Countdown
    var total_seconds = parseInt($("#time_limit").val())+1;
    // Update the count down every 1 second
    var x = setInterval(function() {

        // Time calculations for days, hours, minutes and seconds
        total_seconds -= 1;
        
        var hours   = Math.floor(total_seconds/(3600));
        var minutes = Math.floor(total_seconds%(3600)/(60));
        var seconds = Math.floor(total_seconds%(60));

        // Display the result in the element with id="demo"
        $("#timer").html(hours + "h " + minutes + "m " + seconds + "s ");
        $("#time_limit").val(total_seconds);

        // If the count down is finished, write some text 
        if (total_seconds < 0) {
            clearInterval(x);
            $("#timer").html("Time is over");
            $('#submit-form').submit();
        }
    }, 1000);
    
    $('.ui.button.edit.question').on('click', function(e) {
        var question_id = $(this).attr('data-value');
        
        $.ajax({
            url: '/quiz/ajax/question_data/',
            data: {
                'id': question_id
            },
            dataType: 'json',
            success: function (data) {
                var url = "/quiz/question/" + question_id + "/edit/";
                
                $('.ui.modal.question form').attr('action', url);
                $('.ui.modal.question > .header').html('Edit item');
                $('.ui.modal.question #question_text').val(data.question_text);
                $('.ui.modal.question #question_points').val(data.points);
                
                var extra;
                if (data.choices) {
                    qtype = 'm';
                    extra = '<h4 class="ui dividing header">Choices</h4>';
                    $.each(data.choices, function(index, value) {
                        extra += ChoiceHTML(question_id, this.choice_text, this.correct, 'question_'+question_id+'__choice_'+this.id);
                    });
                }
                else if (data.solution) {
                    qtype = 'f';
                    extra  = `<h4 class="ui dividing header">Solution</h4>
                              <div class="field">
                                <input type="text" name="question_solution" id="question_solution" value="`+ data.solution +`" required />
                              </div>`;
                }
                else if (data.max_characters) {
                    qtype = 'e';
                    extra  = `<h4 class="ui dividing header">Answer</h4>
                              <div class="field">
                                <label>Maximum characters</label>
                                <input type="number" name="question_max_characters" id="question_max_characters" value="`+ data.max_characters +`" required />
                              </div>`;
                }
                
                $('.ui.modal.question #modal-extra').html(extra);
                
                $('.ui.modal.question').modal('show');
            }
        });
    });
    
    $('.add-question').on('click', function(e) {
        $('.ui.modal.question > .header').html('Create a new question');
        $('.ui.modal.question #question_text').val('');
        $('.ui.modal.question #question_points').val('');
        
        var extra = "", url;
        if ($(this).attr('id') == 'add-multiple') {
            qtype = 'm';
            url = "question/new/m/";
            extra = '<h4 class="ui dividing header">Choices</h4>';
            for (i=1; i<=4; i++) {
                extra += ChoiceHTML(i, '', false, 'question_new__choice_'+i);
            }
        } else if ($(this).attr('id') == 'add-fill') {
            qtype = 'f';
            url = "question/new/f/";
            extra  = `<h4 class="ui dividing header">Solution</h4>
                      <div class="field">
                        <input type="text" name="question_solution" id="question_solution" value="" required />
                      </div>`;
        } else if ($(this).attr('id') == 'add-essay') {
            qtype = 'e';
            url = "question/new/e/";
            extra  = `<h4 class="ui dividing header">Answer</h4>
                      <div class="field">
                        <label>Maximum characters</label>
                        <input type="number" name="question_max_characters" id="question_max_characters" value="" required />
                      </div>`;
        }
        
        $('.ui.modal.question form').attr('action', url);
        $('.ui.modal.question #modal-extra').html(extra);
        
        $('.ui.modal.question').modal('show');
    });
    
    $('#question-form').submit(function() {
        var valid = false;
        $.each($('#question-form').find('input'), function(index, obj) {
            if (obj.id.match("correct$")){
                if (obj.checked)
                    valid = true;
            }
        });
        
        if (!valid && qtype=='m') {
            alert('At least one of the answers must be correct!');
            return false;
        }
    });
    
    $('#edit-section').on('click', function(e) {
        var section_id = $(this).attr('data-value');
        
        $.ajax({
            url: '/quiz/ajax/section_data/',
            data: {
                'id': section_id
            },
            dataType: 'json',
            success: function (data) {
                var url = 'edit/';
                
                $('.ui.modal.section > .header').val("Edit section");
                $('.ui.modal.section #section_title').val(data.section_title);
                $('.ui.modal.section #section_description').val(data.section_description);
                $('.ui.modal.section #section_time_hours').val(parseInt(data.total_minutes/60));
                $('.ui.modal.section #section_time_minutes').val(data.total_minutes%60);
                $('.ui.modal.section form').attr('action', url);
            }
        });
        
        $('.ui.modal.section').modal('show');
    });
    
    $('#add-section').on('click', function(e) {
        var url = '../new/';

        $('.ui.modal.section > .header').val("Create a new section");
        $('.ui.modal.section #section_title').val('');
        $('.ui.modal.section #section_description').val('');
        $('.ui.modal.section #section_time_hours').val(0);
        $('.ui.modal.section #section_time_minutes').val(0);
        $('.ui.modal.section form').attr('action', url);
        
        $('.ui.modal.section').modal('show');
    });
    
    $('#delete-section').on('click', function(e) {
        $('.ui.basic.modal.action').modal('show');
    });
    
    $('.ui.sticky').sticky({
        context: '#main_content'
    });
});