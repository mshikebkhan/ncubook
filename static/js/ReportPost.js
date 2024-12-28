// Report Post
function ReportPost(post_id) {
  
      // Update Report Post Button
      button = document.getElementById('id_post_report_button_'+post_id);
      button.innerHTML = "Post Reported"
      button.setAttribute("onclick", "");
      
      // Close Menu
      setTimeout(function() {
         CloseThreeDotMenu(post_id);
      }, 900)

      $.ajax({
          // Send data packet including post id to the server.
          headers: {
            "X-CSRFToken": getCookie("csrftoken")
          },
          type: 'POST',
          url: '../../../report_post/' + post_id + '/',

      });

};
