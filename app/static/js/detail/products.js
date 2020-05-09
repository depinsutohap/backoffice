// ========================================================
// FUNCTION FOR PRODUCT CATEGORY
// ========================================================

function _product_category(){
  _loading(0);
  _products_category_list();
  _submit_data_category();
}

// CATEGORY LIST FOR THE TABLE
function _products_category_list(){
  _loading(1);
  $.post('/v1/api/data/products',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 0,
    })
  }, function (e) {
    if(e.data.length > 0){
      $('.no_data').css('display', 'none');
      for(i=0; i<e.data.length; i++){
        $('#data_body').append(
          '<tr id="data_category_' + e.data[i].id + '">'+
          '<td><input class="check_data" value="' + e.data[i].id + '" type="checkbox"></td>'+
          '<td class="data_category_name_' + e.data[i].id + '">' + e.data[i].name + '</td>'+
          '<td class="data_category_list_' + e.data[i].id + '">' + e.data[i].list + '</td>'+
          '<td>' +
          '<div class="menu">'+
          '<i class="fas fa-ellipsis-h"></i>'+
          '<div class="menu_dropdown">'+
          '<a onclick="_open_category_modal(' + e.data[i].id + ')">Edit</a>'+
          '<a class="logout" onclick="_remove_category_modal(' + e.data[i].id + ')">Remove</a>'+
          '</div>'+
          '</div>'+
          '</td>'+
          '</tr>'
        )
      }
      _menu_dropdown();_check();
    }else{
      notif('info', 'Please, create at least a product category before you create your product item');
      $('.no_data').css('display', 'flex');
      $('a.mm').removeClass('actived');
      $('#nav_product-category').addClass('actived');
    }
  }).fail(function(){
    notif('danger', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

// OPEN AND GET THE CATEGORY DATA
function _open_category_modal(cat_id){
  $.post('/v1/api/data/products',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 2,
      category_id: cat_id,
    })
  }, function (e) {
      if(e.status == '00'){
        $('#edit_category_modal_title').text(e.data.name);
        $('#edit_category_name').val(e.data.name);
        $('#edit_category_id').val(e.data.id);
        open_sideform('edit_category_modal');
      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

// OPEN AND GET THE CATEGORY DATA
function _remove_category_modal(cat_id){
  $.post('/v1/api/data/products',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 2,
      category_id: cat_id,
    })
  }, function (e) {
      if(e.status == '00'){
        $('#remove_category_modal_title').text(e.data.name);
        $('#remove_category_id').val(e.data.id);
        open_sideform('remove_category_modal');
      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

// SUBMIT FORM ALL DATA (ADD, EDIT, REMOVE)
function _submit_data_category(){
  // SUBMIT NEW CATEGORY
  $('form#form_add_category').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 1,
        category_name: $('#category_name').val(),
      })
    }, function (e) {
        if(e.status == '00'){
          if(e.data.status == '00'){
            $('#category_name').val('');
            $('.no_data').css('display', 'none');
            $('#data_body').prepend(
              '<tr id="data_category_' + e.data.id + '">'+
              '<td><input class="check_data" value="' + e.data.id + '" type="checkbox"></td>'+
              '<td class="data_category_name_' + e.data.id + '">' + e.data.name + '</td>'+
              '<td class="data_category_list_' + e.data.id + '">' + e.data.list.length + '</td>'+
              '<td>' +
              '<div class="menu">'+
              '<i class="fas fa-ellipsis-h"></i>'+
              '<div class="menu_dropdown">'+
              '<a onclick="_open_category_modal(' + e.data.id + ')">Edit</a>'+
              '<a class="logout" onclick="_remove_category_modal(' + e.data.id + ')">Remove</a>'+
              '</div>'+
              '</div>'+
              '</td>'+
              '</tr>'
            )
            close_sideform();
            _menu_dropdown();_check();
            notif('success', 'Product category has been successfully added');
          }else{
            notif('danger', e.data.message);
          }
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT EDIT DATA CATEGORY
  $('form#form_edit_category').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 3,
        category_name: $('#edit_category_name').val(),
        category_id: $('#edit_category_id').val(),
      })
    }, function (e) {
        if(e.status == '00'){
          $('#edit_category_name').val('');
          $('#edit_category_id').val('')
          $('.data_category_name_' + e.data.id).text(e.data.name);
          $('.data_category_list_' + e.data.id).text(e.data.list.length);
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT REMOVE DATA CATEGORY
  $('form#form_remove_category').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 4,
        category_id: $('#remove_category_id').val(),
      })
    }, function (e) {
        if(e.status == '00'){
          if(e.data.status == '00'){
            $('#remove_category_id').val('');
            $('#data_category_' + e.data.id).remove();
            close_sideform();
            let _list_row = $('#data_body > tr').length;
            if(_list_row == 0){
              $('.no_data').css('display', 'flex');
            }
          }else{
            notif('info', e.data.message);
          }
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT REMOVE MANY DATA CATEGORY
  $('form#form_remove_many_category').submit(function(e){
    e.preventDefault();
    _loading(1);

    let category_list = []
    $('.check_data:checked').each(function() {
        category_list.push($(this).val());
    });

    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 5,
        category_list: category_list,
      })
    }, function (e) {
        if(e.status == '00'){
          for(i=0; i<e.data.length; i++){
            if(e.data[i].status == '00'){
              $('#data_category_' + e.data[i].id).remove();
            }else{

            }
          }
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
        $('.check_all').prop('checked', false).change();
      });
  });
}

// ========================================================
// FUNCTION FOR PRODUCT ITEM
// ========================================================

function iid(id){
  userData['iid'] = id;
}

function _product_item(){
  _products_item_list();
  _submit_data_item();
  _product_filter();
}

function _product_filter(){
  let value = 0;
  $('#product_category').on('change', function(t){
    value = $(this).val();
    $('.cat_row').css('display', 'none')
    if(parseInt(value) !== 0){
      $('.cat_row_' + value ).css('display', 'table-row')
    }else{
      $('.cat_row').css('display', 'table-row')
    }
  })
}

// ITEM LIST FOR THE TABLE
function _products_item_list(){
  _loading(1);
  $.post('/v1/api/data/products',{
    data: JSON.stringify({
      'id': userData['id'],
      'token': userData['token'],
      'status': 8,
    })
  }, function (e) {

    if(e.data_category.length > 0){
      for(i=0; i<e.data_category.length; i++){
        $('#product_category').append(
          '<option value="' + e.data_category[i].id + '">' + e.data_category[i].name + '</option>'
        )
      }
    }

    if(e.data.length > 0){
      $('.no_data').css('display', 'none');
      for(i=0; i<e.data.length; i++){
        let composed_href = '', invent_href = '', price_href = ''
        if(e.data[i].composed_type == true){
          composed_href = '<a onclick="sub_href(\'/page/product-item/manage-ingredients\'); iid(' + e.data[i].id + ')">Manage Ingredients</a>';
        }
        if(e.data[i].composed_type == false){
          invent_href = '<a onclick="sub_href(\'/page/product-item/manage-stock\'); iid(' + e.data[i].id + ')">Manage Stock</a>';
        }
        if(e.data[i].sold_type == true){
          price_href = '<a onclick="sub_href(\'/page/product-item/manage-price\'); iid(' + e.data[i].id + ')">Manage Price</a>';
        }
        $('#data_body').append(
          '<tr id="data_item_' + e.data[i].id + '" class="cat_row cat_row_' + e.data[i].category.id + '" data-category="' + e.data[i].category.id + '">'+
          '<td><input class="check_data" value="' + e.data[i].id + '" type="checkbox"></td>'+
          '<td class="data_item_name_' + e.data[i].id + '">' + e.data[i].name + '</td>'+
          '<td class="data_item_category_' + e.data[i].id + '">' + e.data[i].category.name + '</td>'+
          '<td class="data_item_price_' + e.data[i].id + '">Rp ' + formatNumber(e.data[i].price.value) + '</td>'+
          '<td>' +
          '<div class="menu">'+
          '<i class="fas fa-ellipsis-h"></i>'+
          '<div class="menu_dropdown">'+
          '<a onclick="sub_href(\'/page/product-item/edit\'); iid(' + e.data[i].id + ')">Edit</a>'+
          price_href +
          composed_href +
          invent_href +
          '<a class="logout" onclick="_remove_item_modal(' + e.data[i].id + ')">Remove</a>'+
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
  }).always(function(){
    _loading(0);
  });
}

// ADD ITEM DATA FUNCTIONS
function _products_item_add(){
  _product_category_list('add_product_category');
  _open_button('add_product_variant', 'variant_button', 'flex');
  _open_button_reverse('add_product_composed', 'stock_exp', 'flex');
  _open_div('add_product_composed', 'single_exp', 'composed_exp', 'block')
  _add_row_variant();
  _measurement_item();
  _submit_data_item();
  _loading(0);
}

// EDIT ITEM DATA FUNCTIONS
function _products_item_edit(){
  _product_category_list('edit_product_category');
  _open_item_data();
  _measurement_item();
  _submit_data_item();
}

// OPEN AND GET THE ITEM DATA

function _measurement_item(){

  $('.product_measurement').on('click', function(){
    $('.div_search_measurement').css('display', 'flex')
    $('.measurement_div_search_input_field').focus()
  });
  $('.div_search_measurement').on('mouseleave', function(){
    $(this).css('display', 'none')
    $('.task').css('display', 'inherit');
    $('.waiting, .enter').css('display', 'none');
    $('.measurement_div_search_input_field').blur().val('').keyup();
    $('.measurement_div_search_data > a').remove();

  })
  $('.measurement_div_search_input_field').on('keyup', function(e){
    if($(this).val().length > 0){
      $('.waiting').css('display', 'inherit');
      $('.task, .enter').css('display', 'none');
      $.post('/v1/api/data/search',{
        data: JSON.stringify({
          id: userData['id'],
          token: userData['token'],
          status: 3,
          q: $(this).val().trim(),
          except: $('.product_measurement').attr('data-id')
        })
      }, function(e){
        console.log(e)
        $('.measurement_div_search_data > a').remove()
        if(e.status=='00'){
          for(i=0;i<e.q.length;i++){
            $('.measurement_div_search_data').prepend(
              '<a onclick="measurement_option(' + e.q[i][0] + ', \'' + e.q[i][1] + '\')" data-id="' + e.q[i][0] + '" data-name="' + e.q[i][1] + '">' + e.q[i][1] + '</a>'
            )
          }
        }else{
          $('.enter').css('display', 'inherit');
          $('.waiting, .task').css('display', 'none');
        }
      });
    }else{
      $('.task').css('display', 'inherit');
      $('.waiting, .enter').css('display', 'none');
    }
  }).on('keydown', function(e){
    if (e.keyCode == 13) {
      if($(this).val().trim().length > 0){

        $.post('/v1/api/data/search',{
          data: JSON.stringify({
            id: userData['id'],
            token: userData['token'],
            status: 4,
            q: $(this).val().trim(),
          })
        }, function(e){
          console.log(e)
          if(e.status == '00'){
            $('.product_measurement').val(e['q'][1]).attr('data-id', e['q'][0]);
          }else{
            $('.product_measurement').val($('.measurement_div_search_input_field').val().trim()).attr('data-id', '0');
          }

        }).done(function(){
          $('.div_search_measurement').css('display', 'none')
          $('.task').css('display', 'inherit');
          $('.waiting, .enter').css('display', 'none');
          $('.measurement_div_search_input_field').val('').keyup();
          $('.measurement_div_search_data > a').remove()
        });

      }
      return false;
    }
  });

}

function measurement_option(id, name){
  $('.product_measurement').val(name.trim()).attr('data-id', id);
}

function _open_item_data(){
  let _row = 0, row_mv = 0;
  _open_button('edit_product_variant', 'variant_button', 'flex');
  _open_button_reverse('edit_product_composed', 'stock_exp', 'flex');
  _open_div('edit_product_composed', 'single_exp', 'composed_exp', 'block')
  $.post('/v1/api/data/products',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 10,
      product_id: userData['iid'],
    })
  }, function (e) {
    console.log(e)
      if(e.status == '00'){
        $('#edit_item_header_title').text(e.data.name);
        $('#edit_product_name').val(e.data.name);
        $('#edit_product_category').val(e.data.category.id);
        $('#edit_product_sku').val(e.data.sku);
        $('#edit_product_barcode').val(e.data.barcode);
        if (e.data.measurement !== null){
          $('#edit_product_measurement').val(e.data.measurement.name).attr('data-id', e.data.measurement.id);
        }
        if(e.data.sold_type == true){
          $('#edit_product_sold').prop('checked', true);
        }else{
          $('#edit_product_sold').prop('checked', false);
        }
        if(e.data.composed_type == true){
          $('#edit_product_composed').prop('checked', true).change();
        }else{
          $('#edit_product_composed').prop('checked', false).change();
        }
        if(e.data.variant_type == true){
          $('#edit_product_variant').prop('checked', true).change();
        }else{
          $('#edit_product_variant').prop('checked', false).change();
        }
        $('#edit_product_description').val(e.data.description);



        $('#manage_variant_button').on('click', function(){
          $.post('/v1/api/data/products',{
            data: JSON.stringify({
              id: userData['id'],
              token: userData['token'],
              status: 18,
              product_id: userData['iid'],
            })
          }, function (e) {
            console.log(e)
              if(e.status == '00'){
                $('.variant_input_body').empty();
                if(e.data.length > 0){
                  for(i=0; i<e.data.length; i++){
                    _edit_row_variant(_row, e.data[i]);
                    _row += 1;
                  }
                }else{
                  _append_row_variant(_row);
                }

                if($('.variant_input_body > div').length == 4){
                  $('.add_variant_button').css('display', 'none');
                }

                $('#manage_variant_id').val(userData['iid'])
                open_sideform('manage_variant_modal');
              }
            }).fail(function(){
              notif('danger', 'Mohon kontak IT Administrator');
            }).done(function(){
              _loading(0);
            });
        })

        $('.add_variant_button').on('click', function(){
          _row += 1;
          if($('.variant_input_body > div').length < 4){
            _append_row_variant(_row)
          }

          if($('.variant_input_body > div').length == 4){
            $('.add_variant_button').css('display', 'none');
          }
        })
      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

function _open_button(x, y, z){
  $('#' + x).on('change', function(){
    if($('#' + x).is(':checked')){
      $('.' + y).css('display', z);
    }else{
      $('.' + y).css('display', 'none');
    }
  })
}

function _open_button_reverse(x, y, z){
  $('#' + x).on('change', function(){
    if($('#' + x).is(':checked')){
      $('.' + y).css('display', 'none');
    }else{
      $('.' + y).css('display', z);
    }
  })
}

function _open_div(x, y0, y1, z){
  $('#' + x).on('change', function(){
    if($('#' + x).is(':checked')){
      $('.' + y1).css('display', z);
      $('.' + y0).css('display', 'none');
    }else{
      $('.' + y0).css('display', z);
      $('.' + y1).css('display', 'none');
    }
  })
}

function _add_row_variant(){
  let _row = 0;
  $('.variant_input_body').empty()
  _append_row_variant(_row)

  $('.add_variant_button').on('click', function(){
    _row += 1;
    if($('.variant_input_body > div').length < 4){
      _append_row_variant(_row)
    }

    if($('.variant_input_body > div').length == 4){
      $('.add_variant_button').css('display', 'none');
    }
  })
}

function _edit_row_variant(_row, data){
  let sub_variant;
  _append_row_variant(_row);
  $('.input_category_' + _row).attr('data-id', data['id']).val(data['name'])
  sub_variant = data['sub_variant']
  for(x=0; x<sub_variant.length;x++){
    _append_tag(_row, sub_variant[x].name, sub_variant[x].id)
  }
  $('.input_tag_' + _row).keydown();
}

function _append_row_variant(t){
  $('.variant_input_body').append(
    '<div class="variant_row variant_row_' + t + '">' +
    '<div class="category">' +
    '<input class="input_category input_category_' + t + '" type="text" data-id="0" data-target="' + t + '" placeholder="Example: Size"/>' +
    '</div>' +
    '<div class="item">' +
    '<div class="tag_div">' +
    '<div class="tag_list tag_list_' + t + '"></div>' +
    '<input class="input_tag input_tag_' + t + '" data-target="' + t + '" type="text" placeholder="Example: S, M, L"/>' +
    '</div>' +
    '<a class="delete" onclick="_remove_variant_row(' + t + ')"><i class="fas fa-trash"></i></a>' +
    '</div>' +
    '</div>'
  )

  _create_tag(t)
  readonly_tag_category(t);
}

function _remove_variant_row(t){
  $('.variant_row_' + t).remove();
  if($('.variant_input_body > div').length <= 4){
    $('.add_variant_button').css('display', 'inherit');
  }
}

// OPEN AND GET THE ITEM DATA
function _remove_item_modal(cat_id){
  $.post('/v1/api/data/products',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 10,
      product_id: cat_id,
    })
  }, function (e) {
      if(e.status == '00'){
        $('#remove_item_modal_title').text(e.data.name);
        $('#remove_item_id').val(e.data.id);
        open_sideform('remove_item_modal');
      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

// SUBMIT FORM ALL DATA (ADD, EDIT, REMOVE)
function _submit_data_item(){
  // SUBMIT NEW ITEM
  $('form#form_add_item').submit(function(e){
    e.preventDefault();
    _loading(1);
    let variant=false, sold=false, composed=false, stock=false;
    if($('#add_product_variant').is(':checked')){
      variant = true;
    }
    if($('#add_product_sold').is(':checked')){
      sold = true;
    }
    if($('#add_product_composed').is(':checked')){
      composed = true;
    }
    if($('#add_manage_stock').is(':checked')){
      stock = true;
    }
    let _cat = $('.input_category'), _data = [];
    for(i=0; i<_cat.length; i++){
      if($(_cat[i]).val().length > 0){
        let _detail = {}
        _target = $(_cat[i]).data('target');
        _detail['id'] = $(_cat[i]).data('id');
        _detail['name'] = $(_cat[i]).val();
        _detail['sub_variant'] = []
        _tag = $('.tag_list_' + _target + ' > a')
        if(_tag.length > 0){
          for(x=0; x<_tag.length;x++){
            _detail['sub_variant'].push({
              'id' : $(_tag[x]).data('id'),
              'name' : $(_tag[x]).data('name'),
            })
          }
        }
        _data.push(_detail)
      }
    }

    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 9,
        product_name: $('#add_product_name').val(),
        product_category: $('#add_product_category').val(),
        product_price: $('#add_product_price').val(),
        product_sku: $('#add_product_sku').val(),
        product_barcode: $('#add_product_barcode').val(),
        product_measurement: {
          id:$('#edit_product_measurement').attr('data-id'),
          name:$('#edit_product_measurement').val().trim()
        },
        product_description: $('#add_product_description').val(),
        product_sold: sold,
        product_variant: variant,
        product_composed: composed,
        product_stock: stock,
        data_variant: _data,
      })
    }, function (e) {
      if(e.status == '00'){
        if(e.data.status == '00'){
          nav_href('product-item');
          notif('success','Product item has been added successfully');
        }else{
          notif('danger', e.data.message);
        }
      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
  });

  // SUBMIT EDIT DATA ITEM
  $('form#form_edit_item').submit(function(e){
    e.preventDefault();
    _loading(1);
    let variant=false, sold=false, composed=false;
    if($('#edit_product_variant').is(':checked')){
      variant = true;
    }
    if($('#edit_product_sold').is(':checked')){
      sold = true;
    }
    if($('#edit_product_composed').is(':checked')){
      composed = true;
    }
    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 11,
        product_id: userData['iid'],
        product_name: $('#edit_product_name').val(),
        product_category: $('#edit_product_category').val(),
        product_price: $('#edit_product_price').val(),
        product_sku: $('#edit_product_sku').val(),
        product_barcode: $('#edit_product_barcode').val(),
        product_measurement: {id:$('#edit_product_measurement').attr('data-id'), name:$('#edit_product_measurement').val().trim()},
        product_description: $('#edit_product_description').val(),
        product_sold: sold,
        product_variant: variant,
        product_composed: composed,
      })
    }, function (e) {
        if(e.status == '00'){
          nav_href('product-item');
          notif('success','Product item has been edited successfully');
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  $('form#form_add_manage_variant').on('submit', function(e){
    e.preventDefault()
    _loading(1);
    let _cat = $('.input_category'), _data = [];
    for(i=0; i<_cat.length; i++){
      if($(_cat[i]).val().length > 0){
        let _detail = {}
        _target = $(_cat[i]).data('target');
        _detail['id'] = $(_cat[i]).data('id');
        _detail['name'] = $(_cat[i]).val();
        _detail['sub_variant'] = []
        _tag = $('.tag_list_' + _target + ' > a')
        if(_tag.length > 0){
          for(x=0; x<_tag.length;x++){
            _detail['sub_variant'].push({
              'id' : $(_tag[x]).data('id'),
              'name' : $(_tag[x]).data('name'),
            })
          }
        }else{
          notif('danger','Please, fill all required fields.');
          _loading(0);
          return false
        }
        _data.push(_detail)
      }else{
        notif('danger','Please, fill all required fields.');
        _loading(0);
        return false
      }
    }
    _loading(0);
    close_sideform();
  });

  $('form#form_edit_manage_variant').on('submit', function(e){
    e.preventDefault()
    _loading(1);
    let _cat = $('.input_category'), _data = [];
    for(i=0; i<_cat.length; i++){
      if($(_cat[i]).val().length > 0){
        let _detail = {}
        _target = $(_cat[i]).data('target');
        _detail['id'] = $(_cat[i]).data('id');
        _detail['name'] = $(_cat[i]).val();
        _detail['sub_variant'] = []
        _tag = $('.tag_list_' + _target + ' > a')
        if(_tag.length > 0){
          for(x=0; x<_tag.length;x++){
            _detail['sub_variant'].push({
              'id' : $(_tag[x]).data('id'),
              'name' : $(_tag[x]).data('name'),
            })
          }
        }else{
          notif('danger','Please, fill all required fields.');
          return false
        }
        _data.push(_detail)
      }else{
        notif('danger','Please, fill all required fields.');
        return false
      }
    }
    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 19,
        product_id: $('#manage_variant_id').val(),
        data_list: _data,
      })
    }, function (e) {
        if(e.data.status == '00'){
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT REMOVE DATA ITEM
  $('form#form_remove_item').submit(function(e){
    e.preventDefault();
    _loading(1);
    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 12,
        product_id: $('#remove_item_id').val(),
      })
    }, function (e) {
        if(e.status == '00'){
          $('#remove_item_id').val('');
          $('#data_item_' + e.data.id).remove();
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // SUBMIT REMOVE MANY DATA ITEM
  $('form#form_remove_many_item').submit(function(e){
    e.preventDefault();
    _loading(1);

    let item_list = []
    $('.check_data:checked').each(function() {
        item_list.push($(this).val());
    });

    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 13,
        product_list: item_list,
      })
    }, function (e) {
        if(e.status == '00'){
          for(i=0; i<e.data.length; i++){
            if(e.data[i].status == '00'){
              $('#data_item_' + e.data[i].id).remove();
            }else{

            }
          }
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
        $('.check_all').prop('checked', false).change();
      });
  });


  // Manage Product's Price
  $('form#form_manage_price').submit(function(e){
    e.preventDefault();
    _loading(1);
    let same_price=false;
    if($('#same_price_manage').is(':checked')){
      same_price = true;
    }
    let price = [], input_price = $('.main_price');
    for(i=0; i<input_price.length;i++){

      let pi = '', vi = '', sold_val = false;
      let sold_type = '.main_sold_pi_' + $(input_price[i]).data('pi') + '_vi_' + $(input_price[i]).data('vi')
      if($(sold_type).is(':checked')){
        sold_val = true;
      }
      if($(input_price[i]).data('vi') != null){
        vi = $(input_price[i]).data('vi');
      }
      if($(input_price[i]).data('pi') != null){
        pi = $(input_price[i]).data('pi');
      }
      price.push({
        'pi': pi,
        'vi': vi,
        'sold': sold_val,
        'value': $(input_price[i]).val().toString()
      })
    }
    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 15,
        product_id: userData['iid'],
        same_price: same_price,
        price: price,
      })
    }, function (e) {
        if(e.status == '00'){
          nav_href('product-item');
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // Manage Product Price per outlet
  $('form#form_manage_outlet_price').submit(function(e){
    e.preventDefault();
    _loading(1);
    let price = [], input_price = $('.outlet_price');
    for(i=0; i<input_price.length;i++){
      let pi = '', vi = '';
      if($(input_price[i]).data('vi') != null){
        vi = $(input_price[i]).data('vi');
      }
      if($(input_price[i]).data('pi') != null){
        pi = $(input_price[i]).data('pi');
      }
      price.push({
        'pi': pi,
        'vi': vi,
        'value': $(input_price[i]).val().toString()
      })
    }

    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 17,
        product_id: userData['iid'],
        outlet_id: $('#manage_outlet_price_id').val(),
        price: price,
      })
    }, function (e) {
        if(e.status == '00'){
          $('#manage_outlet_price_id').val('');
          $('#manage_outlet_price_price').val('');
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // Manage Product's Stock
  $('form#form_manage_stock').submit(function(e){
    e.preventDefault();
    // _loading(1);
    let stock = [], input_stock = $('.main_stock');
    for(i=0; i<input_stock.length;i++){

      let pi = '', vi = '', mng_val = false, alert_val=false;
      let mng_type = '.main_mng_pi_' + $(input_stock[i]).data('pi') + '_vi_' + $(input_stock[i]).data('vi'),
          alert_type = '.main_alert_pi_' + $(input_stock[i]).data('pi') + '_vi_' + $(input_stock[i]).data('vi');
      if($(mng_type).is(':checked')){
        mng_val = true;
      }
      if($(alert_type).is(':checked')){
        alert_val = true;
      }

      vi = 0
      if($(input_stock[i]).data('vi') != null){
        vi = $(input_stock[i]).data('vi');
      }
      if($(input_stock[i]).data('pi') != null){
        pi = $(input_stock[i]).data('pi');
      }
      _value = '0'
      if($(input_stock[i]).val().toString().length > 0){
        _value = $(input_stock[i]).val().toString()
      }
      stock.push({
        'pi': pi,
        'vi': vi,
        'invent_type': mng_val,
        'alert_type': alert_val,
        'value': _value
      })
    }
    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 26,
        product_id: userData['iid'],
        stock: stock,
      })
    }, function (e) {
        if(e.status == '00'){
          nav_href('product-item');
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // Manage Ingredients (UPDATE DATA)
  $('form#form_manage_ingredients').submit(function(e){
    e.preventDefault();
    _loading(1);

    let input_field = $('.ingredients_field'), data_list = [];
    let main_data_list = {};
    main_data_list['vid'] = []
    for(i=0; i<input_field.length;i++){
      let
          row = $(input_field[i]).data('row'),
          mpid = $(input_field[i]).data('pid'),
          mvid = $(input_field[i]).data('vid'),
          ipid = $(input_field[i]).data('ipid'),
          ivariant= $(input_field[i]).data('variant'),
          ivid = '0', ival = '0';
          if(ivariant == true){
            ivid = $('.ingredients_variant_pid_' + mpid + '_vid_' + mvid + '_row_' + row).val();
          }
          if($('.ingredients_value_pid_' + mpid + '_vid_' + mvid + '_row_' + row).val().trim().length > 0){
            ival = $('.ingredients_value_pid_' + mpid + '_vid_' + mvid + '_row_' + row).val();
          }

      main_data_list['pid'] = mpid;
      if(main_data_list['vid'].includes(mvid) == false){
        main_data_list['vid'].push(mvid)
      }

      if(ipid != '0'){
        let _detail = {
          'mpid':mpid,
          'mvid':mvid,
          'ipid':ipid,
          'ivariant': ivariant,
          'ivid': ivid,
          'value': ival,
        }
        data_list.push(_detail)
      }
    }

    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 21,
        main_data_list: main_data_list,
        product_list: data_list,
      })
    }, function (e) {
        if(e.status == '00'){
          nav_href('product-item');
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });

  // Import Data from Products
  $('form#form_manage_import_ingredients').submit(function(e){
    e.preventDefault();
    _loading(1);

    let import_item = $('#import_item'), import_mvid=null;
    if($(import_item).attr('data-variant')){
      import_mvid=$('#import_variant').val()
    }
    let mpid = $('#import_pid_vid_id').attr('data-mpid'),
        mvid = $('#import_pid_vid_id').attr('data-mvid');

    $.post('/v1/api/data/products',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 24,
        import_mpid: import_item.val(),
        import_mvid: import_mvid,
      })
    }, function (e) {
        console.log(e)
        if(e.data.status == '00'){
          let exist_list = e.data.ingredients_list;
          $('.ingredients_list_append_pid_' + mpid + '_vid_' + mvid).empty()
          for(x=0; x<exist_list.list.length; x++){
            row = _num_row(mpid, mvid)
            ingredients_list_append_ingredients(mpid, mvid, row);
            ivid = 0
            if( exist_list.list[x].ipid.variant_type == true){
              ivid =  exist_list.list[x].ivid.id;
            }
            choose_ingredients_option(mpid, mvid, row, exist_list.list[x].ipid.id, exist_list.list[x].ipid.name, exist_list.list[x].ipid.variant_type, ivid);
            $('.ingredients_value_pid_' + mpid + '_vid_' + mvid + '_row_' + row).val(exist_list.list[x].amount);
          }
          close_sideform();
        }
      }).fail(function(){
        notif('danger', 'Mohon kontak IT Administrator');
      }).done(function(){
        _loading(0);
      });
  });


}

// MANAGE PRICE FUNCTIONS
function _products_manage_price(){
  _open_item_price();
  _same_price();
  // _product_category_list('edit_product_category');
  _submit_data_item();
}

// OPEN AND GET THE ITEM DATA
function _open_item_price(){
  $.post('/v1/api/data/products',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 14,
      product_id: userData['iid'],
    })
  }, function (e) {
      if(e.status == '00'){
        $('.price_body').empty();

        $('#edit_item_header_title').text(e.data.name);
        $('#same_price_manage').prop('checked', true).change();
        if(e.data.same_price == false){
          $('#same_price_manage').prop('checked', false).change();
        }

        if(e.data.variant_type == false){
          price_list_append('main', e.data.name, e.data.sku, e.data.id, null, e.data.sold)
          price_list_append('outlet', e.data.name, e.data.sku, e.data.id, null, e.data.sold)
        }else{
          for(i=0; i<e.data.variant_list.length;i++){
            let variant_name = '<span class="variant">' + e.data.variant_list[i].variant_item_1.name + '</span>';
            if(e.data.variant_list[i].variant_item_2 !== null){
              variant_name += '<span class="variant">' + e.data.variant_list[i].variant_item_2.name + '</span>';
            }
            if(e.data.variant_list[i].variant_item_3 !== null){
              variant_name += '<span class="variant">' + e.data.variant_list[i].variant_item_3.name + '</span>';
            }
            if(e.data.variant_list[i].variant_item_4 !== null){
              variant_name += '<span class="variant">' + e.data.variant_list[i].variant_item_4.name + '</span>';
            }
            price_list_append('main', variant_name, e.data.variant_list[i].sku, e.data.id, e.data.variant_list[i].id, e.data.variant_list[i].sold)
            price_list_append('outlet', variant_name, e.data.variant_list[i].sku, e.data.id, e.data.variant_list[i].id, e.data.variant_list[i].sold)
          }
        }

        if(e.data.price.status == 00){
          for(i=0; i < e.data.price.price_list.length; i++){
            $('.main_price_pi_' + e.data.price.price_list[i].pid + '_vi_' + e.data.price.price_list[i].vid).val(e.data.price.price_list[i].value);
          }
        }else if(e.data.price.status == 50){
          for(i=0; i < e.data.price.price_list.length; i++){
            $('.main_price').val(e.data.price.price_list[i].value);
          }
        }

        for(i=0;i<e.data.outlet_list.length;i++){
          $('#unsame_type').append(
            '<div class="colum_input">' +
            '<label>' + e.data.outlet_list[i].name + '</label>' +
            '<button onclick="_open_manage_outlet_price(' + e.data.outlet_list[i].id + ')" type="button" class="default">Manage Price</button>' +
            '</div>'
          )
        }
      }

      $('.main_sold').on('change', function(){
      let product_id = $(this).data('pi'), vl_id = $(this).data('vi');
        if($(this).is(':checked')){
          $('.main_price_pi_' + product_id + '_vi_' + vl_id).prop('readonly', false);
          $('.outlet_price_pi_' + product_id + '_vi_' + vl_id).prop('readonly', false);
        }else{
          $('.main_price_pi_' + product_id + '_vi_' + vl_id).prop('readonly', true);
          $('.outlet_price_pi_' + product_id + '_vi_' + vl_id).prop('readonly', true);
        }
      })

      $('.main_sold').change();

    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

function price_list_append(dc, name, sku, product_id, vl_id, sold_type){
  let same_price = '';
  if(dc == 'main'){
    same_price = '<div class="sell">' +
    '<div class="sold_switch">' +
    '<label class="switch">' +
    '<input class="sold ' + dc + '_sold ' + dc + '_sold_pi_' + product_id + '_vi_' + vl_id + '" data-pi="' + product_id + '" data-vi="' + vl_id + '" type="checkbox">' +
    '<span class="slider"></span>' +
    '</label>' +
    '</div>' +
    '</div>'
  }
  $('.' + dc + '_price_body').append(
    '<div class="price_row">' +
    '<div class="name">' + name + '</div>' +
    '<div class="sku">' + sku + '</div>' +
    '<div class="price_column ' + dc + '_price_column">' +
    '<input class="price ' + dc + '_price ' + dc + '_price_pi_' + product_id + '_vi_' + vl_id + '" data-pi="' + product_id + '" data-vi="' + vl_id + '" id="single_price" type="number" placeholder="Rp 0">' +
    '</div>' +
    same_price +
    '</div>'
  )
  if(dc == 'main'){
    $('.' + dc + '_sold_pi_' + product_id + '_vi_' + vl_id).prop('checked', false).change();
    if(sold_type == true){
      $('.' + dc + '_sold_pi_' + product_id + '_vi_' + vl_id).prop('checked', true).change();
    }
  }
}

function _same_price(){
  $('#same_price_manage').on('change', function(){
    if($('#same_price_manage').is(':checked')){
      $('.same_type').css('display', 'block');
      $('.unsame_type').css('display', 'none');
    }else{
      $('.same_type').css('display', 'none');
      $('.unsame_type').css('display', 'block');
    }
  })



}

function _open_manage_outlet_price(oid){
  let same_price=false;
  if($('#same_price_manage').is(':checked')){
    same_price = true;
  }
  $.post('/v1/api/data/products',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 16,
      outlet_id: oid,
      product_id: userData['iid'],
      same_price: same_price,
    })
  }, function (e) {
    console.log(e)
    if(e.status == '00'){
      $('#manage_outlet_price_modal_title').text(e.data.name);
      $('#manage_outlet_price_id').val(oid);
      if(e.data.price.status == 00){
        for(i=0; i < e.data.price.price_list.length; i++){
          $('.outlet_price_pi_' + e.data.price.price_list[i].pid + '_vi_' + e.data.price.price_list[i].vid).val(e.data.price.price_list[i].value);
        }
      }else{
        for(i=0; i < e.data.price.price_list.length; i++){
          $('.outlet_price').val(e.data.price.price_list[i].value);
        }
      }
      open_sideform('manage_outlet_price');
    }
  }).fail(function(){
    notif('danger', 'Mohon kontak IT Administrator');
  }).done(function(){
    _loading(0);
  });
}

// MANAGE Ingredients FUNCTIONS
function _products_manage_ingredients(){
  _open_item_ingredients();
  _loading(0)
  _submit_data_item();
}

// OPEN AND GET THE ITEM DATA
function _open_item_ingredients(){
  $.post('/v1/api/data/products',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 20,
      product_id: userData['iid'],
    })
  }, function (e) {
    console.log(e)
      if(e.status == '00'){
        $('.ingredients_body').empty();
        $('#edit_item_header_title').text(e.data.name);
        if(e.data.variant_type == false){
          ingredients_list_append_item('main', e.data.name, e.data.sku, e.data.id, 'null', e.data.ingredients_list[0])
        }else{
          for(i=0; i<e.data.variant_list.length;i++){
            let variant_name = '<span class="variant">' + e.data.variant_list[i].variant_item_1.name + '</span>';
            if(e.data.variant_list[i].variant_item_2 !== null){
              variant_name += '<span class="variant">' + e.data.variant_list[i].variant_item_2.name + '</span>';
            }
            if(e.data.variant_list[i].variant_item_3 !== null){
              variant_name += '<span class="variant">' + e.data.variant_list[i].variant_item_3.name + '</span>';
            }
            if(e.data.variant_list[i].variant_item_4 !== null){
              variant_name += '<span class="variant">' + e.data.variant_list[i].variant_item_4.name + '</span>';
            }
            ingredients_list_append_item('main', variant_name, e.data.variant_list[i].sku, e.data.id, e.data.variant_list[i].id, e.data.ingredients_list[i])
          }
        }
      }


    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

function ingredients_list_append_item(dc, name, sku, pid, vid, exist_list){
  let row = 0;
  $('.' + dc + '_ingredients_body').prepend(
    '<div class="ingredients_row">' +
    '<div class="name">' + name + '</div>' +
    '<div class="sku"> ' + sku + '</div>' +
    '<div class="ingredients">' +
    '<div class="ingredients_list_append ingredients_list_append_pid_' + pid + '_vid_' + vid + '">' +
    '</div>' +
    '<div class="ingredients_href">' +
    '<a class="ingredients_add_pid_' + pid + '_vid_' + vid + '">' +
    '<i class="fas fa-plus"></i>Add Ingredients</a>' +
    '<a class="import import_pid_' + pid + '_vid_' + vid + '"' +
    'onclick="_ingredients_import(' + pid + ', ' + vid + ')">Import</a>' +
    '</div>' +
    '</div>' +
    '</div>'
  )
  if(exist_list.list.length > 0){
    for(x=0; x<exist_list.list.length; x++){
      console.log(exist_list.list[x])
      row = _num_row(exist_list.mpid, exist_list.mvid)
      console.log(row)
      ingredients_list_append_ingredients(exist_list.mpid, exist_list.mvid, row);
      ivid = null
      if( exist_list.list[x].ipid.variant_type == true){
        ivid =  exist_list.list[x].ivid.id;
      }
      choose_ingredients_option(exist_list.mpid, exist_list.mvid, row, exist_list.list[x].ipid.id, exist_list.list[x].ipid.name, exist_list.list[x].ipid.variant_type, ivid);
      $('.ingredients_value_pid_' + exist_list.mpid + '_vid_' + exist_list.mvid + '_row_' + row).val(exist_list.list[x].amount);
    }
  }else{
    row = _num_row(exist_list.mpid, exist_list.mvid)
    ingredients_list_append_ingredients(exist_list.mpid, exist_list.mvid, row);
  }

  $('.ingredients_add_pid_' + pid + '_vid_' + vid).on('click', function(){
    row = _num_row(exist_list.mpid, exist_list.mvid)
    ingredients_list_append_ingredients(pid, vid, row);
  })
}

function _num_row(pid, vid){
    _row = 0
    let _append = $('.ingredients_list_append_pid_' + pid + '_vid_' + vid + ' > div ');
    if(_append.length > 0){
      _row = $(_append[_append.length-1]).data('row') + 1
    }
    return _row
}

function ingredients_list_append_ingredients(pid, vid, row){
  $('.ingredients_list_append_pid_' + pid + '_vid_' + vid).append(
    '<div class="ingredients_div ingredients_div_pid_' + pid + '_vid_' + vid + ' ingredients_div_pid_' + pid + '_vid_' + vid + '_row_' + row + '" data-row="' + row + '">' +
    '<div class="ingredients_column ingredients_column_pid_' + pid + '_vid_' + vid + '_row_' + row + '">' +
    '<div class="ingredients_div_input ingredients_div_input_pid_' + pid + '_vid_' + vid + '_row_' + row + '">' +
    '<input class="ingredients_field ingredients_field_pid_' + pid + '_vid_' + vid + ' ingredients_field_pid_' + pid + '_vid_' + vid + '_row_' + row + '" type="text" ' +
    'data-row="' + row + '" data-ipid="0" data-pid="' +  pid + '" data-vid="' + vid + '" data-variant="false" readonly placeholder="Choose Ingredients">' +
    '<select class="ingredients_variant ingredients_variant_pid_' + pid + '_vid_' + vid + ' ingredients_variant_pid_' + pid + '_vid_' + vid + '_row_' + row + '"></select>' +
    '</div>' +
    '<div class="ingredients_div_search ingredients_div_search_pid_' + pid + '_vid_' + vid + '_row_' + row + '">' +
    '<div class="ingredients_div_search_input">' +
    '<input class="ingredients_div_search_input_field ingredients_div_search_input_field_pid_' + pid + '_vid_' + vid + '_row_' + row + '" type="text">' +
    '</div>' +
    '<div class="ingredients_div_search_data ingredients_div_search_data_pid_' + pid + '_vid_' + vid + '_row_' + row + '">' +
    '<div class="waiting waiting_pid_' + pid + '_vid_' + vid + '_row_' + row + '">Waiting...</div>' +
    '<div class="task task_pid_' + pid + '_vid_' + vid + '_row_' + row + '">Insert at least 1 character or more..</div>' +
    '</div>' +
    '</div>' +
    '</div>' +
    '<div class="value">' +
    '<input class="ingredients_value ingredients_value_pid_' + pid + '_vid_' + vid + ' ingredients_value_pid_' + pid + '_vid_' + vid + '_row_' + row + '" type="number" step="0.01" placeholder="0">' +
    '</div>' +
    '<div class="measurement"></div>' +
    '<div class="trash trash_pid_' + pid + '_vid_' + vid + '_row_' + row + '">' +
    '<a><i class="fas fa-trash"></i></a>' +
    '</div>' +
    '</div>'
  )

  _ingredients_dropdown(pid, vid, row)

  $('.trash_pid_' + pid + '_vid_' + vid + '_row_' + row).on('click', function(){
    $('.ingredients_div_pid_' + pid + '_vid_' + vid + '_row_' + row).remove()
  })
}

function _ingredients_dropdown(pid, vid, row){
  $('.ingredients_field_pid_' + pid + '_vid_' + vid +'_row_' + row ).on('click', function(){
    $('.ingredients_div_search_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'block');
    $('.ingredients_div_search_input_field_pid_' + pid + '_vid_' + vid +'_row_' + row).focus();
    $('.waiting_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'none');
    $('.task_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'inherit');
  })
  $('.ingredients_column_pid_' + pid + '_vid_' + vid +'_row_' + row ).mouseleave(function() {
    $('.ingredients_div_search_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'none');
    $('.ingredients_div_search_input_field_pid_' + pid + '_vid_' + vid +'_row_' + row).blur().val('');
    $('.ingredients_div_search_data_pid_' + pid + '_vid_' + vid +'_row_' + row + ' > a').remove();
  });

  $('.ingredients_div_search_input_field_pid_' + pid + '_vid_' + vid +'_row_' + row).on('keyup', function(){
    if($(this).val().length > 0){
      $('.ingredients_div_search_data_pid_' + pid + '_vid_' + vid + '_row_' + row + ' > a').remove();
      $('.waiting_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'inherit');
      $('.task_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'none');
      let input_except = $('.ingredients_field_pid_' + pid + '_vid_' + vid);
      let except = []
      for(i=0; i < input_except.length; i++){
        if($(input_except[i]).val().trim().length > 0 && $(input_except[i]).data('ipid') !== '0'){
          except.push($(input_except[i]).data('ipid'));
        }
      }
      $.post('/v1/api/data/search',{
        data: JSON.stringify({
          id: userData['id'],
          token: userData['token'],
          status: 1,
          pid:userData['iid'],
          q: $(this).val().trim(),
          except: except,
        })
      }, function(e){
        $('.ingredients_div_search_data_pid_' + pid + '_vid_' + vid + '_row_' + row + ' > a').remove();
        if(e.status == '00'){
          $('.waiting_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'none');
          if(e.q.length > 0){
            for(i=0; i<e.q.length; i++){
              $('.ingredients_div_search_data_pid_' + pid + '_vid_' + vid + '_row_' + row).append(
                '<a class="ingredients_options" onclick="choose_ingredients_option(\'' + pid + '\', \'' + vid + '\', \'' + row +'\', \'' + e.q[i][0] + '\', \'' + e.q[i][1] + '\', \'' + e.q[i][2] + '\')">' + e.q[i][1] + '</a>'
              )
            }
          }else{
            $('.ingredients_div_search_data_pid_' + pid + '_vid_' + vid + '_row_' + row + ' > a').remove();
            $('.waiting_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'inherit');
          }
        }
      })
    }else{
      $('.ingredients_div_search_data_pid_' + pid + '_vid_' + vid + '_row_' + row + ' > a').remove();
      $('.waiting_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'none');
      $('.task_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'inherit');
    }
  })
}

function choose_ingredients_option(pid, vid, row, id, name, variant, ivid=null){
  $('.ingredients_field_pid_' + pid + '_vid_' + vid + '_row_' + row).attr('data-ipid', id).attr('data-variant', variant).val(name)
  if(variant == true || variant == 'true'){
    $.post('/v1/api/data/search',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 2,
        mpid:pid,
        mvid:vid,
        ipid: id,
      })
    }, function(e){
      $('.ingredients_variant_pid_' + pid + '_vid_' + vid + '_row_' + row).empty();
      if(e.status == '00'){
        if(e.q.length > 0){
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
            $('.ingredients_variant_pid_' + pid + '_vid_' + vid + '_row_' + row).append(
              '<option value="' + e.q[i].id + '">' + _name + '</option>'
            )
          }
        }else{
          $('.ingredients_div_search_data_pid_' + pid + '_vid_' + vid + '_row_' + row + ' > a').remove();
          $('.waiting_pid_' + pid + '_vid_' + vid +'_row_' + row).css('display', 'inherit');
        }
        if(ivid !== null){
          $('.ingredients_variant_pid_' + pid + '_vid_' + vid + '_row_' + row).val(ivid);
        }
      }
    }).done(function(){
        $('.ingredients_variant_pid_' + pid + '_vid_' + vid + '_row_' + row).css('display', 'inherit');
    })

  }else{
    $('.ingredients_variant_pid_' + pid + '_vid_' + vid + '_row_' + row).css('display', 'none');
  }
  $('.ingredients_div_pid_' + pid + '_vid_' + vid +'_row_' + row).mouseleave();
}

function _ingredients_import(mpid, mvid){
  $.post('/v1/api/data/products', {
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 22,
      mpid:mpid,
      mvid:mvid,
    })
  }, function(e){
    console.log(e)
    if(e.data.status == '00'){
      $('#import_item').empty();
      $('#manage_import_modal_title').text(e.data.name)
      $('#import_pid_vid_id').attr('data-mpid', mpid).attr('data-mvid', mvid);
      for(i=0; i<e.data.list.length; i++){
        $('#import_item').append(
          '<option value="' + e.data.list[i].id + '">' + e.data.list[i].name + '</option>'
        )
      }
      $('#import_item').attr('data-mpid', mpid).attr('data-mvid', mvid).change()
      open_sideform('manage_import_ingredients');
    }else{
      notif('info', 'You don\'t have any saved ingredients yet');
    }
  })
}

function _import_item_change(){
  $.post('/v1/api/data/products', {
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 23,
      import_mpid:$('#import_item').val(),
      mpid:$('#import_item').attr('data-mpid'),
      mvid:$('#import_item').attr('data-mvid')
    })
  }, function(e){
    console.log(e)
    $('#import_variant').empty();
    if(e.data.status == '00'){
      $('import_item').attr('data-variant', e.data.variant);
      for(i=0; i<e.data.list.length; i++){
        let _name = e.data.list[i].variant_item_1.name;
        if(e.data.list[i].variant_item_2 !== null){
          _name += '-' + e.data.list[i].variant_item_2.name;
          if(e.data.list[i].variant_item_3 !== null){
            _name += '-' + e.data.list[i].variant_item_3.name;
            if(e.data.list[i].variant_item_4 !== null){
              _name += '-' + e.data.list[i].variant_item_4.name;
            }
          }
        }
        $('#import_variant').append(
          '<option value="' + e.data.list[i].id + '">' + _name + '</option>'
        )
      }
      $('.import_variant_column').css('display', 'flex');
    }else{
      $('.import_variant_column').css('display', 'none');
    }
  })
}



//
function _products_manage_stock(){
  _open_item_stock();
  // _product_category_list('edit_product_category');
  _submit_data_item();
}

// OPEN AND GET THE ITEM DATA
function _open_item_stock(){
  $.post('/v1/api/data/products',{
    data: JSON.stringify({
      id: userData['id'],
      token: userData['token'],
      status: 25,
      product_id: userData['iid'],
    })
  }, function (e) {
    console.log(e)
      if(e.status == '00'){
        $('.stock_body').empty();

        $('#edit_item_header_title').text(e.data.name);

        if(e.data.variant_type == false){
          stock_list_append('main', e.data.name, e.data.sku, e.data.id, null, e.data.invent_type, e.data.invent_alert_type, e.data.invent_min_stock)

        }else{
          for(i=0; i<e.data.variant_list.length;i++){
            let variant_name = '<span class="variant">' + e.data.variant_list[i].variant_item_1.name + '</span>';
            if(e.data.variant_list[i].variant_item_2 !== null){
              variant_name += '<span class="variant">' + e.data.variant_list[i].variant_item_2.name + '</span>';
            }
            if(e.data.variant_list[i].variant_item_3 !== null){
              variant_name += '<span class="variant">' + e.data.variant_list[i].variant_item_3.name + '</span>';
            }
            if(e.data.variant_list[i].variant_item_4 !== null){
              variant_name += '<span class="variant">' + e.data.variant_list[i].variant_item_4.name + '</span>';
            }
            stock_list_append('main', variant_name, e.data.variant_list[i].sku, e.data.id, e.data.variant_list[i].id, e.data.variant_list[i].invent_type, e.data.variant_list[i].invent_alert_type, e.data.variant_list[i].invent_min_stock)
          }
        }

      }

      $('.main_alert').on('change', function(){
      let product_id = $(this).data('pi'), vl_id = $(this).data('vi');
        if($(this).is(':checked')){
          $('.main_stock_pi_' + product_id + '_vi_' + vl_id).prop('readonly', false);
        }else{
          $('.main_stock_pi_' + product_id + '_vi_' + vl_id).prop('readonly', true);
        }
      })

      $('.main_alert').change()

    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
}

function stock_list_append(dc, name, sku, product_id, vl_id, mng_stock, alert_type, min_stock){
  $('.' + dc + '_stock_body').append(
    '<div class="stock_row">' +
    '<div class="name">' + name + '</div>' +
    '<div class="sku">' + sku + '</div>' +
    '<div class="mng_stock">' +
    '<div class="mng_stock_switch">' +
    '<label class="switch">' +
    '<input class="mng ' + dc + '_mng ' + dc + '_mng_pi_' + product_id + '_vi_' + vl_id + '" data-pi="' + product_id + '" data-vi="' + vl_id + '" type="checkbox">' +
    '<span class="slider"></span>' +
    '</label>' +
    '</div>' +
    '</div>' +
    '<div class="alert_stock">' +
    '<div class="alert_switch">' +
    '<label class="switch">' +
    '<input class="alert ' + dc + '_alert ' + dc + '_alert_pi_' + product_id + '_vi_' + vl_id + '" data-pi="' + product_id + '" data-vi="' + vl_id + '" type="checkbox">' +
    '<span class="slider"></span>' +
    '</label>' +
    '</div>' +
    '</div>' +
    '<div class="stock_min ' + dc + '_stock_column">' +
    '<input class="stock ' + dc + '_stock ' + dc + '_stock_pi_' + product_id + '_vi_' + vl_id + '" data-pi="' + product_id + '" data-vi="' + vl_id + '" type="number" placeholder="0">' +
    '</div>' +
    '</div>'
  )

  $('.' + dc + '_mng_pi_' + product_id + '_vi_' + vl_id).prop('checked', false).change();
  if(mng_stock == true){
    $('.' + dc + '_mng_pi_' + product_id + '_vi_' + vl_id).prop('checked', true).change();
  }

  $('.' + dc + '_alert_pi_' + product_id + '_vi_' + vl_id).prop('checked', false).change();
  if(alert_type == true){
    $('.' + dc + '_alert_pi_' + product_id + '_vi_' + vl_id).prop('checked', true).change();
  }

  $('.' + dc + '_stock_pi_' + product_id + '_vi_' + vl_id).val(min_stock)


}
