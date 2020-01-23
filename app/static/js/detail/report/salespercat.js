function _sales_per_cat(){
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
        'status': 5,
      })
    }, function (e) {
      let i;
      $('#data_body').empty();
      if(e['status'] === '00'){
        $('#sold_total').text(e.data.total_sold);
        $('#revenue_total').text("Rp."+ formatNumber(e.data.total_revenue));
        $('#avgrevenue').text("Rp."+ formatNumber(e.data.total_average));
        if(e.data.data.length > 0){
          for(i=0; i < e.data.data.length; i++){
            sales_per_category_append(e.data.data[i]);
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
  function sales_per_category_append(data){
    $('#data_body').append(
      '<tr>'+
      '<td>'+data.category + '</td>' +
      '<td>'+data.sold + '</td>' +
      '<td>'+"Rp."+formatNumber(data.total_revenue) + '</td>' +
      '<td>'+"Rp."+formatNumber(data.average) + '</td>' +
      '</tr>'+
      '</table>'
    )
  }
