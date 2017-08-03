$(document).ready(function() {
    
    $('.form input').attr("maxlength", "1");
    $('.form input').attr("class", "no-spin");
    
    
    $('.form input').keyup(function(){
        var key = event.keyCode || event.charCode;
        var id = parseInt($(this).attr('id').substr(4,5));
        
        if( key == 8 || key == 46 ){
            id -= 1;
            if ((id)%10==0)
                id-=1;
            var id_prev = $(this).attr('id').substr(0,4) + id.toString();
            $('#'+id_prev).focus(); 
            console.log(id_prev);
        }
        
        if(this.value.length==$(this).attr("maxlength")){
            id += 1;
            if (id%10==0)
                id+=1;
            var id_next = $(this).attr('id').substr(0,4) + id.toString();
            $('#'+id_next).focus();
        }
    });
    
    $('#sample-btn').on('click', function(){
        for(i=1; i<10; i++) {
            for(j=1; j<10; j++) {
                $("#id_s" + i.toString() + j.toString()).val("");
            }
        }
        
        var sample = `003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300`
        var x=0;
        for(i=1; i<10; i++) {
            for(j=1; j<11; j++) {
                if (j<10 && sample[x]!='0')
                    $("#id_s" + i.toString() + j.toString()).val(sample[x]);
                x++;
            }
        }
    });
    
    $('#discard-btn').on('click', function(){
        for(i=1; i<10; i++) {
            for(j=1; j<10; j++) {
                $("#id_s" + i.toString() + j.toString()).val("");
            }
        }
    });
    
});