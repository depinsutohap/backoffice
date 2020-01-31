function _employee(){
  _employee_list();
  _submit_data_employee();
}

// ========================================================
// EMPLOYEE LIST MAIN PAGES
// ========================================================

// EMPLOYEE LIST
function _employee_list(){
  _loading(1); let _outlet_list;
  $.post('/v1/api/data/employee',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 0,
    })
  }, function (e) {
    if(e.data.length > 0){
      $('.no_data').remove()
      for(i=0; i<e.data.length; i++){

        _outlet_list = '-';
        if(e.data[i].outlet_list.length > 0){
          _outlet_list = [];
          for(m=0; m<e.data[i].outlet_list.length; m++){
            _outlet_list.push(e.data[i].outlet_list[m].name)
          }
        }

        $('#data_body').append(
          '<tr id="data_employee_' + e.data[i].id + '">'+
          '<td class="data_employee_name_' + e.data[i].id + '">' + e.data[i].name + '</td>'+
          '<td class="data_employee_type_' + e.data[i].id + '">' + e.data[i].role.name + '</td>'+
          '<td class="data_employee_value_' + e.data[i].id + '">' + _outlet_list.toString() + '</td>'+
          '<td>' +
          '<div class="menu">'+
          '<i class="fas fa-ellipsis-h"></i>'+
          '<div class="menu_dropdown">'+
          '<a onclick="_edit_employee_permission(\'edit\', ' + e.data[i].id + ')">Edit</a>'+
          '<a onclick="_edit_employee_permission(\'manage-access\', ' + e.data[i].id + ')">Manage Access</a>'+
          '<a class="logout" onclick="_remove_employee_modal(' + e.data[i].id + ')">Remove</a>'+
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
    notif('danger', 'Mohon kontak IT Administrator');
  }).done(function(){

  }).always(function(){
    _loading(0);
  });
}

// ========================================================
// FUNCTION FOR EDIT EMPLOYEE PERMISSION
// ========================================================

// OPEN AND GET THE EMPLOYEE DATA
function _edit_employee_permission(_page, _id){
  userData['eid'] = _id
  $('#mainBody').load('/page/employee/' + _page, function() {
    _loading(0);
  });;
}

function _edit_manage_access(){
  _submit_data_employee();
  $('#add_employee_id').val(userData['eid'])
  console.log(userData['eid'])
  $.post('/v1/api/data/employee',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 5,
      employee_id: userData['eid'],
    })
  }, function (e) {
      if(e.status == '00'){

        $('#_edit_employee_name').text(e.data.name)

        if(e.outlet_list.length > 0){
          $('.no_data').remove()
          for(i=0; i<e.outlet_list.length; i++){
            $('#data_body').append(
              '<tr id="data_employee_' + e.outlet_list[i].id + '">'+
              '<td><input class="check_data" id="_check_outlet_' + e.outlet_list[i].id + '" onchange=_check_outlet("' + e.outlet_list[i].id + '") value="' + e.outlet_list[i].id + '" type="checkbox"></td>'+
              '<td class="data_employee_name_' + e.outlet_list[i].id + '">' + e.outlet_list[i].name + '</td>'+
              '<td class="data_employee_type_' + e.outlet_list[i].id + '">' + e.outlet_list[i].business_id.name + '</td>'+
              '<td>' +
              '<button onclick="_open_modal_permission(\'' + e.outlet_list[i].name + '\',\'' + e.outlet_list[i].id + '\')" type="button" class="default _permission_button _permission_button_' + e.outlet_list[i].id + '" onclick="#">Permission</button>' +
              '</td>'+
              '</tr>'
            )
          }
          _menu_dropdown(); _check();
        }else{
          $('.no_data').css('display', 'flex');
        }

        if(e.data_outlet.length > 0){
          for(i=0; i<e.data_outlet.length; i++){
            $('#_check_outlet_' + e.data_outlet[i]).prop('checked', true).change()
          }
        }

        if(e.data.role.id==3){
          $('.bo_permission').css('display', 'none')
        }else{
          $('.bo_permission').css('display', 'block')
        }


      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

// ========================================================
// FUNCTION FOR EDIT EMPLOYEE DATA
// ========================================================


function _edit_employee_data(){
  _submit_data_employee();
  $('#edit_employee_id').val(userData['eid'])

  $.post('/v1/api/data/employee',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 6,
      employee_id: userData['eid'],
    })
  }, function (e) {
      if(e.status == '00'){

        $('#_edit_employee_name_title').text(e.data.name)
        $('#edit_employee_name').val(e.data.name)
        $('#edit_employee_phone').val(e.data.phone_number)
        $('#edit_employee_email').val(e.data.email)

        if(e.data.role.id == 3){
          $('#edit_employee_3').prop('checked', true);
        }else{
          $('#edit_employee_2').prop('checked', true);
        }


      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

// ========================================================
// REMOVE EMPLOYEE DATA
// ========================================================


// OPEN AND GET THE EMPLOYEE DATA TO REMOVE MODAL
function _remove_employee_modal(_id){
  $.post('/v1/api/data/employee',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 6,
      employee_id: _id,
    })
  }, function (e) {
      if(e.status == '00'){
        $('#remove_employee_modal_title').text(e.data.name);
        $('#remove_employee_id').val(e.data.id);
        open_sideform('remove_employee_modal');
      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

// ========================================================
// FUNCTION FOR SUBMIT EMPLOYEE DATA
// ========================================================

// SUBMIT FORM ALL EMPLOYEE (ADD, EDIT, REMOVE)
function _submit_data_employee(){
  // SUBMIT NEW EMPLOYEE
  view_pass();
  $('form#form_add_employee').submit(function(e){
    e.preventDefault();
    _loading(1);

    if($('input[name=add_employee_role]:checked').val() == null ||
      $('#add_employee_name').val().length == 0 ||
      $('#add_employee_phone').val().length == 0 ||
      $('#add_employee_password').val().length == 0
    ){
      _loading(0)
      notif('danger','Please fill required fields.');
      return false
    }

    if($('#add_employee_password').val().length < 8){
      _loading(0)
      notif('danger','Password must be at least 8 characters in length.');
      return false
    }



    $.post('/v1/api/data/employee',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 1,
        employee_name: $('#add_employee_name').val(),
        employee_role_id: $('input[name=add_employee_role]:checked').val(),
        employee_phone: $('#add_employee_phone').val(),
        employee_email: $('#add_employee_email').val(),
        employee_password: $('#add_employee_password').val(),
      })
    }, function (e) {
      console.log(e)
        if(e.status == '00'){

          $('#add_employee_id').val(e.data.id);

          if(e.outlet_list.length > 0){
            $('.no_data').remove()
            for(i=0; i<e.outlet_list.length; i++){
              $('#data_body').append(
                '<tr id="data_employee_' + e.outlet_list[i].id + '">'+
                '<td><input class="check_data" id="_check_outlet_' + e.outlet_list[i].id + '" onchange=_check_outlet("' + e.outlet_list[i].id + '") value="' + e.outlet_list[i].id + '" type="checkbox"></td>'+
                '<td class="data_employee_name_' + e.outlet_list[i].id + '">' + e.outlet_list[i].name + '</td>'+
                '<td class="data_employee_type_' + e.outlet_list[i].id + '">' + e.outlet_list[i].business_id.name + '</td>'+
                '<td>' +
                '<button onclick="_open_modal_permission(\'' + e.outlet_list[i].name + '\',\'' + e.outlet_list[i].id + '\')" type="button" class="default _permission_button _permission_button_' + e.outlet_list[i].id + '" onclick="#">Permission</button>' +
                '</td>'+
                '</tr>'
              )
            }
            _menu_dropdown(); _check();
          }else{
            $('.no_data').css('display', 'flex');
          }

          $('.title').removeClass('active');
          $('#mat').addClass('active');
          if($('input[name=add_employee_role]:checked').val()==3){
            $('.bo_permission').css('display', 'none')
          }else{
            $('.bo_permission').css('display', 'block')
          }
          $('._create_account').css('display', 'none')
          $('._outlet_list').css('display', 'block')


        }else{
          notif('danger', e.message);
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // CONTINUE FROM SUBMIT NEW EMPLOYEE TO USER'S OUTLET
  $('form#form_add_employee_outlet').submit(function(e){
    e.preventDefault();
    _loading(1);
    let outlet_list = [];
    _check_data = $('.check_data:checked');
    for(i=0; i<_check_data.length;i++){
    	outlet_list.push($(_check_data[i]).val())
    }
    $.post('/v1/api/data/employee',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 2,
        employee_outlet_list: outlet_list,
        employee_id: $('#add_employee_id').val(),
      })
    }, function (e) {
        if(e.status == '00'){
          nav_href('employee');
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // CONTINUE FROM SUBMIT NEW EMPLOYEE TO USER'S OUTLET PERMISSION
  $('form#form_add_permission').submit(function(e){
    e.preventDefault();
    _loading(1);

    let employee_list = []
    $('.check_data:checked').each(function() {
        employee_list.push($(this).val());
    });

    $.post('/v1/api/data/employee',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 3,
        employee_id: $('#add_employee_id').val(),
        outlet_id: $('#manage_outlet_permission_id').val(),
        employee_mobile_order: $("#add_employee_mobile_order").is(':checked'),
        employee_mobile_payment: $("#add_employee_mobile_payment").is(':checked'),
        employee_mobile_void: $("#add_employee_mobile_void").is(':checked'),
        employee_mobile_change_trx: $("#add_employee_mobile_change_trx").is(':checked'),
        employee_mobile_custom_price: $("#add_employee_mobile_custom_price").is(':checked'),
        employee_mobile_custom_discount: $("#add_employee_mobile_custom_discount").is(':checked'),
        employee_mobile_reprint_reciept: $("#add_employee_mobile_reprint_reciept").is(':checked'),
        employee_mobile_reprint_kitchen: $("#add_employee_mobile_reprint_kitchen").is(':checked'),
        employee_mobile_print_invoice: $("#add_employee_mobile_print_invoice").is(':checked'),
        employee_mobile_history: $("#add_employee_mobile_history").is(':checked'),
        employee_mobile_customer: $("#add_employee_mobile_customer").is(':checked'),
        employee_bo_outlet: $("#add_employee_bo_outlet").is(':checked'),
        employee_bo_report: $("#add_employee_bo_report").is(':checked'),
        employee_bo_product: $("#add_employee_bo_product").is(':checked'),
        employee_bo_inventory: $("#add_employee_bo_inventory").is(':checked'),
        employee_bo_tax: $("#add_employee_bo_tax").is(':checked'),
        employee_bo_employee: $("#add_employee_bo_employee").is(':checked'),
        employee_bo_promo: $("#add_employee_bo_promo").is(':checked'),
        employee_bo_customer: $("#add_employee_bo_customer").is(':checked'),
        employee_bo_billing: $("#add_employee_bo_billing").is(':checked'),
        employee_bo_email: $("#add_employee_bo_email").is(':checked')
      })
    }, function (e) {
        if(e.status == '00'){
          $('.check_permission').prop('checked', false);
          $('#manage_outlet_permission_title').text('############')
          $('#manage_outlet_permission_id').val('')
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // EDIT DATA EMPLOYEE & SERVICES
  $('form#form_edit_employee').submit(function(e){
    e.preventDefault();
    _loading(1);

    _password = $('#edit_employee_password').val();

    if($('input[name=edit_employee_role]:checked').val() == null ||
      $('#edit_employee_name').val().length == 0 ||
      $('#edit_employee_phone').val().length == 0 ||
      (_password.length > 0 && _password.length < 8)
    ){
      _loading(0)

      if(_password.length > 0 && _password.length < 8){
        notif('danger','Minimum password length 8 characters');
        return false
      }

      notif('danger','Please fill required fields.');
      return false
    }


    if($('#edit_employee_password').val().length == 0){
      _password = null;
    }

    $.post('/v1/api/data/employee',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 7,
        employee_id: $('#edit_employee_id').val(),
        employee_name: $('#edit_employee_name').val(),
        employee_role_id: $('input[name=edit_employee_role]:checked').val(),
        employee_phone: $('#edit_employee_phone').val(),
        employee_email: $('#edit_employee_email').val(),
        employee_password: _password,
      })
    }, function (e) {
        if(e.status == '00'){
          nav_href('employee');
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT REMOVE DATA EMPLOYEE & SERVICES
  $('form#form_remove_employee').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/employee',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 8,
        employee_id: $('#remove_employee_id').val(),
      })
    }, function (e) {
        if(e.status == '00'){
          $('#data_employee_' + $('#remove_employee_id').val()).remove();
          $('#remove_employee_modal_title').val('#########');
          $('#remove_employee_id').val('');

          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });
}

// ========================================================
// GENERAL FUNCTION FOR EMPLOYEE PERMISSION
// ========================================================


// OPEN MODAL PERMISSION AND GET THE DATA
function _open_modal_permission(t, id){
  $('.check_permission').prop('checked', false).change();

  $.post('/v1/api/data/employee',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 4,
      employee_id: $('#add_employee_id').val(),
      outlet_id: id,
    })
  }, function (e) {
      if(e.status == '00'){
        if(e.data.mob_order == true){$("#add_employee_mobile_order").prop('checked', true)}
        if(e.data.mob_payment == true){$("#add_employee_mobile_payment").prop('checked', true)}
        if(e.data.mob_void == true){$("#add_employee_mobile_void").prop('checked', true)}
        if(e.data.mob_change_transaction == true){$("#add_employee_mobile_change_trx").prop('checked', true)}
        if(e.data.mob_custom_price == true){$("#add_employee_mobile_custom_price").prop('checked', true)}
        if(e.data.mob_custom_discount == true){$("#add_employee_mobile_custom_discount").prop('checked', true)}
        if(e.data.mob_reprint_reciept == true){$("#add_employee_mobile_reprint_reciept").prop('checked', true)}
        if(e.data.mob_reprint_kitchen_reciept == true){$("#add_employee_mobile_reprint_kitchen").prop('checked', true)}
        if(e.data.mob_print_invoice_reciept == true){$("#add_employee_mobile_print_invoice").prop('checked', true)}
        if(e.data.mob_history_transaction == true){$("#add_employee_mobile_history").prop('checked', true)}
        if(e.data.mob_customer_management == true){$("#add_employee_mobile_customer").prop('checked', true)}
        if(e.data.bo_outlet_management == true){$("#add_employee_bo_outlet").prop('checked', true)}
        if(e.data.bo_report == true){$("#add_employee_bo_report").prop('checked', true)}
        if(e.data.bo_management_product == true){$("#add_employee_bo_product").prop('checked', true)}
        if(e.data.bo_management_inventory == true){$("#add_employee_bo_inventory").prop('checked', true)}
        if(e.data.bo_management_tax == true){$("#add_employee_bo_tax").prop('checked', true)}
        if(e.data.bo_management_employee == true){$("#add_employee_bo_employee").prop('checked', true)}
        if(e.data.bo_management_promo == true){$("#add_employee_bo_promo").prop('checked', true)}
        if(e.data.bo_customer_management == true){$("#add_employee_bo_customer").prop('checked', true)}
        if(e.data.bo_billing == true){$("#add_employee_bo_billing").prop('checked', true)}
        if(e.data.bo_daily_report == true){$("#add_employee_bo_email").prop('checked', true)}
      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });

  $('#manage_outlet_permission_title').text(t)
  $('#manage_outlet_permission_id').val(id)
  open_sideform('_add_permission');
}

function _check_outlet(t){
  if($('#_check_outlet_' + t).is(':checked')){
    $('._permission_button_' + t).css('display', 'inherit');
  }else{
    $('._permission_button_' + t).css('display', 'none');
  }
}
