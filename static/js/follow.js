<script>
  var followers = {{viewed_user.get_profile.followers.count}};

  $('#btn_follow').click(function(){
    var followers_text = " followers";
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

    if (followers <= 1){
      followers_text = followers + " follower";
    }else{
      followers_text = followers + followers_text;
    }

    console.log(followers_text);

    $('#span_followers').text(followers_text);
    $('#btn_follow').html(btn_text);
  });

</script>
