// FUNCTION FOR GENERAL BUSINESS LIST

function capitalized(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function view_pass(){
  $('input#view_pass').on('change', function () {
    let _target = $(this).attr('data-target');
    console.log(_target)
      if ($(this).is(':checked')) {
          $('input#' + _target).attr('type', 'text');
      }else{
          $('input#' + _target).attr('type', 'password');
      }
  })
}

function _business_category_list(t){
  $.post('/v1/api/data/general',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 0
    })
  }, function(result){
    if(result.status === '00'){
      $('#' + t).empty();
      for(i=0; i < result['data'].length; i++){
        $('#' + t).append(
          '<option value="' + result['data'][i].id + '">' + result['data'][i].name + '</option>'
        )
      }
    }else{
        notif('danger', 'Authentication failed', result.message)
    }
  }).fail(function () {
      $('#notification-box > span').text('Maaf sistem sedang ada ada gangguan');
  });
}

function _outlet_num_emp(t){
  $.post('/v1/api/data/general',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 1
    })
  }, function(result){
    if(result.status === '00'){
      $('#' + t).empty();
      for(i=0; i < result['data'].length; i++){
        $('#' + t).append(
          '<option value="' + result['data'][i].id + '">' + result['data'][i].name + '</option>'
        )
      }
    }else{
        notif('danger', 'Authentication failed', result.message)
    }
  }).fail(function () {
      $('#notification-box > span').text('Maaf sistem sedang ada ada gangguan');
  });
}



// FUNCTION FOR GENERAL LOCATION LIST

function _country_list(t){
  $.post('/v1/api/data/location',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 0
    })
  }, function(result){
    if(result.status === '00'){
      $('#' + t).empty();
      for(i=0; i < result['data'].length; i++){
        $('#' + t).append(
          '<option value="' + result['data'][i].id + '">' + result['data'][i].name + '</option>'
        )
      }
      $('#' + t).val(102);
    }else{
        notif('danger', 'Authentication failed', result.message)
    }
  }).fail(function () {
      $('#notification-box > span').text('Maaf sistem sedang ada ada gangguan');
  });
}

function _general_owner_phone(cbox, t){
  $('input#' + cbox).on('change', function () {
      if ($(this).is(':checked')) {
          $.post('/v1/api/data/user',{
            data: JSON.stringify({
              id: userData['id'],
              token: userData['token'],
              status: 0
            })
          }, function(result){
            if(result.status === '00'){
              $('input#' + t).prop('disabled', true).val(result['data']['phone_number']);
            }else{
                notif('danger', 'Authentication failed', result.message)
            }
          }).fail(function () {
              $('#notification-box > span').text('Maaf sistem sedang ada ada gangguan');
          });

      }else{
          $('input#' + t).prop('disabled', false).val('');
      }
  })
}

function _header_user_data(){
  $('.header_user_name').text(userData['name'])
  $('.header_user_email').text(userData['email'])
}

// FUNCTION FOR GENERAL PRODUCT LIST

function _product_category_list(t){
  $.post('/v1/api/data/products',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 0
    })
  }, function(result){
    if(result.status === '00'){
      $('#' + t).empty();
      for(i=0; i < result['data'].length; i++){
        $('#' + t).append(
          '<option value="' + result['data'][i].id + '">' + result['data'][i].name + '</option>'
        )
      }
    }else{
        notif('danger', 'Authentication failed', result.message)
    }
  }).fail(function () {
      $('#notification-box > span').text('Maaf sistem sedang ada ada gangguan');
  });
}

function _create_tag(target){
  $('.input_tag_' + target).on('keydown', function(e){
    let t = $(this).data('target');
    if(e.keyCode == 9 || e.keyCode == 13 || e.keyCode == 188){
      e.preventDefault();
      if($(this).val().trim().length > 0){
        _append_tag(t, $(this).val())
        $(this).val('')
      }
    }
    if(e.keyCode == 8){
      if($(this).val().trim().length == 0){
        let y = $('.tag_list_' + t + ' > a')
        $(y[y.length - 1]).remove();
      }
    }
  })
  _remove_tag();
}

function _append_tag(x, name, id=0){
  $('.tag_list_' + x).append(
    '<a data-id="' + id + '" data-name="' + name + '" class="tag">' + name + '<i class="fas fa-times"></i></a>'
  )
  _remove_tag();
}

function _remove_tag(){
  $('a.tag').on('click', function(){
    $(this).remove();
  })
}

function readonly_tag_category(t){
  $('.input_tag_' + t + ', .input_category_' + t).on('keydown change', function(){
    let _target = $(this).data('target');
    if($('.tag_list_' + _target + ' > a').length > 0 && $('.input_category_' + _target).val().length){
      $('.input_category_' + _target).prop('readonly', true);
    }else{
      $('.input_category_' + _target).prop('readonly', false);
    }
  })

  $('.input_category').on('keyup keydown', function(e){
    if(e.keyCode == 13) {
      e.preventDefault();
      return false;
    }
  })
}

function outlet_list(){
  _loading(1);
  $.post('/v1/api/data/general',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 2,
    })
  }, function (e) {
    let i;
    if(e['status'] === '00'){
      if(e.data.length > 0){
        for(i=0; i < e.data.length; i++){
          $('.outlet').append(
            '<option value="'+ e.data[i].id +'">'+ e.data[i].name +'</option>'
          )
        }
      }
      $('.outlet').change()
    }else{
      notif('danger', 'System Error!', e.message);
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function outlet_list_b(){
  _loading(1);
  $.post('/v1/api/data/general',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      business: $('#business').val(),
      status: 4
    })
  }, function (e) {
    let i;
    if(e['status'] === '00'){
      if(e.data.length > 0){
        for(i=0; i < e.data.length; i++){
          $('#outlet').append(
            '<option value="'+ e.data[i].id +'">'+ e.data[i].name +'</option>'
          )
        }
      }
    }else{
      notif('danger', 'System Error!', e.message);
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function business_list(){
  _loading(1);
  $.post('/v1/api/data/general',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 3,
    })
  }, function (e) {
    console.log(e)
    let i;
    if(e['status'] === '00'){
      if(e.data.length > 0){
        for(i=0; i < e.data.length; i++){
          $('#business').append(
            '<option value="'+ e.data[i].id +'">'+ e.data[i].name +'</option>'
          )
        }
      }
    }else{
      notif('danger', 'System Error!', e.message);
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function _create_date(n){
  var today = new Date();
  var dd = String(today.getDate()+n).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = today.getFullYear();

  today = yyyy + '-' + mm + '-' + dd;
  return today
}

function _min_max_data(){
  $('.from_date').on('change', function(){
    $('.to_date').attr('min', $(this).val());
  })
  $('.to_date').on('change', function(){
    $('.from_date').attr('max', $(this).val());
  })
  $('.from_date, .to_date').val(_create_date(0)).change();
}
