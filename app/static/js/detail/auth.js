/**
 * Developed by UTAMA TECH Developer Team
 * URL : https://utama.tech
 */


let userData;

function login() {
  _loading(0); view_pass();
  $('form').submit(function (e) {
    e.preventDefault();
    $('button.login').prop('disabled', true);
    notif('info', 'Loading...');
    $.post('/v1/api/auth/login',{
        data: JSON.stringify({
          email: $('#email').val(),
          password: $('#password').val()
        })
    }, function(e){
      if(e.status === '00'){
          notif('success', e.message)
          localStorage.setItem('name', e.name);
          localStorage.setItem('id', e.user_id);
          localStorage.setItem('role_id', e.role_id);
          localStorage.setItem('phone_number', e.phone_number);
          localStorage.setItem('email', e.email);
          localStorage.setItem('lang', e.lang);
          localStorage.setItem('token', e.token);
          localStorage.setItem('permission', JSON.stringify(e.permission));
          location.reload();
      }else{
          notif('danger', e.message);
          $('button.login').prop('disabled', false);
      }
    }).fail(function () {
      notif('warning', 'Maaf, sistem sedang ada gangguan')
      $('button.login').prop('disabled', false)
    });
  })
}


function register() {
  _loading(0); view_pass();
  $('form').submit(function (e) {
      e.preventDefault();
      $('button.login').prop('disabled', true);
      notif('info', 'Loading...');
      let refferal = null;
      if($('#refferal').val().trim().length > 0 ){
        refferal = $('#refferal').val()
      }
      $.post('/v1/api/auth/register',{
        data: JSON.stringify({
          name: $('#name').val(),
          phone: $('#phone').val(),
          email: $('#email').val(),
          password: $('#password').val(),
          refferal: refferal
        })
      }, function(e){
        if(e.status === '00'){
          console.log(e)
          notif('success', e.message)
          localStorage.setItem('name', e.data.name);
          localStorage.setItem('id', e.data.id);
          localStorage.setItem('phone_number', e.data.phone_number);
          localStorage.setItem('email', e.data.email);
          localStorage.setItem('role_id', e.data.role_id);
          localStorage.setItem('token', e.data.token);
          localStorage.setItem('permission', JSON.stringify(e.data.permission));
          location.reload();
        }else{
            notif('danger', e.message)
            $('button.login').prop('disabled', false);
        }
      }).fail(function () {
          notif('warning', 'Maaf, sistem sedang ada gangguan')
          $('button.login').prop('disabled', false);
      });
  })
}

function forgot() {
  _loading(0); view_pass();
  $('form').submit(function (e) {
      e.preventDefault();
      $('button.login').prop('disabled', true)
      notif('info', 'Loading...');
      $.post('/v1/api/auth/forgot',{
        data: JSON.stringify({
          email: $('#email').val(),
        })
      }, function(e){
        if(e.status === '00'){
          notif('success', e.message)
          location.href = window.location.origin;
        }else{
            notif('danger', e.message)
        }
        $('button.login').prop('disabled', false)
      }).fail(function () {
          notif('warning', 'Maaf, sistem sedang ada gangguan')
          $('button.login').prop('disabled', false);
      });
  })
}

function reset() {
  _loading(0); view_pass();
  $('form').submit(function (e) {
      e.preventDefault();
      $('button.login').prop('disabled', true)
      notif('info', 'Loading...');
      $.post('/v1/api/auth/reset-password',{
          data: JSON.stringify({
            token: $('.token').val(),
            password1: $('.password1').val(),
            password2: $('.password2').val()
          })
      }, function(e){
        if(e.status === '00'){
            notif('success', e.message)
            location.href = window.location.origin;
        }else{
            notif('danger', e.message);
            $('button.login').prop('disabled', false);
        }
      }).fail(function () {
        notif('warning', 'Maaf, sistem sedang ada gangguan')
        $('button.login').prop('disabled', false);
      });
  })
}

function detail() {
  userData = localStorage;
  _business_category_list('business_category');
  _outlet_num_emp('outlet_num_emp');
  _country_list('outlet_country');
  _general_owner_phone('owner_phone_check', 'outlet_phone_number');

  _loading(0); view_pass();
  $('form').submit(function (e) {
      e.preventDefault();
      notif('info', 'Loading...');
      $('button.login').prop('disabled', true);
      $.post('/v1/api/auth/detail',{
        data: JSON.stringify({
          id: userData['id'],
          token: userData['token'],
          business_name: $('#business_name').val(),
          outlet_name: $('#outlet_name').val(),
          business_category: $('#business_category').val(),
          outlet_num_emp: $('#outlet_num_emp').val(),
          outlet_phone_number: $('#outlet_phone_number').val(),
          outlet_address: $('#outlet_address').val(),
          outlet_country: $('#outlet_country').val(),
        })
      }, function(result){
        if(result.status === '00'){
            location.reload();
        }else{
            notif('danger', result.message)
            $('button.login').prop('disabled', false);
        }
      }).fail(function () {
          notif('warning', 'Maaf, sistem sedang ada gangguan')
          $('button.login').prop('disabled', false);
      });
  })
}

function view_pass(){
  $('input#view_pass').on('change', function () {
      if ($(this).is(':checked')) {
          $('input#password').attr('type', 'text');
      }else{
          $('input#password').attr('type', 'password');
      }
  })
}
