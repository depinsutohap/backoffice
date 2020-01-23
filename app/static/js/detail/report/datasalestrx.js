function _datasalestrx(){
  nav_lang('report');
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
      'status': 4,
    })
    }, function (e) {
      let i;
      $('#data_body').empty();
      if(e['status'] === '00'){
        $('#total_revenue').text("Rp. "+formatNumber(e.data.total_revenue));
        if(e.data.data.length > 0){
          for(i=0; i < e.data.data.length; i++){
            data_sales_trx_append(e.data.data[i]);
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

  function data_sales_trx_append(data){
    console.log(data)
    $('#data_body').append(
      '<tr>'+
      '<td>'+data.time + '</td>' +
      '<td>'+data.operator + '</td>' +
      '<td>'+data.idtrx + '</td>' +
      '<td>'+data.statustrx + '</td>' +
      '<td>'+"Rp."+formatNumber(data.total) + '</td>' +
      '</tr>'+
      '</table>'
    )
  }
