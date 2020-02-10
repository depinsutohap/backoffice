
function _export(id){
  $.post('/v1/api/data/export',{
      data: JSON.stringify({
        'id': userData['id'],
        'token': userData['token'],
        'business_id': $('#business').val(),
        'outlet': $('#outlet').val(),
        'dari': $('#startdate').val(),
        'sampai': $('#enddate').val(),
        'status': 1, //EXCEL
        'export_type': id
      })
    }, function (e) {
      console.log(e)
      let i;
      if(e.status == '00'){
        notif('success', 'Your file has beem successfully downloaded');
      }else{
        notif('danger', e.message);
      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}
