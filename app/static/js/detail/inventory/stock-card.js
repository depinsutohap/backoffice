function _stock_card(){
  _min_max_data(); outlet_list(); _dinamic_data();
}

function _dinamic_data(){
  $('#outlet, .from_date, .to_date').on('change', function(){
    _loading(1);
    $.post('/v1/api/data/stock',{
      data: JSON.stringify({
        id: userData['id'],
        token: userData['token'],
        status: 0,
        from_date: $('.from_date').val(),
        to_date: $('.to_date').val(),
        outlet: $('#outlet').val(),
      })
    }, function (e) {
      console.log(e)
      $('#data_body').empty()
      if(e.data.status == '00'){
        for(i=0;i<e.data.list.length;i++){
          let vid = ''
          if(e.data.list[i].pid.variant_type == true){
            if(e.data.list[i].vid.status == '00'){
              vid = e.data.list[i].vid.variant_item_1.name;
              if(e.data.list[i].vid.variant_item_2 !== null){
                vid += '-' + e.data.list[i].vid.variant_item_2.name;
                if(e.data.list[i].vid.variant_item_3 !== null){
                  vid += '-' + e.data.list[i].vid.variant_item_3.name;
                  if(e.data.list[i].vid.variant_item_4 !== null){
                    vid += '-' + e.data.list[i].vid.variant_item_4.name;
                  }
                }
              }
            }
          }
          let sa_sc = 'ds', sm_sc = 'ds', sk_sc = 'ds', sp_sc = 'ds',
              pi_sc = 'ds', tr_sc = 'ds', ad_sc = 'ds', fs_sc = 'ds';
          if(e.data.list[i].sa < 0){sa_sc = 'rs'}else if(e.data.list[i].sa > 0){sa_sc = 'gs'}
          if(e.data.list[i].sm < 0){sm_sc = 'rs'}else if(e.data.list[i].sm > 0){sm_sc = 'gs'}
          if(e.data.list[i].sk < 0){sk_sc = 'rs'}else if(e.data.list[i].sk > 0){sk_sc = 'gs'}
          if(e.data.list[i].sp < 0){sp_sc = 'rs'}else if(e.data.list[i].sp > 0){sp_sc = 'gs'}
          if(e.data.list[i].pi < 0){pi_sc = 'rs'}else if(e.data.list[i].pi > 0){pi_sc = 'gs'}
          if(e.data.list[i].tr < 0){tr_sc = 'rs'}else if(e.data.list[i].tr > 0){tr_sc = 'gs'}
          if(e.data.list[i].ad < 0){ad_sc = 'rs'}else if(e.data.list[i].ad > 0){ad_sc = 'gs'}
          if(e.data.list[i].fs < 0){fs_sc = 'rs'}else if(e.data.list[i].fs > 0){fs_sc = 'gs'}
          $('#data_body').append(
            '<tr>' +
            '<td>' + e.data.list[i].pid.name + '</td>' +
            '<td>' + vid + '</td>' +
            '<td><span class="' + sa_sc + '">' + formatNumber(e.data.list[i].sa) + '</span></td>' +
            '<td><span class="' + sm_sc + '">' + formatNumber(e.data.list[i].sm) + '</span></td>' +
            '<td><span class="' + sk_sc + '">' + formatNumber(e.data.list[i].sk) + '</span></td>' +
            '<td><span class="' + sp_sc + '">' + formatNumber(e.data.list[i].sp) + '</span></td>' +
            '<td><span class="' + pi_sc + '">' + formatNumber(e.data.list[i].pi) + '</span></td>' +
            '<td><span class="' + tr_sc + '">' + formatNumber(e.data.list[i].tr) + '</span></td>' +
            '<td><span class="' + ad_sc + '">' + formatNumber(e.data.list[i].ad) + '</span></td>' +
            '<td><span class="' + fs_sc + '">' + formatNumber(e.data.list[i].fs) + '</span></td>' +
            '</tr>'
          )
        }
      }
    }).done(function(){
      _loading(0);
    });
  })
}
