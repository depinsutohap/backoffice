/**
 * Developed by UTAMA TECH Developer Team
 * URL : https://utama.tech
 */


let userData;

function login() {
  _loading(0); view_pass();
  $('form').submit(function (e) {
      e.preventDefault();
      $.post('/v1/api/auth/login',{
          data: JSON.stringify({
            email: $('#email').val(),
            password: $('#password').val()
          })
      }, function(e){
        if(e.status === '00'){
            notif('success', 'Login successful!', e.message)
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
            notif('danger', 'Authentication failed', e.message)
        }
      }).fail(function () {
        notif('warning', 'Authentication failed', 'Maaf, sistem sedang ada gangguan...')
      });
  })
}


function register() {
  _loading(0); view_pass();
  $('form').submit(function (e) {
      e.preventDefault();
      $.post('/v1/api/auth/register',{
        data: JSON.stringify({
          name: $('#name').val(),
          phone: $('#phone').val(),
          email: $('#email').val(),
          password: $('#password').val()
        })
      }, function(e){
        if(e.status === '00'){
          notif('success', 'Registration successful!', e.message)
          localStorage.setItem('name', e.data.name);
          localStorage.setItem('id', e.data.id);
          localStorage.setItem('phone_number', e.data.phone_number);
          localStorage.setItem('email', e.data.email);
          localStorage.setItem('token', e.data.token);
          location.reload();
        }else{
            notif('danger', 'Authentication failed', e.message)
        }
      }).fail(function () {
          $('#notification-box > span').text('Maaf sistem sedang ada ada gangguan');
      });

      $('#notification-box').delay(200).css('display','inherit').fadeIn('slow');

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
            notif('danger', 'Authentication failed', result.message)
        }
      }).fail(function () {
          $('#notification-box > span').text('Maaf sistem sedang ada ada gangguan');
      });

      $('#notification-box').delay(200).css('display','inherit').fadeIn('slow');
  })
}

function change_password() {
    $('form').submit(function (e) {
        e.preventDefault();
        $.post('/request/auth-change-password',{
          data: JSON.stringify({
            old_password: $('#old_password').val(),
            password: $('#password').val(),
            password2: $('#password2').val()
          })
        }, function(result){
          if(result.status === '00'){
              localStorage.setItem('name', result.name);
              localStorage.setItem('id', result.user_id);
              localStorage.setItem('phone_number', result.phone_number);
              localStorage.setItem('email', result.email);
              localStorage.setItem('token', result.token);
              location.reload();
          }else{
              notif('danger', 'Authentication failed', result.message)
          }
        }).fail(function () {
            $('#notification-box > span').text('Maaf sistem sedang ada ada gangguan');
        });
        $('#notification-box').delay(200).fadeIn('slow').css('display', 'flex');

    })
}

function reset_password() {
    $('form').submit(function (e) {
        e.preventDefault();
        $.post('/request/auth-reset',{
          data: JSON.stringify({
            email: $('#email').val()
          })
        }, function(result){
            if(result.status === 0){
                loader(0)
            }else if(result.status === 1){
                location.replace(window.location.origin);
            }
            $('#notification-box > span').text(result.message)
        }).fail(function () {
            $('#notification-box > span').text('Maaf sistem sedang ada ada gangguan');
        });
        $('#notification-box').delay(200).fadeIn('slow').css('display', 'flex');

    })
}

$(document).ready(function(){
  $('#notif-close').click(function () {
      $(this).parent().delay(200).fadeOut('slow');
      loader(0);
  });
})

function view_pass(){
  $('input#view_pass').on('change', function () {
      if ($(this).is(':checked')) {
          $('input#password').attr('type', 'text');
      }else{
          $('input#password').attr('type', 'password');
      }
  })
}
