

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
$('#part-table').on("click",".show-form-update",ShowForm);
$('#modal-part').on("submit",".update-form",SaveForm);

//delete
$('#part-table').on("click",".show-form-delete",ShowForm);
$('#modal-part').on("submit",".delete-form",SaveForm);

