// ========================================================
// FUNCTION OPEN PAGE
// ========================================================

function _business(){
  let bid = localStorage.b_id;
  _business_data(bid);
  _outlet_list_with_exception(bid);
  _move_outlet_current();
  _detail_page('overview');
}

function _business_overview(){
  let bid = localStorage.b_id;
  _outlet_list(bid);
}



function _detail_page(t){
  _loading(1);
  $('.detail_header').removeClass('active');
  $('#detail_' + t).addClass('active');
  $('#detailSection').load('/page/business/section/' + t);
}


// ========================================================
// Business Data
// ========================================================

// LIST FUNCTIONS
function _business_data(b_id){
  _loading(1);
  $.post('/v1/api/data/business',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 1,
      'bid': b_id
    })
  }, function (e) {
    $('#business_name, .move_outlet_title_business_name').text(e.data.name);
    $('#title_business_category').text(e.data.business_category_id.name);
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  });
}


// OUTLET LIST WITH AN EXCEPTION FOR MOVE OUTLET INTO CURRENT EXISTING BUSINESS
function _outlet_list_with_exception(b_id){
  _loading(1);
  $.post('/v1/api/data/business',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 9,
      'business_id': b_id
    })
  }, function (e) {
    for(i=0; i < e.data.length; i++){
      $('#move_list_outlet_into_business').prepend(
        '<option value="' + e.data[i].id + '">' + e.data[i].name + '</option>'
      );
    }

  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  });
}

function _move_outlet_current(){
  $('form#form_move_outlet_business').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/business',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 5,
        outlet_list: $('#move_list_outlet_into_business').val(),
        business_id: userData['b_id'],
      })
    }, function (e) {
        if(e.status == '00'){
          b_id(e.business_id);
          nav_href_business('business', e.business_id);
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      });
  });
}



function _outlet_list(b_id){
  _loading(1);
  _country_list('edit_outlet_country');
  _outlet_num_emp('edit_outlet_numemp');
  submit_edit_outlet();submit_remove_outlet();
  $.post('/v1/api/data/business',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 3,
      'bid': b_id
    })
  }, function (e) {
    for(i=0;i < e.tax_list.length; i++){
      $('#edit_outlet_tax').append(
        '<option value="' + e.tax_list[i].id + '">' + e.tax_list[i].name + '</option>'
      )
    }
    for(i=0; i<e.category_list.length;i++){
      $('.category_list_data').append(
        '<div class="colum_input">' +
        '<p>' + e.category_list[i].name + '</p>' +
        '<div class="div_input">' +
        '<label class="switch">' +
        '<input class="category_check_permission category_check_permission_' + e.category_list[i].id + '" value="' + e.category_list[i].id + '" type="checkbox">' +
        '<span class="slider"></span>' +
        '</label>' +
        '</div>' +
        '</div>'
      )
    }
    for(i=0; i<e.item_list.length;i++){
      $('.item_list_data').append(
        '<div class="colum_input">' +
        '<p>' + e.item_list[i].name + '</p>' +
        '<div class="div_input">' +
        '<label class="switch">' +
        '<input class="item_check_permission item_check_permission_' + e.item_list[i].id + '" value="' + e.item_list[i].id + '" type="checkbox">' +
        '<span class="slider"></span>' +
        '</label>' +
        '</div>' +
        '</div>'
      )
    }
    if(e.list.length > 0){
      for(i=0;i < e.list.length; i++){
        _append_overview_list(e.list[i]);
      }
    }else{
      $('.no_data').css('display', 'flex')
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function _append_overview_list(data){
  let _tax = 'No Tax';
  if(data.tax_list.length>0){
    _tax = 'Taxes applied';
  }


  $('._list_table').append(
    '<div class="list_data list_data_' + data.id + '">' +
    '<div class="accordion" data-target="' + data.id + '" onclick="toggle_accordion(this)">' +
    '<div class="_column column_status">' +
    '<div class="status_dot active"></div>' +
    '</div>' +
    '<div class="_column column_name">' +
    '<p class="outlet_name_' + data.id + '">'+ data.name + '</p>' +
    '</div>' +
    '<div class="_column column_phone">' +
    '<p class="outlet_phone_' + data.id + '">' + data.phone_number + '</p>' +
    '</div>' +
    '<div class="_column column_transactions">' +
    '<p class="outlet_tax_' + data.id + '">' + _tax + '</p>' +
    '</div>' +
    '<div class="_column column_more">' +
    '<a class="fa fa-ellipsis-h"></a>' +
    '</div>' +
    '</div>' +
    '<div id="accordion_' + data.id + '" class="accordion_collapse collapse">' +
    '<div class="_row">' +
    '<div class="col_4">' +
    '<div class="_data">' +
    '<p class="key">Business</p>' +
    '<p class="value" class="outlet_business_' + data.id + '">' + data.business_id.name + '</p>' +
    '</div>' +
    '<div class="_data">' +
    '<p class="key">Employee</p>' +
    '<p class="value" class="outlet_numpemp_' + data.id + '">' + data.num_emp.name + '</p>' +
    '</div>' +
    '<div class="_data">' +
    '<p class="key">Membership</p>' +
    '<p class="value">' + data.billing.name + '</p>' +
    '</div>' +
    '<div class="_data">' +
    '<p class="key">Product Category</p>' +
    '<p class="value"><span class="total_category_outlet_' + data.id + '">' + data.total_category + '</span><a class="edit_button" onclick="_edit_category_outlet(' + data.id + ')">Edit</a></p>' +
    '</div>' +
    '</div>' +
    '<div class="col_4">' +
    '<div class="_data">' +
    '<p class="key">Address</p>' +
    '<p class="value" class="outlet_address_' + data.id + '">' + data.address + '</p>' +
    '</div>' +
    '<div class="_data">' +
    '<p class="key">Country</p>' +
    '<p class="value" class="outlet_country_' + data.id + '">' + data.country.name + '</p>' +
    '</div>' +
    '<div class="_data">' +
    '<p class="key">Expiry Date</p>' +
    '<p class="value" class="outlet_country_' + data.id + '">' + data.billing.expired + '</p>' +
    '</div>' +
    '<div class="_data">' +
    '<p class="key">Product Item</p>' +
    '<p class="value"><span class="total_item_outlet_' + data.id + '">' + data.total_item + '</span><a class="edit_button" onclick="_edit_item_outlet(' + data.id + ')">Edit</a></p>' +
    '</div>' +
    '</div>' +
    '<div class="col_2">' +
    // '<div class="_data _menu">' +
    // '<a onclick="_edit_outlet(' + data.id + ')">Table</a>' +
    // '</div>' +
    '<div class="_data _menu">' +
    '<a onclick="_edit_outlet(' + data.id + ')">Edit</a>' +
    '</div>' +
    '<div class="_data _menu">' +
    '<a onclick="_remove_outlet(' + data.id + ')">Remove</a>' +
    '</div>' +
    '</div>' +
    '</div>' +
    '</div>' +
    '</div>'
  )
}


function _edit_outlet(t){
  $.post('/v1/api/data/business',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 10,
      'outlet_id': t
    })
  }, function (e) {
    $('#edit_outlet_modal_title').text(e.data.name);
    $('#edit_outlet_id').val(e.data.id);
    $('#edit_outlet_name').val(e.data.name);
    $('#edit_outlet_numemp').val(e.data.num_emp.id);
    $('#edit_outlet_phone').val(e.data.phone_number);
    $('#edit_outlet_address').val(e.data.address);
    $('#edit_outlet_country').val(e.data.country.id);

    for(i=0; i<e.data.tax_list.length;i++){
      $('.dropdown').dropdown('set selected', e.data.tax_list[i]);
    }

    $('#edit_table_module_id').prop('checked', false);
    if(e.data.table_status == true){
      $('#edit_table_module_id').prop('checked', true);
    }


    open_sideform('edit_outlet_modal');
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function _edit_category_outlet(t){
  $.post('/v1/api/data/business',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 13,
      'outlet_id': t
    })
  }, function (e) {
    console.log(e)
    if(e.status == '00'){
      $('#edit_category_outlet_modal_title').text(e.data.name);
      $('#edit_category_outlet_id').val(e.data.id);
      $('#category_check_permission').prop('checked', false);
      for(i=0;i<e.list.length;i++){
        $('.category_check_permission_' + e.list[i].id).prop('checked', true);
      }
    }
  open_sideform('edit_category_outlet_modal');
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function _edit_item_outlet(t){
  $.post('/v1/api/data/business',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 15,
      'outlet_id': t
    })
  }, function (e) {
    console.log(e)
    if(e.status == '00'){
      $('#edit_item_outlet_modal_title').text(e.data.name);
      $('#edit_item_outlet_id').val(e.data.id);
      $('#item_check_permission').prop('checked', false);
      for(i=0;i<e.list.length;i++){
        $('.item_check_permission_' + e.list[i].id).prop('checked', true);
      }
    }
  open_sideform('edit_item_outlet_modal');
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function submit_edit_outlet(){
  $('form#form_edit_outlet').submit(function(e){
    e.preventDefault();
    let _tax_list = [], table_status = false;
    if($('#edit_outlet_tax').val() !== null){
      _tax_list = $('#edit_outlet_tax').val();
    }
    if($('#edit_table_module_id').is(':checked')){
      table_status = true;
    }
    $.post('/v1/api/data/business',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 11,
        outlet_id: $('#edit_outlet_id').val(),
        outlet_name:$('#edit_outlet_name').val(),
        outlet_numemp:$('#edit_outlet_numemp').val(),
        outlet_phone:$('#edit_outlet_phone').val(),
        outlet_address:$('#edit_outlet_address').val(),
        outlet_country:$('#edit_outlet_country').val(),
        outlet_tax:_tax_list,
        table_status: table_status
      })
    }, function (e) {

      if(e.status == '00'){
        $('.outlet_name_' + e.data.id).text(e.data.name)
        $('.outlet_phone_' + e.data.id).text(e.data.phone_number)

        let _tax = 'No Tax';
        if(e.data.tax_list.length>0){
          _tax = 'Taxes applied';
        }
        $('.outlet_tax_' + e.data.id).text(_tax)


        $('.outlet_business_' + e.data.id).text(e.data.business_id.name)
        $('.outlet_business_' + e.data.id).text(e.data.num_emp.name)
        $('.outlet_address_' + e.data.id).text(e.data.address)
        $('.outlet_country_' + e.data.id).text(e.data.country)

        $('#edit_outlet_id').val('');
        $('#edit_outlet_name').val('');
        $('#edit_outlet_numemp').val('');
        $('#edit_outlet_phone').val('');
        $('#edit_outlet_address').val('');
        $('#edit_outlet_country').val('');
        $('.dropdown').dropdown('clear');

      }
      close_sideform();
    }).fail(function(){
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });

  })


    $('form#form_edit_category_outlet').submit(function(e){
      e.preventDefault();
      let _list = [], outlet = $('.category_check_permission:checked');
      for(i=0; i<outlet.length;i++){
        _list.push($(outlet[i]).val())
      }
      $.post('/v1/api/data/business',{
        data: JSON.stringify({
          id: userData['id'],
          token: userData['token'],
          status: 14,
          outlet_id: $('#edit_category_outlet_id').val(),
          list:_list,
        })
      }, function (e) {
        if(e.status == '00'){
          $('.total_category_outlet_' + $('#edit_category_outlet_id').val()).text(e.data)
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
    })

    $('form#form_edit_item_outlet').submit(function(e){
      e.preventDefault();
      let _list = [], outlet = $('.item_check_permission:checked');
      for(i=0; i<outlet.length;i++){
        _list.push($(outlet[i]).val())
      }
      $.post('/v1/api/data/business',{
        data: JSON.stringify({
          id: userData['id'],
          token: userData['token'],
          status: 16,
          outlet_id: $('#edit_item_outlet_id').val(),
          list:_list,
        })
      }, function (e) {
        if(e.status == '00'){
          $('.total_item_outlet_' + $('#edit_item_outlet_id').val()).text(e.data)
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
    })

}



function _remove_outlet(t){
  $.post('/v1/api/data/business',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 10,
      'outlet_id': t
    })
  }, function (e) {
    $('#remove_outlet_modal_title').text(e.data.name);
    $('#remove_outlet_id').val(e.data.id);

    for(i=0; i<e.data.tax_list.length;i++){
      $('.dropdown').dropdown('set selected', e.data.tax_list[i]);
    }


    open_sideform('remove_outlet_modal');
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function submit_remove_outlet(){
  $('form#form_remove_outlet').submit(function(e){
    e.preventDefault();
    $.post('/v1/api/data/business',{
      data: JSON.stringify({
        'id': userData['id'],
        'token': userData['token'],
        'status': 12,
        'outlet_id': $('#remove_outlet_id').val(),
      })
    }, function (e) {

      if(e.status == '00'){
        $('#edit_outlet_id').val('');
        $('.list_data_' + e.data.id).remove();
      }

      if($('.list_data').length == 0){
        $('.no_data').css('display', 'flex')
      }

      close_sideform();

    }).fail(function(){
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });

  })
}


// ========================================================
// FUNCTION NEW BUSINESS
// ========================================================

function _new_business(){
  _loading(0);
  _submit_new_business();
  _business_category_list('business_category');
}

function _skip(){
  b_id($('#new_business_id').val());
  nav_href_business('business', $('#new_business_id').val());
}

function _submit_new_business(){
  $('form#form_new_business').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/business',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 4,
        business_name: $('#business_name').val(),
        business_category: $('#business_category').val(),
        business_description: $('#business_description').val()
      })
    }, function (e) {
        if(e.status == '00'){
          $('.title').removeClass('active');
          $('#mot').addClass('active');
          $('#new_business').css('display', 'none');
          $('#move_resources').css('display', 'flex');

          $('#list_business').prepend(
            '<a class="mm" href="#" id="nav_business_' + e.data.id + '" onclick="b_id(' + e.data.id + ');nav_href_business(\'business\', ' + e.data.id + ');">' +
            '<p>' + e.data.name + '</p>' +
            '</a>'
          );

          $('#mrt').text(e.data.name);
          $('#new_business_id').val(e.data.id);
          for(i=0; i < e.data_outlet.length; i++){
            $('#move_list_outlet').prepend(
              '<option value="' + e.data_outlet[i].id + '">' + e.data_outlet[i].name + '</option>'
            );
          }
        }else{
          _loading(0);
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  $('form#form_move_outlet').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/business',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 5,
        outlet_list: $('#move_list_outlet').val(),
        business_id: $('#new_business_id').val(),
      })
    }, function (e) {
        if(e.status == '00'){
          b_id(e.business_id);
          nav_href_business('business', e.business_id);
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

}

// ========================================================
// FUNCTION NEW OUTLET
// ========================================================

function _new_outlet(){
  _loading(0);
  _business_list();
  _outlet_num_emp('outlet_num_emp');
  _country_list('outlet_country');
  _general_owner_phone('owner_phone_check', 'outlet_phone_number');
  _submit_new_outlet();
}

function _business_list(){
  $.post('/v1/api/data/business',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 0,
    })
  }, function (e) {
    for(i=0; i < e.data.length; i++){
      $('#select_business').append(
        '<option value="' + e.data[i].id + '">' + e.data[i].name + '</option>'
      )
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function _submit_new_outlet(){
  $('form#form_new_outlet').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/business',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 6,
        business_id: $('#select_business').val(),
        outlet_name: $('#outlet_name').val(),
        outlet_num_emp: $('#outlet_num_emp').val(),
        outlet_phone_number: $('#outlet_phone_number').val(),
        outlet_address: $('#outlet_address').val(),
        outlet_country: $('#outlet_country').val()
      })
    }, function (e) {
      if(e.status == '00'){
        b_id(e.data.business_id.id);
        nav_href_business('business', e.data.business_id.id);
      }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });
}


// ========================================================
// FUNCTION NEW SETTING
// ========================================================

function _business_settings(){
  _business_category_list('settings_business_category');
  _business_settings_detail();
  _form_business_settings();
  _form_business_delete();
}

function _business_settings_detail(){
  $.post('/v1/api/data/business',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 2,
      bid: userData['b_id']
    })
  }, function (e) {
    if(e.status == '00'){
      $('#settings_business_name').val(e.data.name);
      $('#settings_delete_title_business_name').text(e.data.name);
      $('#settings_business_category').val(e.data.business_category_id.id);
      $('#settings_business_description').val(e.data.description);

      if(e.list.length > 0){
        $('#delete_business_button').prop('disabled', true);
      }else{
        $('#delete_business_button').prop('disabled', false).addClass('danger');
      }
    }
    }).fail(function(){
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

function _form_business_settings(){
  $('form#form_business_settngs').submit(function(e){
    e.preventDefault();

    $.post('/v1/api/data/business',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 7,
        business_id: userData['b_id'],
        business_name: $('#settings_business_name').val(),
        business_category: $('#settings_business_category').val(),
        business_description: $('#settings_business_description').val(),
      })
    }, function (e) {
      if(e.status == '00'){
        $('#nav_business_' + e.data.id).html('<p>' + e.data.name + '</p>');
        $('h1#business_name, #title_business_name_delete').text(e.data.name);
        $('#title_business_category').text(e.data.business_category_id.name);
      }else{
        notif('danger', 'Empty Fields', e.message);
      }
    }).fail(function(){
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });

  })
}


function _form_business_delete(){
  $('form#form_delete_business').submit(function(e){
    e.preventDefault();

    $.post('/v1/api/data/business',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 8,
        business_id: userData['b_id'],
      })
    }, function (e) {
      if(e.status == '00'){
        nav_href('dashboard');
        if(e.data == false){
          _loading(1);
          location.reload();
        }
        $('#nav_business_' + userData['b_id']).remove();
      }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });

  })
}
