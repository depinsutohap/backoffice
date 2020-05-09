function _datasalestrx(){
  // nav_lang('report');
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
          $('.no_data').css('display', 'none')
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

  function data_sales_trx_append(data){
    console.log(data)
    $('#data_body').append(
      '<tr>'+
      '<td>'+data.time + '</td>' +
      '<td>'+data.operator + '</td>' +
      '<td>'+data.idtrx + '</td>' +
      '<td>'+data.statustrx + '</td>' +
      '<td>'+"Rp."+formatNumber(data.total) + '</td>' +
      '<td><a class="data_detail" onclick="_data_trx(\'' + data.idtrx + '\')"><i class="fas fa-info-circle"></i></a></td>' +
      '</tr>'+
      '</table>'
    )
  }

  function _data_trx(trx_id){
    _loading(1);
    $.post('/v1/api/data/subreport',{
      data: JSON.stringify({
        'id': userData['id'],
        'token': userData['token'],
        'trx_id': trx_id,
        'status': 15,
      })
      }, function (e) {
        console.log(e)
        if(e.status == '00'){
          $('#no_order').text(e.data.no_order);
          $('#order_name').text(e.data.order_name);
          $('#operator').text(e.data.operator);
          $('#table').text(e.data.table);
          $('#code_struk, #detail_trx_title').text(e.data.code_struk);
          $('#transaction_time').text(e.data.transaction_time);
          $('#payment_cashier').text(e.data.payment_cashier);
          $('#payment').text(e.data.payment);
          $('#status_transaction').text(e.data.status_transaction);
          $('#sub_total').text('Rp ' + formatNumber(e.data.sub_total));
          $('#discount').text('Rp ' + formatNumber(e.data.discount));
          $('#tax').text('Rp ' + formatNumber(e.data.tax));
          $('#total').text('Rp ' + formatNumber(e.data.total));
          $('#payment_amount').text('Rp ' + formatNumber(e.data.payment_amount));
          $('#change').text('Rp ' + formatNumber(e.data.change));

          $('.data_detail_product').empty();
          for(i=0; i<e.data.product_list.length; i++){
            $('.data_detail_product').append(
              '<div class="colum_input">' +
              '<p class="title"><span class="quantity">' + e.data.product_list[i].quantity + '</span>' + e.data.product_list[i].product + '</p>' +
              '<p class="body" id="sub_total">' + e.data.product_list[i].price + '</p>' +
              '</div>'
            )
          }

          open_sideform('detail_trx');
        }

      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  }
