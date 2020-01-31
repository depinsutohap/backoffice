function _report(){
  _loading(1);
  nav_lang('report');
  $.post('/v1/api/data/report',{
      data: JSON.stringify({
        'id': userData['id'],
        'token': userData['token'],
        'status': 0,
      })
    }, function (e) {
      let i;
      if(e['status'] === '00'){
        if (userData['id'] > 0){
          $('#totaltrans').text(e.data.total_trans);
          $('#successtrans').text(e.data.success_trans);
          $('#ongoingtrans').text(e.data.ongoing_trans);
          $('#cancelled').text(e.data.cancelled_trans);
          $('#voidtrans').text(e.data.void_trans);
        }else{
          notif('danger', 'user tidak terdaftar')
        }
      }else{
        notif('danger', e.message);
      }
    }).fail(function(){
      notif('danger', 'Mohon kontak IT Administrator');
    }).done(function(){
      _loading(0);
    });
  }
