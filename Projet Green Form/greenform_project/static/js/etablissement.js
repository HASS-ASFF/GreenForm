
var SaveForm_etab =  function(){
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
                $('#modal-etab').modal('hide');
                setTimeout(function(){
                            location.reload(); 
                       }, 50); 
                
            } else {					
                $('#modal-etab .modal-content').html(data.html_form)

            }
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ":" + xhr.responseText)
        }
    })
    return false;
}


//--------------------------------------------ETABLISSEMENTS

ShowForm_etab = function(){
    btn = $(this);
    $.ajax({
        url: btn.attr("data-url"),
        type: 'GET',
        dataType:'json',
        beforeSend: function(){
            $('#modal-etab').modal('show');
        },
        success: function(data){
            $('#modal-etab .modal-content').html(data.html_form);
        }
    });
};

$(".show-form").click(ShowForm_etab);
$("#modal-etab").on("submit",".create-form",SaveForm_etab);

//update
$('#etab-table').on("click",".show-form-update",ShowForm_etab);
$('#modal-etab').on("submit",".update-form",SaveForm_etab);

//delete
$('#etab-table').on("click",".show-form-delete",ShowForm_etab);
$('#modal-etab').on("submit",".delete-form",SaveForm_etab);


