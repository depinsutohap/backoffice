

// ========================================================
// FUNCTION FOR STOCK ENTRY LIST
// ========================================================

function stock_entry(){
  outlet_list(); _min_max_data();
  stock_entry_list();
}

function stock_entry_list(){
  $.post('/v1/api/data/stock',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 1,
      from_date: $('.from_date').val(),
      to_date: $('.to_date').val(),
      outlet: $('#outlet').val(),
    })
  }, function (e) {
    console.log(e)
    if(e.data.status == '00'){
      for(i=0;i<e.data.list.length;i++){
        $('#data_body').append(
          '<tr class="_click" onclick="_stock_entry_detail(' + e.data.list[i].id + ', ' + e.data.list[i].outlet.id + ')">' +
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

function _stock_entry_detail(id, outlet_id){
  _loading(1)
  $.post('/v1/api/data/stock',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 2,
      stock_id: id,
      outlet: outlet_id,
    })
  }, function (e) {
    console.log(e)
    if(e.data.status == '00'){
      $('#data_body_modal').empty()
      $('#stock_entry_modal_title').text(e.data.name)
      $('.stock_entry_outlet').text(e.data.outlet.business_id.name + ' - ' + e.data.outlet.name)
      $('.stock_entry_date').text(e.data.date)
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
        console.log(vid)
        let measurement = '';
        if(e.data.list[i].pid.measurement.status == '00'){
          measurement = e.data.list[i].pid.measurement.name
        }
        $('#data_body_modal').append(
          '<tr>' +
          '<td>' + e.data.list[i].pid.name + '</td>' +
          '<td>' + vid + '</td>' +
          '<td>' + formatNumber(e.data.list[i].quantity) + '</td>' +
          '<td>' + measurement + '</td>' +
          '<td>' + formatNumber(e.data.list[i].cost.value) + '</td>' +
          '<td>' + formatNumber(e.data.list[i].quantity * e.data.list[i].cost.value) + '</td>' +
          '</tr>'
        )
      }
    }
  }).done(function(){
    _loading(0)
  })
  open_sideform('stock_entry_modal')
}

// ========================================================
// FUNCTION FOR ADD STOCK ENTRY
// ========================================================


function add_stock_entry(){
  outlet_list(); $('#date').attr('max', _create_date(0)).val(_create_date(0));
  _appen_on_click();
  _submit_form();
}

function _appen_on_click(){
  row = 0;
  _append_row(row);
  row +=1;
  $('.add_row').on('click', function(){
    _append_row(row);
    row +=1;
  })
}

function _append_row(row){
  $('.table_body').append(
    '<div class="table_row table_row_' + row + '" data-row="' + row + '">' +
    '<div class="item_column item_column_' + row + '">' +
    '<input type="text" class="item item_' + row + '" data-variant="false" data-row="' + row + '" data-id="0" readonly>' +
    '<div class="div_search_stock div_search_stock_' + row + '">' +
    '<div class="stock_div_search_input">' +
    '<input class="stock_div_search_input_field stock_div_search_input_field_' + row + '" type="text">' +
    '</div>' +
    '<div class="stock_div_search_data stock_div_search_data_' + row + '">' +
    '<div class="waiting waiting_' + row + '">Waiting...</div>' +
    '<div class="task task_' + row + '">Insert at least 1 character or more..</div>' +
    '</div>' +
    '</div>' +
    '</div>' +
    '<div class="variant_column variant_column_' + row + '">' +
    '<span>-</span>' +
    '<select class="variant variant_' + row + '" data-row="' + row + '" data-pid="0"></select>' +
    '</div>' +
    '<div class="total_unit_column">' +
    '<input class="total_unit total_unit_' + row + '" type="number" placeholder="0" value="0">' +
    '</div>' +
    '<div class="unit unit_' + row + '"></div>' +
    '<div class="cost_unit_column">' +
    '<input class="cost_unit cost_unit_' + row + '" type="number" placeholder="0" value="0">' +
    '</div>' +
    '<div class="total_cost_column">' +
    '<input class="total_cost total_cost_' + row + '" type="number" placeholder="0" value="0">' +
    '</div>' +
    '<div class="trash_column">' +
    '<a onclick="_remove_row(' + row + ')"><i class="fas fa-trash"></i></a>' +
    '</div>' +
    '</div>'
  )

  _search_query(row);_calculate_row(row);


}

function _calculate_row(row){
  $('.total_unit_' + row + ', .cost_unit_' + row).on('change', function(){
    let _tu = parseInt($('.total_unit_' + row).val()),
        _cpu = parseInt($('.cost_unit_' + row).val());
    $('.total_cost_' + row).val(_tu * _cpu);
  });
  $('.total_cost_' + row).on('change', function(){
    let _tu = parseInt($('.total_unit_' + row).val()),
        _tc = parseInt($('.total_cost_' + row).val());
    $('.cost_unit_' + row).val(_tc / _tu);
  })
}


function _remove_row(row){
 $('.table_row_' + row).remove()
}

function _search_query(row){

  $('.item_' + row).on('click', function(){
    $('.div_search_stock_' + row).css('display', 'flex');
    $('.stock_div_search_input_field_' + row).val('').focus();
    $('.stock_div_search_data_' + row + ' > a').remove();
    $('.task_' + row).css('display', 'inherit');
    $('.waiting_' + row).css('display', 'none');
  });

  $('.item_column_' + row).on('mouseleave', function(){
    $('.div_search_stock_' + row).css('display', 'none');
    $('.stock_div_search_input_field_' + row).val('').blur();
    $('.task_' + row).css('display', 'inherit');
    $('.waiting_' + row).css('display', 'none');
  });

  $('.stock_div_search_input_field_' + row).on('keyup', function(e){
    if($(this).val().length > 0){
      $('.stock_div_search_data_' + row + ' > a').remove();
      $('.waiting_' + row).css('display', 'inherit');
      $('.task_' + row).css('display', 'none');
      let input_except = $('.item');
      let except = []
      for(i=0; i < input_except.length; i++){
        if($(input_except[i]).val().trim().length > 0 && $(input_except[i]).data('id') !== 0){
          if(except.length > 0){ // If Except list is more than 0
            let _data_0 = [];
            for(x=0; x<except.length;x++){
              _data_0.push(except[x][0])
            }
            if(_data_0.includes($(input_except[i]).attr('data-id'))){
              for(x=0; x<except.length;x++){
                if(except[x][0] == $(input_except[i]).attr('data-id') && except[x][1] == 'true'){
                  if(except[x][2].includes($('.variant_' + $(input_except[i]).attr('data-row'))) == 'false'){
                    except[x][2].push($('.variant_' + $(input_except[i]).attr('data-row')).val());
                  }
                }else{
                  let detail_except = [$(input_except[i]).attr('data-id'), $(input_except[i]).attr('data-variant'), []]
                  if($(input_except[i]).attr('data-variant') !== 'false'){
                    detail_except[2].push($('.variant_' + $(input_except[i]).attr('data-row')).val())
                  }
                  except.push(detail_except);
                }
              }
            }else{
              let detail_except = [$(input_except[i]).attr('data-id'), $(input_except[i]).attr('data-variant'), []]
              if($(input_except[i]).attr('data-variant') !== 'false'){
                detail_except[2].push($('.variant_' + $(input_except[i]).attr('data-row')).val())
              }
              except.push(detail_except);
            }
          }else{
            let detail_except = [$(input_except[i]).attr('data-id'), $(input_except[i]).attr('data-variant'), []]
            if($(input_except[i]).attr('data-variant') !== 'false'){
              detail_except[2].push($('.variant_' + $(input_except[i]).attr('data-row')).val())
            }
            except.push(detail_except);
          }
        }
      }
      $.post('/v1/api/data/search',{
        data: JSON.stringify({
          id: userData['id'],
          token: userData['token'],
          status: 5,
          q: $(this).val().trim(),
          except: except,
        })
      }, function(e){
        console.log(e)
        $('.stock_div_search_data_' + row + ' > a').remove();
        if(e.status == '00'){
          $('.waiting_' + row).css('display', 'none');
          if(e.q.length > 0){
            for(i=0; i<e.q.length; i++){
              $('.stock_div_search_data_' + row).append(
                '<a class="stock_options" onclick="choose_stock_option(\'' + row +'\', \'' + e.q[i][0] + '\', \'' + e.q[i][1] + '\', \'' + e.q[i][2] + '\')">' + e.q[i][1] + '</a>'
              )
            }
          }else{
            $('.ingredients_div_search_data_pid_' + pid + '_vid_' + vid + '_row_' + row + ' > a').remove();
            $('.waiting_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'inherit');
          }
        }
      })
    }else{
      $('.stock_div_search_data_' + row + ' > a').remove();
      $('.task_' + row).css('display', 'inherit');
      $('.waiting_' + row).css('display', 'none');
    }
  }).on('keydown', function(e){
    if (e.keyCode == 13) {return false;}
  })
}

function choose_stock_option(row, id, name, variant){
  $('.item_' + row).val(name).attr('data-id', id).attr('data-variant', variant)
  $('.div_search_stock_' + row).css('display', 'none');
  if(variant == 'true'){
    let input_except = $('.item');
    let except = []
    for(i=0; i < input_except.length; i++){
      if($(input_except[i]).val().trim().length > 0 && $(input_except[i]).data('id') !== '0'){
        if($(input_except[i]).data('id') == id){
          let _data_value = $('.variant_' + $(input_except[i]).data('row')).val()
          if(except.includes(_data_value) == false && _data_value !== null){
            except.push(_data_value)
          }
        }

      }
    }
    $.post('/v1/api/data/search',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 6,
        ipid: id,
        except: except,
      })
    }, function(e){
      if(e.status == '00'){
        $('.variant_' + row).empty().prop('disabled', false).append(
          '<option value="0">Pilih Variant</option>'
        )
        for(i=0; i<e.q.length; i++){
          let _name = e.q[i].variant_item_1.name;
          if(e.q[i].variant_item_2 !== null){
            _name += '-' + e.q[i].variant_item_2.name;
            if(e.q[i].variant_item_3 !== null){
              _name += '-' + e.q[i].variant_item_3.name;
              if(e.q[i].variant_item_4 !== null){
                _name += '-' + e.q[i].variant_item_4.name;
              }
            }
          }
          $('.variant_' + row).append(
            '<option value="' + e.q[i].id + '">' + _name + '</option>'
          )
        }
        $('.variant_' + row).attr('data-pid', id)
        $('.variant_' + row).css('display', 'inherit');
        $('.stock_div_search_input_field_' + row).val('').blur();
        $('.task_' + row).css('display', 'inherit');
        $('.waiting_' + row).css('display', 'none');
      }
    }).done(function(e){

    });

  }else{
    $('.variant_' + row).css('display', 'none');
  }

  $('.variant_' + row).on('change', function(){
    $(this).prop('disabled', true);
  })
}

function _submit_form(){
  $('#form_add_stock_entry').submit(function(e){
    _loading(1);
    e.preventDefault();

    let _data = $('.item'), _data_list = []
    for(i=0;i<_data.length;i++){
      if($(_data[i]).attr('data-id') == '0'){
        notif('info', 'Don\'t forget to fill your item item to add the stock entry');
        return false;
      }else{
        let row = $(_data[i]).attr('data-row')
        let _tu = parseInt($('.total_unit_' + row).val()),
            _cpu = parseInt($('.cost_unit_' + row).val()),
            _tc = parseInt($('.total_cost_' + row).val()),
            _detail_data = [$(_data[i]).attr('data-id'), $(_data[i]).attr('data-variant'), '0', _tu, _cpu, _tc]
        if($(_data[i]).attr('data-variant') == 'true'){
          if($('.variant_' + row).val() !== '0'){
            _detail_data[2] = $('.variant_' + row).val();
          }else{
            notif('info', 'Don\'t forget to choose your variant to add the stock entry');
            return false;
          }
        }
        _data_list.push(_detail_data)
      }
    }
    $.post('/v1/api/data/stock',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 3,
        date: $('#date').val(),
        outlet: $('#outlet').val(),
        description: $('#description').val(),
        data_list: _data_list,
      })
    }, function (e) {
      if(e.status == '00'){
        sub_href('/page/inventory/stock-entry')
      }
    }).done(function(){
      _loading(0)
    })
  })
}
