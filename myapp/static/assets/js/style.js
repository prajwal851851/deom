    $(document).ready(function () {
    // Like button functionality
    $('.like-btn').on('click', function () {
        const postId = $(this).data('post-id');
        const csrfToken = $('[name=csrfmiddlewaretoken]').val() || $('meta[name="csrf-token"]').attr('content');
        const likeBtn = $(this);

         $.ajax({
            url: `/like/${postId}/`,
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            success: function (response) {
                $(`#like-count-${postId}`).text(response.like_count);
                likeBtn.text(response.liked ? 'Unlike' : 'Like');
            },
            error: function (_xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    // Comment form submission
    $('.comment-form').on('submit', function (event) {
        event.preventDefault();
        const postId = $(this).data('post-id');
        const csrfToken = $('[name=csrfmiddlewaretoken]').val() || $('meta[name="csrf-token"]').attr('content');
        const content = $(this).find('input[name="content"]').val();

        if (!content) {
            alert('Comment cannot be empty.');
            return;
        }

        $.ajax({
            url: `/comment/${postId}/`,
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            data: { content: content },
            success: function (response) {
                const commentHtml = `
                    <p>
                        <strong>${response.username}</strong>: ${response.content}
                        <small>${response.created_at}</small>
                    </p>
                `;
                $(`#comments-${postId}`).append(commentHtml);
                $(`#comment-form-${postId}`).find('input[name="content"]').val('');

                // Update comment count (assuming you have a header to update)
                const commentCount = $(`#comments-${postId} p`).length;
                $(`#comments-header-${postId}`).text(`Comments (${commentCount}):`);
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    // Edit and Delete functionality
    $('.edit-btn').on('click', function () {
        const postId = $(this).data('post-id');
        $(`#edit-form-${postId}`).show();
        $(`#post-content-${postId}`).hide();
    });

    $('.cancel-edit-btn').on('click', function () {
        const postId = $(this).data('post-id');
        $(`#edit-form-${postId}`).hide();
        $(`#post-content-${postId}`).show();
    });

    $('.edit-form').on('submit', function (event) {
        event.preventDefault();
        const postId = $(this).data('post-id');
        const csrfToken = $('[name=csrfmiddlewaretoken]').val() || $('meta[name="csrf-token"]').attr('content');
        const content = $(this).find('textarea[name="content"]').val();

        $.ajax({
            url: `/edit/${postId}/`,
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            data: { content: content },
            success: function (response) {
                $(`#post-content-${postId}`).text(response.content).show();
                $(`#edit-form-${postId}`).hide();
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    $('.delete-btn').on('click', function () {
        const postId = $(this).data('post-id');
        const csrfToken = $('[name=csrfmiddlewaretoken]').val() || $('meta[name="csrf-token"]').attr('content');

        if (confirm('Are you sure you want to delete this post?')) {
            $.ajax({
                url: `/delete/${postId}/`,
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
                success: function () {
                    $(`#post-${postId}`).remove();
                },
                error: function (xhr, status, error) {
                    console.error('Error:', error);
                }
            });
        }
    });

    // Follow/Unfollow functionality
    $('#follow-btn').on('click', function () {
        const userId = $(this).data('user-id'); 
        const csrfToken = $('[name=csrfmiddlewaretoken]').val() || $('meta[name="csrf-token"]').attr('content');
        const followBtn = $(this);

        $.ajax({
            url: `/follow/${userId}/`,
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            success: function (response) {
                followBtn.text(response.followed ? 'Unfollow' : 'Follow');
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
    });

