function _taxrevenue(){
  business_list(); _date(); _detail();
  _loading(1);

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
  _loading(1);
  $.post('/v1/api/data/subreport',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'outlet': $('#outlet').val(),
      'dari': $('#startdate').val(),
      'sampai': $('#enddate').val(),
      'business_id': $('#business').val(),
      'status': 7,
    })
    }, function (e) {
      let i;
      console.log(e.data.length)
      $('#data_body').empty();
      if(e['status'] === '00'){
        if(e.data.data.length > 0){
          for(i=0; i < e.data.data.length; i++){
            tax_revenue_append(e.data.data[i], e.data);
          }
        }else{
          $('#data_body').append(
            '<div class="_notif_menu"><i class="fa fa-exclamation-triangle"></i>data belum tersedia.</div>'
          )
        }
      }else{
        notif('danger', 'System Error !', e.message);
      }
    }).fail(function(){
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}
  function tax_revenue_append(data){
    $('#data_body').append(
      '<tr>'+
      '<td>'+data.name + '</td>' +
      '<td>'+"Rp."+formatNumber(data.total_tax) + '</td>' +
      '</tr>'+
      '<tr>'+
      '<td>'+"Grand Total"+'</td>'+
      '<td>'+"Rp. "+formatNumber(data.grand_total)+'</td>'+
      '</tr>'+
      '</table>'
    )
  }
