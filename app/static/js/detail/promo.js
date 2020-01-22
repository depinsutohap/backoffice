// ========================================================
// FUNCTION FOR PROMO INDEX
// ========================================================
function _promo_index(){
  $.post('/v1/api/data/promo',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 0,
    })
  }, function (e) {
    $('.total_special_promo').text(e.data_sp);
    $('.total_auto_promo').text(e.data_ap);
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}


// ========================================================
// FUNCTION FOR SPECIAL PROMO
// ========================================================

function _special_promo(){
  $.post('/v1/api/data/promo',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 1,
    })
  }, function (e) {

    if(e.outlet_list.length > 0){
      let table = ['add_', 'edit_'];
      for(m=0; m<table.length; m++){
        $('.' + table[m] + 'outlet_list').empty()
        for(i=0; i<e.outlet_list.length; i++){
          $('.' + table[m] + 'outlet_list').append(
            '<tr id="' + table[m] + 'data_category_' + e.outlet_list[i].id + '">'+
            '<td><input class="' + table[m] + 'check_data ' + table[m] + 'check_data_' + e.outlet_list[i].id + '" value="' + e.outlet_list[i].id + '" type="checkbox"></td>'+
            '<td class="' + table[m] + 'data_promo_name_' + e.outlet_list[i].id + '">' + e.outlet_list[i].name + '</td>'+
            '</td>'+
            '</tr>'
          )
        }
      }
      _check_outlet_promo('add');
      _check_outlet_promo('edit');
    }

    let promo_value;
    if(e.data.length > 0){
      $('.no_data').remove()
      $('#data_body').empty()
      for(i=0; i<e.data.length; i++){
        promo_value = e.data[i].value + '%'
        if(e.data[i].percent != true){
          promo_value = 'Rp ' + e.data[i].value
        }
        $('#data_body').append(
          '<tr id="data_promo_' + e.data[i].id + '">'+
          '<td><input class="check_data" value="' + e.data[i].id + '" type="checkbox"></td>'+
          '<td class="data_promo_name_' + e.data[i].id + '">' + e.data[i].name + '</td>'+
          '<td class="data_promo_value_' + e.data[i].id + '">' + promo_value + '</td>'+
          '<td>' +
          '<div class="menu">'+
          '<i class="fas fa-ellipsis-h"></i>'+
          '<div class="menu_dropdown">'+
          '<a onclick="_open_promo_modal(' + e.data[i].id + ')">Edit</a>'+
          '<a class="logout" onclick="_remove_promo_modal(' + e.data[i].id + ')">Remove</a>'+
          '</div>'+
          '</div>'+
          '</td>'+
          '</tr>'
        )
      }
      _menu_dropdown();_check();
    }else{
      $('.no_data').css('display', 'flex');
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });



  _check_applied_day_promo('add');
  _check_applied_day_promo('edit');
  _show_applied('add', '_special_promo_date_status', '_promo_date');
  _show_applied('edit', '_special_promo_date_status', '_promo_date');
  _show_applied('add', '_special_promo_applied_status', '_applied_time');
  _show_applied('edit', '_special_promo_applied_status', '_applied_time');
  _submit_data_special_promo();
}

// OPEN AND GET THE SPECIAL PROMO DATA
function _open_promo_modal(id){
  $.post('/v1/api/data/promo',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 3,
      promo_id: id,
    })
  }, function (e) {
      if(e.status == '00'){
        $('#edit_special_promo_modal_title').text(e.data.name);
        $('#edit_special_promo_name').val(e.data.name);
        $('#edit_special_promo_percent_type').val('0')
        if(e.data.percent == false){
          $('#edit_special_promo_percent_type').val('1')
        }
        $('#edit_special_promo_value').val(e.data.value)
        if(e.data.promo_date_status == false){
          $('#edit_special_promo_date_status').prop('checked', false).change()
          $('#edit_special_promo_start_date').val('')
          $('#edit_special_promo_end_date').val('')
        }else{
          $('#edit_special_promo_date_status').prop('checked', true).change()
          $('#edit_special_promo_start_date').val(e.data.startdate)
          $('#edit_special_promo_end_date').val(e.data.enddate)
        }
        $('.edit_applied_check_all').prop('checked', false).change()
        if(e.data.sunday == true){
          $('#edit_special_promo_sunday').prop('checked', true).change();
        }
        if(e.data.monday == true){
          $('#edit_special_promo_monday').prop('checked', true).change();
        }
        if(e.data.tuesday == true){
          $('#edit_special_promo_tuesday').prop('checked', true).change();
        }
        if(e.data.wednesday == true){
          $('#edit_special_promo_wednesday').prop('checked', true).change();
        }
        if(e.data.thursday == true){
          $('#edit_special_promo_thursday').prop('checked', true).change();
        }
        if(e.data.friday == true){
          $('#edit_special_promo_friday').prop('checked', true).change();
        }
        if(e.data.saturday == true){
          $('#edit_special_promo_saturday').prop('checked', true).change();
        }
        if(e.data.apply_time_status == false){
          $('#edit_special_promo_applied_status').prop('checked', false).change()
          $('#edit_special_promo_start_time').val('')
          $('#edit_special_promo_end_time').val('')
        }else{
          $('#edit_special_promo_applied_status').prop('checked', true).change()
          $('#edit_special_promo_start_time').val(e.data.starttime)
          $('#edit_special_promo_end_time').val(e.data.endtime)
        }
        $('.edit_check_all').prop('checked', false).change()
        for(i=0; i < e.data.outlet_list.length; i++){
          $('.edit_check_data_' + e.data.outlet_list[i].id).prop('checked', true).change()
        }
        $('#edit_special_promo_id').val(e.data.id);
        open_sideform('edit_special_promo_modal');
      }
    }).fail(function(){
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

// OPEN AND GET THE CATEGORY DATA
function _remove_promo_modal(id){
  $.post('/v1/api/data/promo',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 3,
      promo_id: id,
    })
  }, function (e) {
      if(e.status == '00'){
        $('#remove_special_promo_modal_title').text(e.data.name);
        $('#remove_special_promo_id').val(e.data.id);
        open_sideform('remove_special_promo_modal');
      }
    }).fail(function(){
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

function _clear_input_sp(t){
  $('#' + t + '_special_promo_name').val('')
  $('#' + t + '_special_promo_percent_type').val('0')
  $('#' + t + '_special_promo_value').val('')
  $('#' + t + '_special_promo_date_status').prop('checked', false).change()
  $('#' + t + '_special_promo_start_date').val('')
  $('#' + t + '_special_promo_end_date').val('')
  $('.' + t + '_applied_check_all').prop('checked', false).change()
  $('#' + t + '_special_promo_applied_status').prop('checked', false).change()
  $('#' + t + '_special_promo_start_time').val('')
  $('#' + t + '_special_promo_end_time').val('')
  $('.' + t + '_check_all').prop('checked', false).change()
  if(t == 'edit'){
    $('#edit_special_promo_modal_title').text('########')
    $('.' + t + '_special_promo_id').val('')
  }
}

// SUBMIT FORM ALL DATA (ADD, EDIT, REMOVE)
function _submit_data_special_promo(){
  // SUBMIT NEW SPECIAL PROMO
  $('form#form_add_special_promo').submit(function(e){
    e.preventDefault();
    _loading(1);

    let input_applied_day=$('.add_applied_check:checked'); applied_day=[];
    for(i=0; i<input_applied_day.length;i++){
      applied_day.push($(input_applied_day[i]).val())
    }

    let input_outlet=$('.add_check_data:checked'); outlet_list=[];
    for(i=0; i<input_outlet.length;i++){
      outlet_list.push($(input_outlet[i]).val())
    }

    $.post('/v1/api/data/promo',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 2,
        promo_name: $('#add_special_promo_name').val(),
        promo_percent_type: $('#add_special_promo_percent_type').val(),
        promo_value: $('#add_special_promo_value').val(),
        promo_date_status: $('#add_special_promo_date_status').is(':checked'),
        promo_start_date: $('#add_special_promo_start_date').val(),
        promo_end_date: $('#add_special_promo_end_date').val(),
        applied_day: applied_day,
        promo_applied_time_status: $('#add_special_promo_applied_status').is(':checked'),
        promo_start_time: $('#add_special_promo_start_time').val(),
        promo_end_time: $('#add_special_promo_end_time').val(),
        promo_outlet: outlet_list,
      })
    }, function (e) {
        if(e.status == '00'){
          if(e.data.status == '00'){
            promo_value = e.data.value + '%'
            if(e.data.percent != true){
              promo_value = 'Rp ' + e.data.value
            }
            $('#data_body').append(
              '<tr id="data_promo_' + e.data.id + '">'+
              '<td><input class="check_data" value="' + e.data.id + '" type="checkbox"></td>'+
              '<td class="data_promo_name_' + e.data.id + '">' + e.data.name + '</td>'+
              '<td class="data_promo_value_' + e.data.id + '">' + promo_value + '</td>'+
              '<td>' +
              '<div class="menu">'+
              '<i class="fas fa-ellipsis-h"></i>'+
              '<div class="menu_dropdown">'+
              '<a onclick="_open_promo_modal(' + e.data.id + ')">Edit</a>'+
              '<a class="logout" onclick="_remove_promo_modal(' + e.data.id + ')">Remove</a>'+
              '</div>'+
              '</div>'+
              '</td>'+
              '</tr>'
            )
            _clear_input_sp('add');
            $('.no_data').css('display', 'none');
            close_sideform();
            _menu_dropdown();_check();
            notif('success', 'Special Promo Added', 'a new special promo has been successfully added');
          }else{
            notif('danger', 'Add Special Promo Failed', e.data.message);
          }
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT EDIT DATA SPECIAL PROMO
  $('form#form_edit_special_promo').submit(function(e){
    e.preventDefault();
    _loading(1);

    let input_applied_day=$('.edit_applied_check:checked'); applied_day=[];
    for(i=0; i<input_applied_day.length;i++){
      applied_day.push($(input_applied_day[i]).val())
    }

    let input_outlet=$('.edit_check_data:checked'); outlet_list=[];
    for(i=0; i<input_outlet.length;i++){
      outlet_list.push($(input_outlet[i]).val())
    }
    console.log(outlet_list);

    $.post('/v1/api/data/promo',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 4,
        promo_id: $('#edit_special_promo_id').val(),
        promo_name: $('#edit_special_promo_name').val(),
        promo_percent_type: $('#edit_special_promo_percent_type').val(),
        promo_value: $('#edit_special_promo_value').val(),
        promo_date_status: $('#edit_special_promo_date_status').is(':checked'),
        promo_start_date: $('#edit_special_promo_start_date').val(),
        promo_end_date: $('#edit_special_promo_end_date').val(),
        applied_day: applied_day,
        promo_applied_time_status: $('#edit_special_promo_applied_status').is(':checked'),
        promo_start_time: $('#edit_special_promo_start_time').val(),
        promo_end_time: $('#edit_special_promo_end_time').val(),
        promo_outlet: outlet_list,
      })
    }, function (e) {
        if(e.status == '00'){
          if(e.data.status == '00'){
            promo_value = e.data.value + '%'
            if(e.data.percent != true){
              promo_value = 'Rp ' + e.data.value
            }

            $('.data_promo_name_' + e.data.id).text(e.data.name);
            $('.data_promo_value_' + e.data.id).text(promo_value);
            _clear_input_sp('edit');
            close_sideform();
            notif('success', 'Special Promo Edited', 'a special promo has been successfully edited');
          }else{
            notif('danger', 'Edit Special Promo Failed', e.data.message);
          }
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT REMOVE DATA CATEGORY
  $('form#form_remove_special_promo').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/promo',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 5,
        promo_id: $('#remove_special_promo_id').val(),
      })
    }, function (e) {
        if(e.status == '00'){
          if(e.status == '00'){
            $('#data_promo_' + $('#remove_special_promo_id').val()).remove();
            $('#remove_special_promo_id').val('');
          }
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT REMOVE MANY DATA CATEGORY
  $('form#form_remove_many_special_promo').submit(function(e){
    e.preventDefault();
    _loading(1);

    let promo_list = []
    $('.check_data:checked').each(function() {
        promo_list.push($(this).val());
    });

    $.post('/v1/api/data/promo',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 6,
        promo_list: promo_list,
      })
    }, function (e) {
        if(e.status == '00'){
          for(i=0; i<promo_list; i++){
            $('#data_promo_' + promo_list[i]).remove();
          }
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
        $('.check_all').prop('checked', false).change();
      });
  });
}


// ========================================================
// FUNCTION FOR AUTO PROMO
// ========================================================

function apid(id){
  userData['apid'] = id;
}

function _auto_promo_index(){
  $.post('/v1/api/data/promo',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 7,
    })
  }, function (e) {
    console.log(e)
    let promo_value;
    if(e.data.length > 0){
      $('.no_data').remove()
      $('#data_body').empty()
      for(i=0; i<e.data.length; i++){
        $('#data_body').append(
          '<tr id="data_promo_' + e.data[i].id + '">'+
          '<td><input class="check_data" value="' + e.data[i].id + '" type="checkbox"></td>'+
          '<td class="data_promo_name_' + e.data[i].id + '">' + e.data[i].name + '</td>'+
          '<td class="data_promo_date data_promo_date_' + e.data[i].id + '">' + e.data[i].promo_date + '</td>'+
          '<td class="data_promo_applied_day data_promo_applied_day_' + e.data[i].id + '">' + e.data[i].applied_day.toString().replace(/,/g, ', ') + '</td>'+
          '<td class="data_promo_applied_time data_promo_applied_time_' + e.data[i].id + '">' + e.data[i].applied_time + '</td>'+
          '<td>' +
          '<div class="menu">'+
          '<i class="fas fa-ellipsis-h"></i>'+
          '<div class="menu_dropdown">'+
          '<a onclick="_open_edit_auto_promo(' + e.data[i].id + ')">Edit</a>'+
          '<a class="logout" onclick="_remove_auto_promo_modal(' + e.data[i].id + ')">Remove</a>'+
          '</div>'+
          '</div>'+
          '</td>'+
          '</tr>'
        )
      }
      _menu_dropdown();_check();

      _submit_data_auto_promo();
    }else{
      $('.no_data').css('display', 'flex');
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function _add_auto_promo(){
  _loading(1)
  $.post('/v1/api/data/promo',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 8,
    })
  }, function (e) {
    console.log(e)
    if(e.outlet_list.length > 0){
      $('.add_outlet_list').empty()
      for(i=0; i<e.outlet_list.length; i++){
        $('.add_outlet_list').append(
          '<tr id="add_data_promo_' + e.outlet_list[i].id + '">'+
          '<td><input class="add_check_data add_check_data_' + e.outlet_list[i].id + '" value="' + e.outlet_list[i].id + '" type="checkbox"></td>'+
          '<td class="add_data_promo_name_' + e.outlet_list[i].id + '">' + e.outlet_list[i].name + '</td>'+
          '</td>'+
          '</tr>'
        )
      }
      _check_outlet_promo('add');
    }
    if(e.item_list.length > 0){
      $('.auto_promo_select_item').empty()
      $('.auto_promo_select_item').append(
        '<option value="0">Select an item</option>'
      )
      for(i=0; i<e.item_list.length; i++){
        $('.auto_promo_select_item').append(
          '<option value="' + e.item_list[i].id + '">' + e.item_list[i].name + '</option>'
        )
      }
    }
    if(e.category_list.length > 0){
      $('.auto_promo_select_category').empty()
      $('.auto_promo_select_category').append(
        '<option value="0">Select a category</option>'
      )
      for(i=0; i<e.category_list.length; i++){
        $('.auto_promo_select_category').append(
          '<option value="' + e.category_list[i].id + '">' + e.category_list[i].name + '</option>'
        )
      }
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });


  _check_auto_promo_type('add');
  _check_applied_day_promo('add');
  _show_applied('add', '_auto_promo_date_status', '_promo_date');
  _show_applied('add', '_auto_promo_applied_status', '_applied_time');
  _check_auto_promo_category('add', '1', 'buy');
  _check_auto_promo_category('add', '3', 'buy');
  _check_auto_promo_category('add', '3', 'get');
  _submit_data_auto_promo();
}

function _open_edit_auto_promo(id){
  apid(id);
  sub_href('/page/promo/edit-auto-promo')
}

function _edit_auto_promo(){
  _loading(1)
  $.post('/v1/api/data/promo',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'promo_id': userData['apid'],
      'status': 10,
    })
  }, function (e) {
    console.log(e)
    if(e.outlet_list.length > 0){
      $('.edit_outlet_list').empty()
      for(i=0; i<e.outlet_list.length; i++){
        $('.edit_outlet_list').append(
          '<tr id="edit_data_promo_' + e.outlet_list[i].id + '">'+
          '<td><input class="edit_check_data edit_check_data_' + e.outlet_list[i].id + '" value="' + e.outlet_list[i].id + '" type="checkbox"></td>'+
          '<td class="edit_data_promo_name_' + e.outlet_list[i].id + '">' + e.outlet_list[i].name + '</td>'+
          '</td>'+
          '</tr>'
        )
      }
      _check_outlet_promo('edit');
    }
    if(e.item_list.length > 0){
      $('.auto_promo_select_item').empty()
      $('.auto_promo_select_item').append(
        '<option value="0">Select an item</option>'
      )
      for(i=0; i<e.item_list.length; i++){
        $('.auto_promo_select_item').append(
          '<option value="' + e.item_list[i].id + '">' + e.item_list[i].name + '</option>'
        )
      }
    }
    if(e.category_list.length > 0){
      $('.auto_promo_select_category').empty()
      $('.auto_promo_select_category').append(
        '<option value="0">Select a category</option>'
      )
      for(i=0; i<e.category_list.length; i++){
        $('.auto_promo_select_category').append(
          '<option value="' + e.category_list[i].id + '">' + e.category_list[i].name + '</option>'
        )
      }
    }

    _check_auto_promo_type('edit');
    _check_applied_day_promo('edit');
    _show_applied('edit', '_auto_promo_date_status', '_promo_date');
    _show_applied('edit', '_auto_promo_applied_status', '_applied_time');
    _check_auto_promo_category('edit', '1', 'buy');
    _check_auto_promo_category('edit', '3', 'buy');
    _check_auto_promo_category('edit', '3', 'get');
    _submit_data_auto_promo();


    $('#edit_auto_promo_id').val(e.data.id);
    $('.edit_auto_promo_type_' + e.data.type).prop('checked', true).change();
    if(e.data.type == 1){
      $('#edit_auto_promo_1_buy_value').val(e.data.requirement_value)
      if(e.data.requirement_id == 1){
        $('#edit_auto_promo_1_buy_check_category').prop(false, true).change();
        $('#edit_auto_promo_1_buy_item').val(e.data.requirement_relation)
      }else{
        $('#edit_auto_promo_1_buy_check_category').prop('checked', true).change();
        $('#edit_auto_promo_1_buy_category').val(e.data.requirement_relation)
      }

      $('#edit_auto_promo_1_get_percent_type').val(e.data.reward_id)
      $('#edit_auto_promo_1_get_value').val(e.data.reward_value)
    }else if(e.data.type == 2){
      $('#edit_auto_promo_2_buy_value').val(e.data.requirement_value);
      $('#edit_auto_promo_2_get_percent_type').val(e.data.reward_id);
      $('#edit_auto_promo_2_get_value').val(e.data.reward_value);
    }else if(e.data.type == 3){
      $('#edit_auto_promo_3_buy_value').val(e.data.requirement_value)
      if(e.data.requirement_id == 1){
        $('#edit_auto_promo_3_buy_check_category').prop(false, true).change();
        $('#edit_auto_promo_3_buy_item').val(e.data.requirement_relation)
      }else{
        $('#edit_auto_promo_3_buy_check_category').prop('checked', true).change();
        $('#edit_auto_promo_3_buy_category').val(e.data.requirement_relation)
      }

      $('#edit_auto_promo_3_get_value').val(e.data.reward_value)
      if(e.data.reward_id == 1){
        $('#edit_auto_promo_3_get_check_category').prop(false, true).change();
        $('#edit_auto_promo_3_get_item').val(e.data.reward_relation)
      }else{
        $('#edit_auto_promo_3_get_check_category').prop('checked', true).change();
        $('#edit_auto_promo_3_get_category').val(e.data.reward_relation)
      }
      $('#edit_auto_promo_check_multiple').prop('checked', false).change();
      if(e.data.multiple == true){
        $('#edit_auto_promo_check_multiple').prop('checked', true).change();
      }
    }

    if(e.data.promo_date_status == false){
      $('#edit_auto_promo_date_status').prop('checked', false).change()
      $('#edit_auto_promo_start_date').val('')
      $('#edit_auto_promo_end_date').val('')
    }else{
      $('#edit_auto_promo_date_status').prop('checked', true).change()
      $('#edit_auto_promo_start_date').val(e.data.startdate)
      $('#edit_auto_promo_end_date').val(e.data.enddate)
    }
    $('.edit_applied_check_all').prop('checked', false).change()
    if(e.data.sunday == true){
      $('#edit_auto_promo_sunday').prop('checked', true).change();
    }
    if(e.data.monday == true){
      $('#edit_auto_promo_monday').prop('checked', true).change();
    }
    if(e.data.tuesday == true){
      $('#edit_auto_promo_tuesday').prop('checked', true).change();
    }
    if(e.data.wednesday == true){
      $('#edit_auto_promo_wednesday').prop('checked', true).change();
    }
    if(e.data.thursday == true){
      $('#edit_auto_promo_thursday').prop('checked', true).change();
    }
    if(e.data.friday == true){
      $('#edit_auto_promo_friday').prop('checked', true).change();
    }
    if(e.data.saturday == true){
      $('#edit_auto_promo_saturday').prop('checked', true).change();
    }
    if(e.data.apply_time_status == false){
      $('#edit_auto_promo_applied_status').prop('checked', false).change()
      $('#edit_auto_promo_start_time').val('')
      $('#edit_auto_promo_end_time').val('')
    }else{
      $('#edit_auto_promo_applied_status').prop('checked', true).change()
      $('#edit_auto_promo_start_time').val(e.data.starttime)
      $('#edit_auto_promo_end_time').val(e.data.endtime)
    }
    $('.edit_check_all').prop('checked', false).change()
    for(i=0; i < e.data.outlet_list.length; i++){
      $('.edit_check_data_' + e.data.outlet_list[i].id).prop('checked', true).change()
    }
    $('#edit_auto_promo_id').val(e.data.id);

  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });

}

// OPEN AND GET THE CATEGORY DATA
function _remove_auto_promo_modal(id){
  $.post('/v1/api/data/promo',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 12,
      promo_id: id,
    })
  }, function (e) {
      if(e.status == '00'){
        console.log(e)
        $('#remove_auto_promo_modal_title').text(e.data.name);
        $('#remove_auto_promo_id').val(e.data.id);
        open_sideform('remove_auto_promo_modal');
      }
    }).fail(function(){
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

function _check_auto_promo_type(t){
  $('.' + t + '_auto_promo_type').on('change', function(){
    $('.auto_promo_rule').css('display', 'none');
    $('.auto_promo_time_rule, .auto_promo_table, .auto_promo_' + $('.' + t + '_auto_promo_type:checked').val()).css('display', 'flex');
  })
}

function _check_auto_promo_category(x, y, z){
  $('#'+ x + '_auto_promo_' + y + '_' + z + '_check_category').on('change', function(){
    if($('#'+ x + '_auto_promo_' + y + '_' + z + '_check_category').is(':checked')){
        $('#'+ x + '_auto_promo_' + y + '_' + z + '_item').css('display', 'none')
        $('#'+ x + '_auto_promo_' + y + '_' + z + '_category').css('display', 'inherit')
    }else{
        $('#'+ x + '_auto_promo_' + y + '_' + z + '_item').css('display', 'inherit')
        $('#'+ x + '_auto_promo_' + y + '_' + z + '_category').css('display', 'none')
    }
  })
}

// SUBMIT FORM ALL DATA (ADD, EDIT, REMOVE)
function _submit_data_auto_promo(){
  // SUBMIT NEW SPECIAL PROMO
  $('form#form_add_auto_promo').submit(function(e){
    e.preventDefault();
    _loading(1);

    let type_id = $('.add_auto_promo_type:checked').val(),
        requirement_id = null,
        requirement_value = null,
        requirement_relation = 'None',
        reward_id = null,
        reward_value = null,
        reward_relation = 'None',
        multiple = false;

    if(type_id == undefined){
      type_id = ''
    }

    if(type_id == '1'){
      // Requirement
      requirement_value = $('#add_auto_promo_1_buy_value').val();
      requirement_id = 1;
      requirement_relation = $('#add_auto_promo_1_buy_item').val();
      if($('#add_auto_promo_1_buy_check_category').is(':checked')){
        requirement_id = 2;
        requirement_relation = $('#add_auto_promo_1_buy_category').val();
      }
      // Reward
      reward_value = $('#add_auto_promo_1_get_value').val();
      reward_id = $('#add_auto_promo_1_get_percent_type').val();
    }else if(type_id == '2'){
      // Requirement
      requirement_value = $('#add_auto_promo_2_buy_value').val();
      requirement_id = 3;
      // Reward
      reward_value = $('#add_auto_promo_2_get_value').val();
      reward_id = $('#add_auto_promo_2_get_percent_type').val();
    }else if(type_id == '3'){
      // Requirement
      requirement_value = $('#add_auto_promo_3_buy_value').val();
      requirement_id = 1;
      requirement_relation = $('#add_auto_promo_3_buy_item').val();
      if($('#add_auto_promo_3_buy_check_category').is(':checked')){
        requirement_id = 2;
        requirement_relation = $('#add_auto_promo_3_buy_category').val();
      }
      // Reward
      reward_value = $('#add_auto_promo_3_get_value').val();
      reward_id = 1;
      reward_relation = $('#add_auto_promo_3_get_item').val();
      multiple = $('#add_auto_promo_check_multiple').is(':checked');
      if($('#add_auto_promo_3_get_check_category').is(':checked')){
        reward_id = 2;
        reward_relation = $('#add_auto_promo_3_get_category').val();
      }
    }

    let input_applied_day=$('.add_applied_check:checked'); applied_day=[];
    for(i=0; i<input_applied_day.length;i++){
      applied_day.push($(input_applied_day[i]).val())
    }

    let input_outlet=$('.add_check_data:checked'); outlet_list=[];
    for(i=0; i<input_outlet.length;i++){
      outlet_list.push($(input_outlet[i]).val())
    }
    outlet_list;

    $.post('/v1/api/data/promo',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 9,
        type_id: type_id,
        requirement_id: requirement_id,
        requirement_value: requirement_value,
        requirement_relation: requirement_relation,
        reward_id: reward_id,
        reward_value: reward_value,
        reward_relation: reward_relation,
        multiple: multiple,
        promo_date_status: $('#add_auto_promo_date_status').is(':checked'),
        promo_start_date: $('#add_auto_promo_start_date').val(),
        promo_end_date: $('#add_auto_promo_end_date').val(),
        applied_day: applied_day,
        promo_applied_time_status: $('#add_auto_promo_applied_status').is(':checked'),
        promo_start_time: $('#add_auto_promo_start_time').val(),
        promo_end_time: $('#add_auto_promo_end_time').val(),
        promo_outlet: outlet_list,
      })
    }, function (e) {
        if(e.status == '00'){
          if(e.data.status == '00'){
            sub_href('/page/promo/auto-promo')
          }else{
            notif('danger', 'Add Auto Promo Failed', e.data.message);
          }
        }else{
          notif('danger', 'Add Auto Promo Failed', e.message);
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT EDIT DATA SPECIAL PROMO
  $('form#form_edit_auto_promo').submit(function(e){
    e.preventDefault();
    _loading(1);

    let type_id = $('.edit_auto_promo_type:checked').val(),
        requirement_id = null,
        requirement_value = null,
        requirement_relation = 'None',
        reward_id = null,
        reward_value = null,
        reward_relation = 'None',
        multiple = false;

    if(type_id == undefined){
      type_id = ''
    }

    if(type_id == '1'){
      // Requirement
      requirement_value = $('#edit_auto_promo_1_buy_value').val();
      requirement_id = 1;
      requirement_relation = $('#edit_auto_promo_1_buy_item').val();
      if($('#edit_auto_promo_1_buy_check_category').is(':checked')){
        requirement_id = 2;
        requirement_relation = $('#edit_auto_promo_1_buy_category').val();
      }
      // Reward
      reward_value = $('#edit_auto_promo_1_get_value').val();
      reward_id = $('#edit_auto_promo_1_get_percent_type').val();
    }else if(type_id == '2'){
      // Requirement
      requirement_value = $('#edit_auto_promo_2_buy_value').val();
      requirement_id = 3;
      // Reward
      reward_value = $('#edit_auto_promo_2_get_value').val();
      reward_id = $('#edit_auto_promo_2_get_percent_type').val();
    }else if(type_id == '3'){
      // Requirement
      requirement_value = $('#edit_auto_promo_3_buy_value').val();
      requirement_id = 1;
      requirement_relation = $('#edit_auto_promo_3_buy_item').val();
      if($('#edit_auto_promo_3_buy_check_category').is(':checked')){
        requirement_id = 2;
        requirement_relation = $('#edit_auto_promo_3_buy_category').val();
      }
      // Reward
      reward_value = $('#edit_auto_promo_3_get_value').val();
      reward_id = 1;
      reward_relation = $('#edit_auto_promo_3_get_item').val();
      multiple = $('#edit_auto_promo_check_multiple').is(':checked');
      if($('#edit_auto_promo_3_get_check_category').is(':checked')){
        reward_id = 2;
        reward_relation = $('#edit_auto_promo_3_get_category').val();
      }
    }

    let input_applied_day=$('.edit_applied_check:checked'); applied_day=[];
    for(i=0; i<input_applied_day.length;i++){
      applied_day.push($(input_applied_day[i]).val())
    }

    let input_outlet=$('.edit_check_data:checked'); outlet_list=[];
    for(i=0; i<input_outlet.length;i++){
      outlet_list.push($(input_outlet[i]).val())
    }
    outlet_list;

    $.post('/v1/api/data/promo',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 11,
        promo_id: $('#edit_auto_promo_id').val(),
        type_id: type_id,
        requirement_id: requirement_id,
        requirement_value: requirement_value,
        requirement_relation: requirement_relation,
        reward_id: reward_id,
        reward_value: reward_value,
        reward_relation: reward_relation,
        multiple: multiple,
        promo_date_status: $('#edit_auto_promo_date_status').is(':checked'),
        promo_start_date: $('#edit_auto_promo_start_date').val(),
        promo_end_date: $('#edit_auto_promo_end_date').val(),
        applied_day: applied_day,
        promo_applied_time_status: $('#edit_auto_promo_applied_status').is(':checked'),
        promo_start_time: $('#edit_auto_promo_start_time').val(),
        promo_end_time: $('#edit_auto_promo_end_time').val(),
        promo_outlet: outlet_list,
      })
    }, function (e) {
      if(e.status == '00'){
        if(e.data.status == '00'){
          sub_href('/page/promo/auto-promo')
        }else{
          notif('danger', 'Edit Auto Promo Failed', e.data.message);
        }
      }else{
        notif('danger', 'Edit Auto Promo Failed', e.message);
      }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT REMOVE DATA CATEGORY
  $('form#form_remove_auto_promo').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/promo',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 13,
        promo_id: $('#remove_auto_promo_id').val(),
      })
    }, function (e) {
        if(e.status == '00'){
          if(e.status == '00'){
            $('#data_promo_' + $('#remove_auto_promo_id').val()).remove();
            $('#remove_auto_promo_id').val('');
          }
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT REMOVE MANY DATA CATEGORY
  $('form#form_remove_many_auto_promo').submit(function(e){
    e.preventDefault();
    _loading(1);

    let promo_list = []
    $('.check_data:checked').each(function() {
        promo_list.push($(this).val());
    });

    $.post('/v1/api/data/promo',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 14,
        promo_list: promo_list,
      })
    }, function (e) {
      console.log(e)
      console.log(promo_list)
        if(e.status == '00'){
          for(i=0; i<promo_list.length; i++){
            console.log(promo_list[i])
            $('#data_promo_' + promo_list[i]).remove();
          }
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
        $('.check_all').prop('checked', false).change();
      });
  });
}


// ========================================================
// FUNCTION FOR PROMO
// ========================================================




function _check_outlet_promo(t){
  $('.' + t + '_check_all').on('change', function(){
    if($('.' + t + '_check_all').is(':checked')){
      $('.' + t + '_check_data').prop('checked', true);
    }else{
      $('.' + t + '_check_data').prop('checked', false);
    }
  })

  $('.' + t + '_check_data').on('change', function(){
    if($('.' + t + '_check_data:checked').length == $('.' + t + '_check_data').length){
      $('.' + t + '_check_all').prop('checked', true);
    }else{
      $('.' + t + '_check_all').prop('checked', false);
    }
  });
}

function _check_applied_day_promo(t){
  $('.' + t + '_applied_check_all').on('change', function(){
    if($('.' + t + '_applied_check_all').is(':checked')){
      $('.' + t + '_applied_check').prop('checked', true);
    }else{
      $('.' + t + '_applied_check').prop('checked', false);
    }
  })

  $('.' + t + '_applied_check').on('change', function(){
    if($('.' + t + '_applied_check:checked').length == $('.' + t + '_applied_check').length){
      $('.' + t + '_applied_check_all').prop('checked', true);
    }else{
      $('.' + t + '_applied_check_all').prop('checked', false);
    }
  });
}

function _show_applied(x, y, z){
  $('#' + x + y).on('change', function(){
    if($('#' + x + y).is(':checked')){
      $('.' + x + z).css('display', 'flex');
    }else{
      $('.' + x + z).css('display', 'none');
    }
  })
}
