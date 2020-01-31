function _dashboard_sales(){
  business_list(); _date(); _detail();
  _loading(1);

  $("#outlet, #startdate, #enddate, #business").change(function () {
    outlet_list();
    _loading(1);
    _detail()
  });

  nav_lang('report');

}

function _detail(){
  _loading(1);
  $.post('/v1/api/data/dashboard',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'outlet': $('#outlet').val(),
      'dari': $('#startdate').val(),
      'sampai': $('#enddate').val(),
      'business_id': $('#business').val(),
      'dash_on': 0,
    })
  }, function (e) {
    console.log(e)
    let i;
    $('#data_body').empty();
    if(e['status'] === '00'){
      if(e.data.hourly_sales.length > 0){
          graph(e.data.hourly_sales, e.data.product_sales, e.data.category_sales);
      }
      else{
        graph();
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

function graph(data_sell, product_sell, category_sell){
  _loading(0);
  var data_sales = []
  var product_sell_data = []
  var category_sell_data = []
  if (typeof data_sell !== 'undefined') {
      product_sell.sort((a, b) => parseFloat(b.sold_item) - parseFloat(a.sold_item));
      category_sell.sort((a, b) => parseFloat(b.sold) - parseFloat(a.sold));
      for(i=0; i < data_sell.length; i++){
        data_sales.push([data_sell[i]['hour'],data_sell[i]['revenue']])
      }
      for(i=0; i < product_sell.length; i++){
        product_sell_data.push([product_sell[i]['name'],product_sell[i]['sold_item']])
      }
      for(i=0; i < category_sell.length; i++){
        category_sell_data.push([category_sell[i]['category'],category_sell[i]['sold']])
      }
  }else {
      for (i=0; i<24; i++){
          x = i.toString().length
          if (x < 2){
            y = '0'+i+':00';
          }
          else{
            y = i+':00';
          }
          data_sales.push([y,0]);
      }
      for (i=0; i<5; i++){
        product_sell_data.push(['-',0])
      }
      for (i=0; i<5; i++){
        category_sell_data.push(['-',0])
      }
  }
  sorted_product = product_sell_data.slice(0, 5).sort((a,b) => b.sold_item - a.sold_item);
  sorted_category = category_sell_data.slice(0, 5).sort((a,b) => b.sold - a.sold);
  graph_single_line('sales_line_chart', data_sales);
  graph_bar('product_bar_chart', sorted_product);
  graph_bar('category_bar_chart', sorted_category);
}
