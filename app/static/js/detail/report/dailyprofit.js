function _dailyprofit(){
  nav_lang('report');
  business_list(); _date(); _detail()
  _loading(1);
  $("#outlet, #startdate, #enddate, #business").change(function () {
    outlet_list_b();
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
        'status': 9,
      })
    }, function (e) {
      let i;
      $('#data_body').empty();
      if(e['status'] === '00'){
        if(e.data.data.length > 0){
          $('#total_trans').text(e.data.total_trans);
          $('#total_tax').text("Rp."+ formatNumber(e.data.total_tax));
          $('#total_discount').text("Rp."+ formatNumber(e.data.total_discount));
          $('#total_cost').text("Rp."+ formatNumber(e.data.total_cost));
          $('#total_profit').text("Rp."+ formatNumber(e.data.total_profit));
          for(i=0; i < e.data.data.length; i++){
            daily_profit_append(e.data.data[i]);
          }
        }else{
          $('.no_data').css('display', 'flex')
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
  function daily_profit_append(data){
    // console.log(data.all_sold)
    $('#data_body').append(
      '<tr>'+
      '<td>'+data.datePayment + '</td>' +
      '<td>'+"Rp. "+formatNumber(data.revenue) + '</td>' +
      '<td>'+"Rp. "+formatNumber(data.tax) + '</td>' +
      '<td>'+"Rp. "+formatNumber(data.discount) + '</td>' +
      '<td>'+"Rp. "+formatNumber(data.cost) + '</td>' +
      '<td>'+"Rp. "+formatNumber(data.profit) + '</td>' +
      '</tr>'+
      '</table>'
    )
  }