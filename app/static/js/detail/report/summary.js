function _summary(){
  business_list(); _date(); _detail();
  _loading(1);
  _min_max_data();

  $("#business").change(function () {
    outlet_list_b();
    _loading(1);
  });
  $("#outlet, #startdate, #enddate, #business").change(function () {
    _min_max_data();
    _loading(1);
    _detail()
  });
}

function _detail(){
  $.post('/v1/api/data/subreport',{
      data: JSON.stringify({
        'id': userData['id'],
        'token': userData['token'],
        'outlet': $('#outlet').val(),
        'dari': $('#startdate').val(),
        'sampai': $('#enddate').val(),
        'business_id': $('#business').val(),
        'status': 1,
      })
    }, function (e) {
      let i;
      if(e.status == '00'){
        if ( userData['id'] > 0){
          $('#revenue').text("Rp " + formatNumber(e.data.success_st));
          $('#discount').text("Rp "+ formatNumber(e.data.discount_success_st));
          $('#void').text("Rp "+ formatNumber(e.data.void_st));
          $('#nett_revenue').text("Rp "+ formatNumber(e.data.nettrevenue));
          $('#taxservice').text("Rp "+ formatNumber(e.data.tax_success_st));
          $('#total_revenue').text("Rp "+ formatNumber(e.data.total));
        }else{
          notif('danger', 'user tidak terdaftar')
        }
      }else{
        notif('danger', e.message);
      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

function _export(){
  $('#table').tableExport({type:'csv', fileName: 'summary'});
}
