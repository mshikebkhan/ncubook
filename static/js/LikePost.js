// Like/Unlike Post Button
function LikePost(post_id) {

      // If Not Liked
      if ($('#post_like_button_'+post_id).length > 0)
      {     
            // Update Unike Post Button
            var button =  document.getElementById('post_like_button_'+post_id);
            button.setAttribute("class", "fa fa-thumbs-up fa-lg");
            button.setAttribute("id", "post_unlike_button_"+post_id);

            // Update Likes Count Of Post
            var likes_count = document.getElementById('post_likes_count_'+post_id).innerHTML;
            new_likes_count = parseInt(likes_count) + 1;
            document.getElementById('post_likes_count_'+post_id).innerHTML = new_likes_count
         
      } 

      // If Already Liked
      else if ($('#post_unlike_button_'+post_id).length > 0)
      {
            // Update Like Post Button
            var button =  document.getElementById('post_unlike_button_'+post_id);
            button.setAttribute("class", "fa fa-thumbs-o-up fa-lg");
            button.setAttribute("id", "post_like_button_"+post_id);

            // Update Likes Count Of Post
            var likes_count = document.getElementById('post_likes_count_'+post_id).innerHTML;
            new_likes_count = parseInt(likes_count) - 1;
            document.getElementById('post_likes_count_'+post_id).innerHTML = new_likes_count

      }

      $.ajax({
          // Send data packet including post id to the server.
          headers: {
            "X-CSRFToken": getCookie("csrftoken")
          },
          type: 'POST',
          url: '../../../like_post/' + post_id + '/',

      });

};

