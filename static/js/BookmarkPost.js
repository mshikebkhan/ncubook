// Bookmark/Unbookmark Post Button
function BookmarkPost(post_id) {

      // If Not Bookmarked
      if ($('#post_bookmark_button_'+post_id).length > 0)
      {     
            var button =  document.getElementById('post_bookmark_button_'+post_id);
            button.setAttribute("class", "fa fa-bookmark fa-lg");
            button.setAttribute("id", "post_unbookmark_button_"+post_id);

            // Update Total Bookmarked Posts Count      
            if (document.getElementById('total_bookmarked_posts')) {
               var total_bookmarked_posts = document.getElementById('total_bookmarked_posts').innerHTML;
               new_total_bookmarked_posts = parseInt(total_bookmarked_posts) + 1;
               document.getElementById('total_bookmarked_posts').innerHTML = new_total_bookmarked_posts
            }            
      } 

      // If Already Bookmarked
      else if ($('#post_unbookmark_button_'+post_id).length > 0)
      {
            var button =  document.getElementById('post_unbookmark_button_'+post_id);
            button.setAttribute("class", "fa fa-bookmark-o fa-lg");
            button.setAttribute("id", "post_bookmark_button_"+post_id);

            // Update Total Bookmarked Posts Count      
            if (document.getElementById('total_bookmarked_posts')) {
               var total_bookmarked_posts = document.getElementById('total_bookmarked_posts').innerHTML;
               new_total_bookmarked_posts = parseInt(total_bookmarked_posts) - 1;
               document.getElementById('total_bookmarked_posts').innerHTML = new_total_bookmarked_posts
            }
      }

      $.ajax({
          // Send data packet including post id to the server.
          headers: {
            "X-CSRFToken": getCookie("csrftoken")
          },
          type: 'POST',
          url: '../../../community/bookmark_post/' + post_id + '/',

      });

};
