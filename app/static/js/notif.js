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

function notif(type, title, content) {
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
  $('div#notification-box').prepend(
    '<div class="notification-box ' + type + '">' +
    '<div class="left"><i class="fas fa-' + icon + '"></i></div>' +
    '<div class="right ' + type + '">' +
    '<h5>' + title + '</h5>' +
    '<p>' + content + '</p>' +
    '</div>' +
    '<a onclick="close_notif(this)"><i class="glyphicon glyphicon-menu-right notif"></i></a>' +
    '</div>'
  );


  let _notif_box = $('div#notification-box > div');
  console.log(_notif_box.length)
  console.log('haha');
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

function auto_close(t){
  $(t).css('right', '-200%');
  setTimeout(
    function(){
      $(t).remove();
  }, 1000)
}
