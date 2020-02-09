function _export(id){
  $.post('/v1/api/data/subreport',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 16,
      business_id: $('#business').val(),
      outlet: $('#outlet').val(),
      dari: $('#startdate').val(),
      sampai: $('#enddate').val(),
      export_type : id
    })
  }, function (e) {
    if(e.status == '00'){
      notif('success', 'Your file has been succeessfully downloaded');
    }else{
      notif('danger', e.message);
    }
  }).fail(function(){
    notif('danger', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}
