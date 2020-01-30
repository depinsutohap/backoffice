function _account(){
  _account_data();
  _submit_data_account();
}

// ========================================================
// account & SERVICES LIST
// ========================================================

// CALL THE users
function _account_data(){
  _loading(1);
  $.post('/v1/api/data/user',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 1,
    })
  }, function (e) {
    console.log(e);
    if(e.status == '00'){
      $('._name').text(e.data.name)
      $('._email').text(e.data.email)
      $('._phone').text(e.data.phone_number)
      $('._reg_date').text(e.data.register_date)
      $('._last_login').text(e.data.log_time)
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

// OPEN AND GET THE account DATA
function _open_account_modal(){
  $.post('/v1/api/data/user',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 1,
    })
  }, function (e) {
    console.log(e)
      if(e.status == '00'){
        $('#edit_account_name').val(e.data.name)
        $('#edit_account_email').val(e.data.email)
        $('#edit_account_phone').val(e.data.phone_number)
        $('#edit_account_id').val(e.data.id);
        open_sideform('edit_account_modal');
      }
    }).fail(function(){
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}



// SUBMIT FORM ALL account (ADD, EDIT, REMOVE)
function _submit_data_account(){

    // SUBMIT EDIT DATA ACCOUNT & SERVICES
    $('form#form_edit_account').submit(function(e){
      e.preventDefault();
      _loading(1);

      $.post('/v1/api/data/user',{
        data: JSON.stringify({
          id: userData['id'],
          token: userData['token'],
          status: 2,
          name: $('#edit_account_name').val(),
          email: $('#edit_account_email').val(),
          phone: $('#edit_account_phone').val(),
        })
      }, function (e) {
        console.log(e)
          if(e.data.status == '00'){
            $('#edit_account_name, #edit_account_email, #edit_account_phone').val('');
            $('._name').text(e.data.name);
            $('._phone').text(e.data.phone_number);
            $('._email').text(e.data.email);
            userData['token'] = e.data.token;
            notif('success', 'Sucessfully Updated', 'Your data has been updated');
            close_sideform();
          }else{
            notif('danger', 'Update Failed', e.message);
          }
        }).fail(function(){
          notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
        }).done(function(){
          _loading(0);
        });
    });

    // SUBMIT CHANGE PASSWORD ACCOUNT
    $('form#form_chg_pass_account').submit(function(e){
      e.preventDefault();
      _loading(1);

      $.post('/v1/api/data/user',{
        data: JSON.stringify({
          id: userData['id'],
          token: userData['token'],
          status: 3,
          cur_pass: $('#_cur_pass').val(),
          new_pass: $('#_new_pass').val(),
          pass_ver: $('#_ver_pass').val(),
        })
      }, function (e) {
        console.log(e)
          if(e.status == '00'){
            $('#_cur_pass, #_new_pass, #_ver_pass').val('');
            userData['token'] = e.data.token;
            notif('success', 'Sucessfully Updated', 'Your password has been updated');
            close_sideform();
          }else{
            notif('danger', 'Update Failed', e.message);
          }
        }).fail(function(){
          notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
        }).done(function(){
          _loading(0);
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
