// Report Comment
function ReportComment(comment_id) {
  
      // Update Report Comment Button
      button = document.getElementById('id_comment_report_button_'+comment_id);
      button.innerHTML = "[Reported]"
      button.setAttribute("onclick", "");
      
      $.ajax({
          // Send data packet including comment id to the server.
          headers: {
            "X-CSRFToken": getCookie("csrftoken")
          },
          type: 'POST',
          url: '../../../report_comment/' + comment_id + '/',

      });

};
