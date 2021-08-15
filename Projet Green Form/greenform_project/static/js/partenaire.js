
var SaveForm =  function(){
    var form = $(this);
    data = []
    contentType= false
    processData = false
    var string = form.attr("data-url")
    if(string.includes("modify")){
        formData = new FormData(this);
        data = formData
    }
    else {
        data = form.serialize()
        contentType= "application/x-www-form-urlencoded; charset=UTF-8"
        processData = true
    }
    $.ajax({

        url: form.attr('data-url'),
        contentType: contentType,
        processData: processData,
        data : data,
        type: form.attr('method'),
        dataType: 'json',
        cache : false,
        enctype: 'multipart/form-data',
        success: function(data){
            
            if(data.form_is_valid){
                $('#modal-part').modal('hide');
                setTimeout(function(){
                            location.reload(); 
                       }, 50); 
                
                
            } else {					
                $('#modal-part .modal-content').html(data.html_form)

            }
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ":" + xhr.responseText)
        }
    })
    return false;
}


//--------------------------------------------PARTENAIRES

ShowForm_part = function(){
    btn = $(this);
    $.ajax({
        url: btn.attr("data-url"),
        type: 'GET',
        dataType:'json',
        beforeSend: function(){
            $('#modal-part').modal('show');
        },
        success: function(data){
            $('#modal-part .modal-content').html(data.html_form);
        }
    });
};

$(".show-form").click(ShowForm_part);
$("#modal-part").on("submit",".create-form",SaveForm);

//update
$('#part-table').on("click",".show-form-update",ShowForm_part);
$('#modal-part').on("submit",".update-form",SaveForm);

//delete
$('#part-table').on("click",".show-form-delete",ShowForm_part);
$('#modal-part').on("submit",".delete-form",SaveForm);

