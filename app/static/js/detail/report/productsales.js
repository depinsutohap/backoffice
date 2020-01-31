function _productsales(){
  nav_lang('report');
  business_list(); _date(); _detail()
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
      'status': 2,
    })
    }, function (e) {
      console.log('product sales')
      console.log(e)
      let i;
      $('#data_body').empty();
      if(e['status'] === '00'){
        if(e.data.product_sales.length > 0){
          $('#sold_total').text(e.data.total_sold);
          $('#revenue_total').text("Rp."+ formatNumber(e.data.total_revenue));
          for(i=0; i < e.data.product_sales.length; i++){
            product_sales_append(e.data.product_sales[i]);
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
  function product_sales_append(data){
    // console.log(data.all_sold)
    $('#data_body').append(
      '<tr>'+
      '<td>'+data.name + '</td>' +
      '<td>'+data.category + '</td>' +
      '<td>'+data.sku + '</td>' +
      '<td>'+data.sold_item + '</td>' +
      '<td>'+"Rp. "+formatNumber(data.revenue) + '</td>' +
      '</tr>'+
      '</table>'
    )
  }
