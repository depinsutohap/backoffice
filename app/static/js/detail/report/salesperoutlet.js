function _sales_per_outlet(){
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
        'status': 6,
      })
    }, function (e) {
      let i;
      $('#data_body').empty();
      if(e['status'] === '00'){
        $('#count_trx').text(e.data.count_trx);
        $('#revenue').text("Rp."+ formatNumber(e.data.total_revenue));
        $('#avgrevenue').text("Rp."+ formatNumber(e.data.avg_revenue));
        if(e.data.data.length > 0){
          for(i=0; i < e.data.data.length; i++){
            sales_per_outlet_append(e.data.data[i]);
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
  function sales_per_outlet_append(data){
    $('#data_body').append(
      '<tr>'+
      '<td>'+data.outlet + '</td>' +
      '<td>'+data.sold + '</td>' +
      '<td>'+"Rp."+formatNumber(data.revenue) + '</td>' +
      '<td>'+"Rp."+formatNumber(data.avg) + '</td>' +
      '</tr>'+
      '</table>'
    )
  }
