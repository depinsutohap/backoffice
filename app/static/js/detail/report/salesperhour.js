function _sales_per_hour(){
  nav_lang('report');
  business_list(); _date();
  _loading(1);

  $("#business").change(function () {
    outlet_list_b();
    _loading(1);
  });
  $("#outlet, #startdate, #enddate, #business").change(function () {
    _min_max_data();
    _loading(1);
    _detail();
    _min_max_data()
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
        'status': 11,
        'dash_on': 0,
      })
    }, function (e) {
      let i;
      $('#data_body').empty();
      if(e['status'] === '00'){
        $('#count_trx').text(e.data.total_sold);
        $('#total_revenue').text("Rp."+ formatNumber(e.data.total_revenue));
        $('#total_average').text("Rp."+ formatNumber(e.data.total_average));
        if(e.data.hourly_sales.length > 0){
          for(i=0; i < e.data.hourly_sales.length; i++){
            sales_per_hour_append(e.data.hourly_sales[i]);
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
  function sales_per_hour_append(data){
    console.log(data.hour)
    $('#data_body').append(
      '<tr>'+
      '<td>'+data.hour + '</td>' +
      '<td>'+data.total_trans + '</td>' +
      '<td>'+"Rp."+formatNumber(data.revenue) + '</td>' +
      '<td>'+"Rp."+formatNumber(data.average) + '</td>' +
      '</tr>'+
      '</table>'
    )
  }
