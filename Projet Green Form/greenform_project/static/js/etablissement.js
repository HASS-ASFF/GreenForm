
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
$("#modal-etab").on("submit",".create-form",SaveForm);

//update
$('#etab-table').on("click",".show-form-update",ShowForm);
$('#modal-etab').on("submit",".update-form",SaveForm);

//delete
$('#etab-table').on("click",".show-form-delete",ShowForm);
$('#modal-etab').on("submit",".delete-form",SaveForm);


