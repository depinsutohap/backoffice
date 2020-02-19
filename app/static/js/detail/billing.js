// ========================================================
// FUNCTION OPEN PAGE
// ========================================================

function _billing(){
  _detail_page('overview');
  _submit_billing();
}

function _detail_page(t){
  $('#billing_title').text(capitalized(t));
  $('.detail_header').removeClass('active');
  $('#detail_' + t).addClass('active');
  $('#detailSection').load('/page/billing/section/' + t);
}

function _billing_overview(){
  $.post('/v1/api/data/billing',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 0,
    })
  }, function (e) {
    $('#data_body').empty();
    console.log(e)
    if(e.status == '00'){
      $('#order_count').text(e.count)
      if(e.ongoing !== true){

        if(e.business_list.length > 0){
          for(i=0; i<e.business_list.length; i++){
            $('#business_list').append(
              '<option value="' + e.business_list[i].id + '">' + e.business_list[i].name + '</option>'
            )
          }
        }

        for(i=0; i<e.data.length; i++){
          $('#data_body').append(
            '<tr class="data_row_' + e.data[i].id + ' data_business data_business_' + e.data[i].business_id.id + '">' +
            '<td><input value="' + e.data[i].id + '" class="check_data check_data_' + e.data[i].id + '" type="checkbox"></td>' +
            '<td>' + e.data[i].name + '</td>' +
            '<td>' + e.data[i].business_id.name + '</td>' +
            '<td>' + e.data[i].billing.name + '</td>' +
            '<td>' + e.data[i].billing.expired + '</td>' +
            '</tr>'
          )
        }
        for(i=0; i<e.package.length; i++){
          $('#edit_subs').append(
            '<option value="' + e.package[i].id + '">' +
            e.package[i].name +
            ' (' + formatNumber(e.package[i].value) + ')' +
            '</option>'
          )
        }

        _check();
      }else{
        _detail_page('history')
      }
    }
  }).fail(function(){
    notif('danger', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
  _submit_billing();
  _billing_filter();
}

function _billing_filter(){
  let value = 0;
  $('#business_list').on('change', function(t){
    value = $(this).val();
    $('.data_business').css('display', 'none')
    if(parseInt(value) !== 0){
      $('.data_business_' + value ).css('display', 'table-row')
    }else{
      $('.data_business').css('display', 'table-row')
    }
  })
}

function _billing_order(){
  $.post('/v1/api/data/billing',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 2,
    })
  }, function (e) {
    $('#data_body').empty();
    console.log(e)
    if(e.status == '00'){
      if(e.ongoing !== true){
        let _total = 0;
        for(i=0; i<e.payment.length; i++){
          $('#payment_list').append(
            '<option value="' + e.payment[i].id + '">' + e.payment[i].name + '</option>'
          )
        }
        for(i=0; i<e.data.list.length; i++){
          $('#data_body').append(
            '<tr class="data_row_' + e.data.list[i].id + '">' +
            '<td><input value="' + e.data.list[i].id + '" class="check_data check_data_' + e.data.list[i].id + '" type="checkbox"></td>' +
            '<td>' + e.data.list[i].outlet.name + '</td>' +
            '<td>' + e.data.list[i].outlet.business_id.name + '</td>' +
            '<td>' + e.data.list[i].package.name + '</td>' +
            '<td>' + formatNumber(e.data.list[i].package.total) + '</td>' +
            '</tr>'
          )
          _total += e.data.list[i].package.total
        }
        $('#data_body').append(
          '<tr>' +
          '<td></td>' +
          '<td></td>' +
          '<td></td>' +
          '<td>Total</td>' +
          '<td>' + formatNumber(_total) + '</td>' +
          '</tr>'
        )

        _check();
      }else{
        _detail_page('history')
      }
    }
  }).fail(function(){
    notif('danger', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
  _submit_billing();
}

function _billing_history(){
  $.post('/v1/api/data/billing',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 5,
    })
  }, function (e) {
    console.log(e)
    if(e.status == '00'){
        for(i=0; i<e.data.length; i++){
          let sub_class = '', detail_href = '';

          if(e.data[i].status.id == 2){
            detail_href = '<a class="db_bill" onclick="_detail_payment()"><i class="fas fa-eye"></i> Detail</a>'
          }else if(e.data[i].status.id == 3){
            sub_class = 'positive'
          }else if(e.data[i].status.id == 4 || e.data[i].status.id == 5){
            sub_class = 'danger'
          }
          $('#data_body').append(
            '<tr>' +
            '<td>' + e.data[i].name + ' (Rp ' + formatNumber(e.data[i].total) + ') <span class="sub '+ sub_class + '">' + e.data[i].status.name + '</span>' + detail_href + '</td>' +
            '<td>' + moment(e.data[i].datetime).lang("en").fromNow() + '</td>' +
            '</tr>'
          )
        }

    }

  }).fail(function(){
    notif('danger', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
  _submit_billing();
}

function _detail_payment(){
  $.post('/v1/api/data/billing',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 6,
    })
  }, function (e) {
    $('#data_body').empty();
    console.log(e)
    if(e.status=='00'){
      $('#mainBody').load('/page/billing/detail-payment', function() {
        $('.payment_datetime').text(e.data.datetime)
        $('.payment_code').text(e.data.billing_payment.company_code + e.data.user.phone_number)
        $('.payment_bill').text('Rp ' + formatNumber(e.data.total))
        if(e.data.payment_tools.length > 0){
          for(i=0;i<e.data.payment_tools.length;i++){
            _append_payment_list(e.data.payment_tools[i])
          }
        }
        _loading(0);
      });;
    }

  }).fail(function(){
    notif('danger', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
  _submit_billing();
}

function _append_payment_list(data){
  let _list = ''
  if(data.list.length>0){
    for(m=0; m<data.list.length;m++){
      _list += '<li>' + data.list[m] + '</li>'
    }
  }
  $('._list_table').append(
    '<div class="list_data list_data_' + data.id + '">' +
    '<div class="accordion" data-target="' + data.id + '" onclick="toggle_accordion(this)">' +
    '<div class="_column column_name">' +
    '<p class="outlet_name_' + data.id + '">'+ data.name + '</p>' +
    '</div>' +
    '</div>' +
    '<div id="accordion_' + data.id + '" class="accordion_collapse collapse">' +
    '<ol>' +
    _list +
    '</ol>' +
    '</div>'
  )
}

function _submit_billing(){
  $('form#form_billing_upgrade').submit(function(e){
    e.preventDefault();
    _loading(1);
    let _data = [], _check = $('.check_data:checked')
    for(i=0;i<_check.length;i++){
      _data.push($(_check[i]).val())
    }
    $.post('/v1/api/data/billing',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 1,
        package_id: $('#edit_subs').val(),
        outlet_list: _data
      })
    }, function (e) {
        if(e.status == '00'){
          for(i=0;i<_data.length;i++){
            $('.check_data_' + _data[i]).prop('checked', false).change()
            $('.data_row_' + _data[i]).remove()
          }
          $('#order_count').text(e.data.value)
          close_sideform()
          _detail_page('order')
        }else{
          _loading(0);
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  $('form#form_remove_order').submit(function(e){
    e.preventDefault();
    _loading(1);
    let _data = [], _check = $('.check_data:checked')
    for(i=0;i<_check.length;i++){
      _data.push($(_check[i]).val())
    }
    $.post('/v1/api/data/billing',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 3,
        package_id: $('#edit_subs').val(),
        trx_list: _data
      })
    }, function (e) {
      console.log(e)
        if(e.status == '00'){
          for(i=0;i<_data.length;i++){
            $('.check_data_' + _data[i]).prop('checked', false).change()
          }

          if(e.list.status == '00'){
            $('#data_body').empty();
            let _total = 0
            $('#data_body').empty();
            for(i=0; i<e.list.list.length; i++){
              $('#data_body').append(
                '<tr class="data_row_' + e.list.list[i].id + '">' +
                '<td><input value="' + e.list.list[i].id + '" class="check_data check_data_' + e.list.list[i].id + '" type="checkbox"></td>' +
                '<td>' + e.list.list[i].outlet.name + '</td>' +
                '<td>' + e.list.list[i].outlet.business_id.name + '</td>' +
                '<td>' + e.list.list[i].package.name + '</td>' +
                '<td>' + formatNumber(e.list.list[i].package.total) + '</td>' +
                '</tr>'
              )
              _total += e.list.list[i].package.total
            }
            $('#data_body').append(
              '<tr>' +
              '<td></td>' +
              '<td></td>' +
              '<td></td>' +
              '<td>Total</td>' +
              '<td>' + formatNumber(_total) + '</td>' +
              '</tr>'
            )
          }

          $('#order_count').text(e.data.value)
          close_sideform()
        }else{
          _loading(0);
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  $('form#form_payment_order').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/billing',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 4,
        payment_id: $('#payment_list').val(),
      })
    }, function (e) {
      console.log(e)
        if(e.status == '00'){
          $('#order_count').text(e.count)
          close_sideform();
          _detail_page('history');
        }else{
          _loading(0);
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).always(function(){
        _loading(0);
      });
  });

}
