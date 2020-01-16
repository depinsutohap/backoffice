function _tax(){
  _tax_list();
  _submit_data_tax();
}

// ========================================================
// TAX & SERVICES LIST
// ========================================================

// CALL THE users
function _tax_list(){
  _loading(1);
  $.post('/v1/api/data/tax',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 0,
    })
  }, function (e) {
    console.log(e);
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
      _check_outlet_detail('add');
      _check_outlet_detail('edit');
    }

    if(e.type.length>0){
      for(i=0; i<e.type.length; i++){
        $('#add_tax_type, #edit_tax_type').append(
          '<option value="' + e.type[i].id + '">' + e.type[i].name + '</option>'
        )
      }
    }
    if(e.data.length > 0){
      $('.no_data').remove()
      for(i=0; i<e.data.length; i++){
        $('#data_body').append(
          '<tr id="data_tax_' + e.data[i].id + '">'+
          '<td><input class="check_data" value="' + e.data[i].id + '" type="checkbox"></td>'+
          '<td class="data_tax_name_' + e.data[i].id + '">' + e.data[i].name + '</td>'+
          '<td class="data_tax_type_' + e.data[i].id + '">' + e.data[i].tax_type.name + '</td>'+
          '<td class="data_tax_value_' + e.data[i].id + '">' + e.data[i].value + '</td>'+
          '<td>' +
          '<div class="menu">'+
          '<i class="fas fa-ellipsis-h"></i>'+
          '<div class="menu_dropdown">'+
          '<a onclick="_open_tax_modal(' + e.data[i].id + ')">Edit</a>'+
          '<a class="logout" onclick="_remove_tax_modal(' + e.data[i].id + ')">Remove</a>'+
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
}

// OPEN AND GET THE TAX DATA
function _open_tax_modal(_id){
  $.post('/v1/api/data/tax',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 2,
      tax_id: _id,
    })
  }, function (e) {
    console.log(e)
      if(e.status == '00'){
        $('#edit_tax_modal_title').text(e.data.name);
        $('#edit_tax_name').val(e.data.name);
        $('#edit_tax_type').val(e.data.tax_type.id);
        $('#edit_tax_value').val(e.data.value);

        $('.edit_check_all').prop('checked', false).change()
        for(i=0; i < e.data.outlet_list.length; i++){
          $('.edit_check_data_' + e.data.outlet_list[i].id).prop('checked', true).change()
        }

        $('#edit_tax_id').val(e.data.id);
        open_sideform('edit_tax_modal');
      }
    }).fail(function(){
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

// OPEN AND GET THE TAX DATA TO REMOVE MODAL
function _remove_tax_modal(_id){
  $.post('/v1/api/data/tax',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 2,
      tax_id: _id,
    })
  }, function (e) {
      if(e.status == '00'){
        $('#remove_tax_modal_title').text(e.data.name);
        $('#remove_tax_id').val(e.data.id);
        open_sideform('remove_tax_modal');
      }
    }).fail(function(){
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}


// SUBMIT FORM ALL TAX (ADD, EDIT, REMOVE)
function _submit_data_tax(){
  // SUBMIT NEW TAX & SERVICES
  $('form#form_add_tax').submit(function(e){
    e.preventDefault();
    _loading(1);


    let input_outlet=$('.add_check_data:checked'); outlet_list=[];
    for(i=0; i<input_outlet.length;i++){
      outlet_list.push($(input_outlet[i]).val())
    }

    $.post('/v1/api/data/tax',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 1,
        tax_name: $('#add_tax_name').val(),
        tax_type_id: $('#add_tax_type').val(),
        tax_value: $('#add_tax_value').val(),
        outlet_list: outlet_list,
      })
    }, function (e) {
        if(e.status == '00'){
          $('#tax_name').val('');
          $('#data_body').prepend(
            '<tr id="data_tax_' + e.data.id + '">'+
            '<td><input class="check_data" value="' + e.data.id + '" type="checkbox"></td>'+
            '<td class="data_tax_name_' + e.data.id + '">' + e.data.name + '</td>'+
            '<td class="data_tax_type_' + e.data.id + '">' + e.data.tax_type.name + '</td>'+
            '<td class="data_tax_value_' + e.data.id + '">' + e.data.value + '</td>'+
            '<td>' +
            '<div class="menu">'+
            '<i class="fas fa-ellipsis-h"></i>'+
            '<div class="menu_dropdown">'+
            '<a onclick="_open_tax_modal(' + e.data.id + ')">Edit</a>'+
            '<a class="logout" onclick="_remove_tax_modal(' + e.data.id + ')">Remove</a>'+
            '</div>'+
            '</div>'+
            '</td>'+
            '</tr>'
          )
          $('.no_data').css('display', 'none');
          close_sideform();
          _menu_dropdown();_check();
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT EDIT DATA TAX & SERVICES
  $('form#form_edit_tax').submit(function(e){
    e.preventDefault();
    _loading(1);

    let input_outlet=$('.edit_check_data:checked'); outlet_list=[];
    for(i=0; i<input_outlet.length;i++){
      outlet_list.push($(input_outlet[i]).val())
    }

    $.post('/v1/api/data/tax',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 3,
        tax_name: $('#edit_tax_name').val(),
        tax_type_id: $('#edit_tax_type').val(),
        tax_value: $('#edit_tax_value').val(),
        tax_id: $('#edit_tax_id').val(),
        outlet_list: outlet_list,
      })
    }, function (e) {
        if(e.status == '00'){
          $('#edit_tax_name').val('');
          $('#edit_tax_id').val('')
          $('.data_tax_name_' + e.data.id).text(e.data.name);
          $('.data_tax_type_' + e.data.id).text(e.data.tax_type.name);
          $('.data_tax_value_' + e.data.id).text(e.data.value);
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT REMOVE DATA TAX & SERVICES
  $('form#form_remove_tax').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/tax',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 4,
        tax_id: $('#remove_tax_id').val(),
      })
    }, function (e) {
        if(e.status == '00'){
          $('#remove_tax_id').val('');
          if(e.data.status == '00'){
            $('#data_tax_' + e.data.id).remove();
          }
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT REMOVE MANY DATA TAX & SERVICES
  $('form#form_remove_many_tax').submit(function(e){
    e.preventDefault();
    _loading(1);

    let tax_list = []
    $('.check_data:checked').each(function() {
        tax_list.push($(this).val());
    });

    $.post('/v1/api/data/tax',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 5,
        tax_list: tax_list,
      })
    }, function (e) {
        if(e.status == '00'){
          for(i=0; i<e.data.length; i++){
            if(e.data[i].status == '00'){
              $('#data_tax_' + e.data[i].id).remove();
            }else{

            }
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

function _check_outlet_detail(t){
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
