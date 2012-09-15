<script>
  var followers = {{viewed_user.get_profile.followers.count}};

  $('#btn_follow').click(function(){
    var text = $('#btn_follow').html();
    var btn_text = '';
    if (text.indexOf("Unfollow") == -1){
      followers += 1;
      btn_text = '<i class="icon-remove"></i> Unfollow';
    }
    else{
      followers -= 1;
      btn_text = '<i class="icon-user"></i> Follow this user';
    }
    $('#span_followers').html(followers);
    $('#btn_follow').html(btn_text);
  });

</script>
