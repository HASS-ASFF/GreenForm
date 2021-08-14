
//--------------------------------------------ABONNEMENTS

ShowForm_abo = function(){
    btn = $(this);
    $.ajax({
        url: btn.attr("data-url"),
        type: 'GET',
        dataType:'json',
        beforeSend: function(){
            $('#modal-abo').modal('show');
        },
        success: function(data){
            $('#modal-abo .modal-content').html(data.html_form);
        }
    });
};

$(".show-form").click(ShowForm_abo);
$("#modal-abo").on("submit",".create-form",SaveForm);

//update
$('#abo-table').on("click",".show-form-update",ShowForm);
$('#modal-abo').on("submit",".update-form",SaveForm);

//delete
$('#abo-table').on("click",".show-form-delete",ShowForm);
$('#modal-abo').on("submit",".delete-form",SaveForm);


