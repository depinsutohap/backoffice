/**
 * Developed by ION Developer Team
 * URL : https://ION.id
 */

 $('button[data-dismiss="alert"]').on('click', function () {
     $(this).parent().remove()
 });

function _loading(t){
  if(t === 0){
    $('#panel-layer').css('opacity', 0);
      setTimeout(
        function(){
        $('#panel-layer').css('display', 'none')
      }, 1000);
  }else{
    $('#panel-layer').css('display', 'flex')
    setTimeout(
      function(){
      $('#panel-layer').css('opacity', 1);
    }, 100);
  }
}

function notif(type, message) {
  let icon;
  if(type === 'danger'){
    icon = 'times-circle';
  }else if(type === 'notif'){
    icon = 'bell';
  }else if(type === 'success'){
    icon = 'check-circle';
  }else if(type === 'warning'){
    icon = 'exclamation';
  }else if(type === 'info'){
    icon = 'info';
  }

  let _cn = (Math.floor(Math.random() * 10000000)).toString()

  $('div#notification-box').prepend(
    '<div class="notification-box notif-' + _cn + ' ' + type + '">' +
    '<div class="left"><i class="fas fa-' + icon + '"></i></div>' +
    '<p>' + message + '</p>' +
    '<a onclick="close_notif(this)"><i class="glyphicon glyphicon-menu-right notif"></i></a>' +
    '</div>'
  );

  setTimeout(function() {
    auto_close($('.notif-' + _cn));
  }, 2000);

  let _notif_box = $('div#notification-box > div');
  if(_notif_box.length > 1){
    for(i=0; i<_notif_box.length; i++){
      if(i!= 0){
        auto_close($(_notif_box[i]));
      }
    }
  }
}

function close_notif(t){
  $($(t).parent()).css('right', '-200%');
  setTimeout(
    function(){
      $($(t).parent()).remove();
  }, 1000)
}

function close_notif_ad(t){
  $($($(t).parent()).parent()).css('right', '-200%');
  setTimeout(
    function(){
      $($($(t).parent()).parent()).remove();
  }, 1000)
}

function auto_close(t){
  $(t).css('right', '-200%');
  setTimeout(
    function(){
      $(t).remove();
  }, 1000)
}
