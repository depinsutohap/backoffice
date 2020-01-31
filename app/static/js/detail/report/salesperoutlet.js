function _sales_per_outlet(){
  nav_lang('report');
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
        'status': 6,
      })
    }, function (e) {
      console.log('sales per outler')
      console.log(e)
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
          $('.no_data').css('display', 'flex')
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
