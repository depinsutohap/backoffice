

// ========================================================
// FUNCTION FOR STOCK OPNAME LIST
// ========================================================

function stock_opname(){
  outlet_list(); _min_max_data();
  stock_opname_list();
}

function stock_opname_list(){
  $.post('/v1/api/data/stock',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 10,
      from_date: $('.from_date').val(),
      to_date: $('.to_date').val(),
      outlet: $('#outlet').val(),
    })
  }, function (e) {
    if(e.data.status == '00'){
      for(i=0;i<e.data.list.length;i++){
        $('#data_body').append(
          '<tr class="_click" onclick="_stock_opname_detail(' + e.data.list[i].id + ', ' + e.data.list[i].outlet.id + ')">' +
          '<td>' + e.data.list[i].name + '</td>' +
          '<td>' + e.data.list[i].outlet.name + '</td>' +
          '<td>' + e.data.list[i].date + '</td>' +
          '</tr>'
        )
      }
    }
  }).done(function(){
    _loading(0)
  })
}

function _stock_opname_detail(id, outlet_id){
  _loading(1)
  $.post('/v1/api/data/stock',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 11,
      stock_id: id,
      outlet: outlet_id,
    })
  }, function (e) {
    if(e.data.status == '00'){
      $('#data_body_modal').empty()
      $('#stock_opname_modal_title').text(e.data.name)
      $('.stock_opname_outlet').text(e.data.outlet.business_id.name + ' - ' + e.data.outlet.name)
      $('.stock_opname_date').text(e.data.date)
      for(i=0;i<e.data.list.length;i++){
        let vid = ''
        if(e.data.list[i].pid.variant_type == true){
          if(e.data.list[i].vid.status == '00'){
            vid = e.data.list[i].vid.variant_item_1.name;
            if(e.data.list[i].vid.variant_item_2 !== null){
              vid += '-' + e.data.list[i].vid.variant_item_2.name;
              if(e.data.list[i].vid.variant_item_3 !== null){
                vid += '-' + e.data.list[i].vid.variant_item_3.name;
                if(e.data.list[i].vid.variant_item_4 !== null){
                  vid += '-' + e.data.list[i].vid.variant_item_4.name;
                }
              }
            }
          }
        }
        let measurement = '';
        if(e.data.list[i].pid.measurement.status == '00'){
          measurement = e.data.list[i].pid.measurement.name
        }
        let sc = 'ds'
        if(e.data.list[i].quantity_deviation < 0){
          sc = 'rs'
        }else if(e.data.list[i].quantity_deviation > 0){
          sc = 'gs'
        }
        $('#data_body_modal').append(
          '<tr>' +
          '<td>' + e.data.list[i].pid.name + '</td>' +
          '<td>' + vid + '</td>' +
          '<td>' + formatNumber(e.data.list[i].quantity_system) + '</td>' +
          '<td><span class="' + sc + '">' + formatNumber(e.data.list[i].quantity_system + e.data.list[i].quantity_deviation) + '</span></td>' +
          '<td><span class="' + sc + '">' + formatNumber(e.data.list[i].quantity_deviation) + '</span></td>' +
          '<td>' + measurement + '</td>' +
          '</tr>'
        )
      }
    }
    open_sideform('stock_opname_modal')
  }).fail(function(){
    notif('warning', 'An unknown error has occured')
  }).always(function(){
    _loading(0);
  })
}

// ========================================================
// FUNCTION FOR ADD STOCK OPNAME
// ========================================================


function add_stock_opname(){
  outlet_list(); $('#date').attr('max', _create_date(0)).val(_create_date(0));
  _submit_form();

  $('#outlet').on('change', function(){
    if($(this).val() !== '0'){
      _add_data();
    }else{
      $('.table_body').empty();
      $('._data_opname').css('display', 'none');
    }
  })
}

function _add_data(){
  _loading(1);
  $.post('/v1/api/data/stock',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 12,
      outlet: $('#outlet').val(),
    })
  }, function(e){
    if(e.status == '00'){
      $('.table_body').empty();
      row = 0;
      for(i=0; i<e.data.list.length; i++){
        _append_row(row, e.data.list[i])
        row += 1;
      }
    }
  }).done(function(e){
    $('._data_opname').css('display', 'flex');
    _loading(0);
  });
}

function _append_row(row, data){
  let vid = '', measurement = '-', vid_id=0;
  if(data.pid.variant_type == true){
    vid = data.vid.variant_item_1.name;
    if(data.vid.variant_item_2 !== null){
      vid += '-' + data.vid.variant_item_2.name;
      if(e.data.list[i].vid.variant_item_3 !== null){
        vid += '-' + e.data.list[i].vid.variant_item_3.name;
        if(e.data.list[i].vid.variant_item_4 !== null){
          vid += '-' + e.data.list[i].vid.variant_item_4.name;
        }
      }
    }
  }else{
    vid = '-'
  }
  if(data.pid.measurement.status=='00'){
    measurement = data.pid.measurement.name
  }
  if(data.pid.variant_type == true){
    vid_id = data.vid.id;
  }
  $('.table_body').append(
    '<div class="table_row table_row_' + row + '" data-row="' + row + '">' +
    '<div class="item_column item_column_' + row + '">' +
    data.pid.name +
    '</div>' +
    '<div class="variant_column variant_column_' + row + '">' +
    vid +
    '</div>' +
    '<div class="total_unit_column">' +
    formatNumber(data.fs) +
    '</div>' +
    '<div class="total_unit_column">' +
    '<input data-pid="' + data.pid.id + '" data-variant="' + data.pid.variant_type + '" ' +
    'data-vid="' + vid_id + '" data-system="' + data.fs + '" data-deviation="0" ' +
    'class="total_unit total_unit_actual total_unit_actual_' + row + '" type="number" placeholder="0">' +
    '</div>' +
    '<div class="unit unit_' + row + '">' + measurement + '</div>' +
    '<div class="total_unit_column total_unit_column_deviation_' + row + '">' +
    '0' +
    '</div>' +
    '</div>'
  )

  _calculate_row(row);


}

function _calculate_row(row){
  $('.total_unit_actual_' + row).on('keyup', function(){
    let _system = parseInt($(this).attr('data-system')),
        _actual = parseInt($(this).val());
    if($(this).val().length > 0){
      $(this).val(_actual)
      let _deviation = _actual - _system;
      $('.total_unit_column_deviation_' + row).text(_deviation)
      $(this).attr('data-deviation', _deviation)
    }else{
      $('.total_unit_column_deviation_' + row).text(0)
      $(this).attr('data-deviation', 0)
    }
  });
}

function _submit_form(){
  $('#form_add_stock_opname').submit(function(e){
    _loading(1);
    e.preventDefault();

    let _data = $('.total_unit_actual'), _data_list = []
    for(i=0;i<_data.length;i++){
      if($(_data[i]).val().length !== 0 && parseInt($(_data[i]).attr('data-deviation')) !== 0){
        _detail_data = [
          $(_data[i]).attr('data-pid'),
          $(_data[i]).attr('data-variant'),
          $(_data[i]).attr('data-vid'),
          parseInt($(_data[i]).attr('data-system')),
          parseInt($(_data[i]).attr('data-deviation')),
        ]
      }else{
        _detail_data = [
          $(_data[i]).attr('data-pid'),
          $(_data[i]).attr('data-variant'),
          $(_data[i]).attr('data-vid'),
          parseInt($(_data[i]).attr('data-system')),
          0
        ]
      }
      _data_list.push(_detail_data);
    }
    $.post('/v1/api/data/stock',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 13,
        outlet: $('#outlet').val(),
        description: $('#description').val(),
        data_list: _data_list,
      })
    }, function (e) {
      if(e.status == '00'){
        sub_href('/page/inventory/stock-opname')
      }
    }).done(function(){
      _loading(0)
    })
  })
}
