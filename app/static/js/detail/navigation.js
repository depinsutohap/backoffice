let userData;
$(document).ready(function () {
  userData = localStorage;
  userData['sq'] = '';
  _nav_permission();
  nav_href('dashboard');
  _header_user_data();
  _nav_business_list();
  _menu_dropdown();
  nav_lang('nav');
  _search();
});

function _nav_permission(){
  let _permission = JSON.parse(userData['permission'])
  if(_permission !== null){
    console.log(_permission)
    if(_permission.bo_report.length == 0){
      $('#nav_report').remove()
    }
    if(_permission.bo_management_product.length == 0){
      $('.products').remove()
    }
    if(_permission.bo_management_inventory.length == 0){
      $('#nav_inventory').remove()
    }
    if(_permission.bo_management_product.length == 0 && _permission.bo_management_inventory.length == 0){
      $('.sidenav_product').remove()
    }
    if(_permission.bo_management_tax.length == 0){
      $('#nav_tax').remove()
    }
    if(_permission.bo_management_employee.length == 0){
      $('#nav_employee').remove()
    }
    if(_permission.bo_management_promo.length == 0){
      $('#nav_promo').remove()
    }
    if(_permission.bo_billing.length == 0){
      $('#nav_billing').remove()
    }
    if(_permission.bo_management_employee.length == 0 && _permission.bo_management_promo.length == 0 && _permission.bo_billing.length == 0){
      $('.sidenav_manage').remove()
    }
  }
}

function nav_lang(t){
  if (userData['lang'] !== 1){
    for(i=0; i<language[t].length; i++){
      $('.' + language[t][i][0]).text(language[t][i][1][userData['lang']])
    }
  }
}

function _menu(t){
  if(t == 0){
    $('.sidenav').css('left', '-300px')
  }else{
    $('.sidenav').css('left', 0)
  }
}

function _search(){
  $('#nav_search_bar').on('keyup', function(){
    if(userData['sq'] != $(this).val()){
      $.post('/v1/api/data/search',{
        data: JSON.stringify({
          'id': userData['id'],
          'token': userData['token'],
          'status': 0,
          'q': $(this).val(),
        })
      }, function (e) {
        if(e.status == '00'){
          userData['sq'] = $('#nav_search_bar').val();
          console.log(e)
        }
      }).fail(function(){
        notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
    }
  })
}

function nav_href(t) {
  _loading(1);
  $('#mainBody').load('/page/' + t, function() {});
  $('a.mm').removeClass('actived');
  $('#nav_' + t).addClass('actived');
  if(window.innerWidth < 991){
    console.log('test')
    _menu(0)
  }
}

function nav_href_business(t, i) {
  _loading(1);
  $('#mainBody').load('/page/' + t, function() {

  });

  $('a.mm').removeClass('actived');
  $('#nav_business_' + i).addClass('actived');
  if(window.innerWidth < 991){
    _menu(0)
  }
}

function sub_href(t) {
  _loading(1);
  $('#mainBody').load(t, function() {

  });
}

function logout() {
  _loading(1);
  localStorage.clear();
  window.location.href = '/logout';
}

function alert(cls, msg) {
    let strong;
    if(cls === 'success'){
        strong = 'Success!';
    }else if(cls === 'info'){
        strong = 'Info!';
    }else{
        strong = 'Warning';
    }
    $('#alert').empty().append(
        '<div class="alert alert-' + cls + ' alert-dismissible fade in">' +
        '<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
        '<strong>' + strong + '</strong> ' + msg +
        '</div>'
    );
}


function toggle_nav(i){
  let name = $(i).data('target');

  if($('#caret_' + name).hasClass('fa-caret-up')){
    $('#caret_' + name).removeClass('fa-caret-up').addClass('fa-caret-down');
  }else{
    $('#caret_' + name).addClass('fa-caret-up').removeClass('fa-caret-down');
  }

  $('#list_' + name).collapse('toggle');
}

function toggle_accordion(i){
  let name = $(i).data('target');

  if($('#list_data_' + name).hasClass('active')){
    $('#caret_' + name).removeClass('active');
  }else{
    $('#list_data_' + name).addClass('active');
  }

  $('#accordion_' + name).collapse('toggle');
}


function _nav_business_list(){
  $.post('/v1/api/data/business',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 0,
    })
  }, function (e) {
    if(e.status == '00'){
      if (JSON.parse(userData['permission']) == null){
        $('#list_business').empty().prepend(
          '<a class="nb" href="#" id="nav_outlet" onclick="sub_href(\'/page/business/new\')">' +
          '<i class="fa fa-plus-circle"></i>' +
          '<p>New Business</p></a>'
        );
      }
      _b_list = JSON.parse(userData['permission'])['business_list']
      for(i=0; i < e.data.length; i++){
        if(_b_list.includes(e.data[i].id)){
          $('#list_business').prepend(
            '<a class="mm" href="#" id="nav_business_' + e.data[i].id + '" onclick="b_id(' + e.data[i].id + ');nav_href_business(\'business\', ' + e.data[i].id + ');">' +
            '<p>' + e.data[i].name + '</p>' +
            '</a>'
          )
        }
      }
    }else{
      notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
    }
  }).fail(function(){
    notif('danger', 'System Error!', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

function b_id(n){
  localStorage.b_id = n;
}

function _menu_dropdown(){
  $(".menu").on('click', function(){
    $(this).children('.menu_dropdown').css('display', 'block');
  }).mouseleave(function() {
    $(this).children('.menu_dropdown').css('display', 'none');
  });
}

function open_sideform(t){
  $('#' + t).css('right', '0');
  $('.backdrop').css('display', 'block');
}


function close_sideform(){
  $('.sidemodal').css('right', '-200%');
  $('.backdrop').css('display', 'none');
}

function _check(){
  $('.check_all').on('change', function(){
    if($('.check_all').is(':checked')){
      $('.check_data').prop('checked', true).change();
    }else{
      $('.check_data').prop('checked', false).change();
    }
  })

  $('.check_data').on('change', function(){
    if($('.check_data:checked').length == $('.check_data').length){
      $('.check_all').prop('checked', true);
    }else{
      $('.check_all').prop('checked', false);
    }

    if($('.check_data:checked').length > 0){
      $('._remove_all').attr('disabled', false).css('display', 'block');
    }else{
      $('._remove_all').attr('disabled', true).css('display', 'none');
    }

  });
}


function input_formatNumberwocommas(n) {
  $(n).val($(n).val().toString().replace(/\D/g, ""))
}

function isNumber(evt) {
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true;
}

function _inputwithcommas(x){
  $(x).on({
    keyup: function() {
      formatCurrency($(this));
    },
    blur: function() {
      validateCurrency($(this));
      formatCurrency($(this), "blur");
    }
  });
}

function validateCurrency(input){
    var c = parseFloat(input.val().replace(/\,|$/g,'').replace('$',''));
    if(c<input.attr('min')){
        input.val(input.attr('min'));
    }else if(c>input.attr('max')){
        input.val(input.attr('max'));
    }
}
function formatNumber(n) {
  // format number 1000000 to 1,234,567
  return n.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}


function formatCurrency(input, blur) {
  // appends $ to value, validates decimal side
  // and puts cursor back in right position.

  // get input value
  var input_val = input.val();

  // don't validate empty input
  if (input_val === "") { return; }

  // original length
  var original_len = input_val.length;

  // initial caret position
  var caret_pos = input.prop("selectionStart");


  // check for decimal
  if (input_val.indexOf(".") >= 0) {

    // get position of first decimal
    // this prevents multiple decimals from
    // being entered
    var decimal_pos = input_val.indexOf(".");

    // split number by decimal point
    var left_side = input_val.substring(0, decimal_pos);
    var right_side = input_val.substring(decimal_pos);

    // add commas to left side of number
    left_side = formatNumber(left_side);

    // validate right side
    right_side = formatNumber(right_side);

    // On blur make sure 2 numbers after decimal
    if (blur === "blur") {
      right_side += "00";
   }

    // Limit decimal to only 2 digits
    right_side = right_side.substring(0, 2);

    // join number by .
    input_val = left_side + "." + right_side;

  } else {
    // no decimal entered
    // add commas to number
    // remove all non-digits
    input_val = formatNumber(input_val);
    input_val = input_val;

    // final formatting
    if (blur === "blur") {
      input_val += ".00";
    }
  }

  // send updated string to input
  input.val(input_val);

  // put caret back in the right position
  var updated_len = input_val.length;
  caret_pos = updated_len - original_len + caret_pos;
  input[0].setSelectionRange(caret_pos, caret_pos);
}

function _date(){
  Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
  });
  startdate = new Date().toDateInputValue();
  enddate = new Date().toDateInputValue();
  document.getElementById('startdate').value = startdate
  document.getElementById('enddate').value = enddate
  console.log(startdate)
}
