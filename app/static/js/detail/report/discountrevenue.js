function _discrevenue(){
  business_list(); _date(); _detail();
  _loading(1);

  $("#outlet, #startdate, #enddate, #business").change(function () {
    outlet_list();
    _loading(1);
    _detail();
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
        'status': 8,
      })
    }, function (e) {
      let i;
      $('#data_body').empty();
      if(e['status'] === '00'){
        $('#count_trx').text(e.data.count_trx);
        $('#total_amount').text("Rp."+ formatNumber(e.data.total_amount));
        if(e.data.data.length > 0){
          for(i=0; i < e.data.data.length; i++){
            discount_revenue_append(e.data.data[i]);
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
  function discount_revenue_append(data){
    console.log(data)
    $('#data_body').append(
      '<tr>'+
      '<td>'+data.name +" (" +formatNumber(data.value)+")"+'</td>' +
      '<td>'+data.count + '</td>' +
      '<td>'+"Rp."+formatNumber(data.total_disc) + '</td>' +
      '</tr>'+
      '</table>'
    )
  }
