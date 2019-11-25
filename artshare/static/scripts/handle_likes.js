const baseUrl = document.location.origin;

// When user clicks on like button, send POST to backend, then on success show changes to user
$(".like").each(function() {
  $(this).on("click", function() {
    let postId = $(this).attr("id");
    let postUrl = `${baseUrl}/like/${postId}`;
    let likesAmount = $(`#likes-count-${postId}`);

    $.ajax({
      type: "POST",
      url: postUrl,
      success: function(resultData) {
        if (resultData.is_authenticated) {
          if (resultData.liked) {
            $(`#${postId}`).html(
              '<i class="fas fa-heart-broken"></i>  Dislike'
            );
            likesAmount.text(parseInt(likesAmount.text()) + 1);
          } else {
            $(`#${postId}`).html('<i class="fas fa-heart"></i>  Like');
            likesAmount.text(parseInt(likesAmount.text()) - 1);
          }
        } else {
          alert("Please log in to like posts...");
        }
      },
      error: function() {
        console.log("Something went wrong...");
      }
    });
  });
});

$(".profile-view-like").each(function() {
  $(this).on("click", function() {
    let postId = $(this).attr("id");
    let postUrl = `${baseUrl}/like/${postId}`;

    $.ajax({
      type: "POST",
      url: postUrl,
      success: function(resultData) {
        if (resultData.is_authenticated) {
          // Dislike post and remove it from view
          $(`#img-card-${postId}`).remove();
        } else {
          alert("Please log in to like posts...");
        }
      },
      error: function() {
        console.log("Something went wrong...");
      }
    });
  });
});
