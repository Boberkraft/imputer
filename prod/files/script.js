/**
 * Created by Bobi on 14.06.2017.
 */


// If the number of images is 0 -> Reload the site
// Commented because sometime server dont have time to change state of all
// selected pictures so it stops in the middle of work.
// TODO: Change AJAX to fix this
function change_loaded_images(what) {
    loaded_images = loaded_images + what;
    if (loaded_images <= 0) {
        //				    location.reload(true);
    }
    console.log('Loaded images: ' + loaded_images);
};


// Function for pretty tag :input
var inputs = document.querySelectorAll('.inputfile');
Array.prototype.forEach.call(inputs, function (input) {
    var label = input.nextElementSibling,
        labelVal = label.innerHTML;

    input.addEventListener('change', function (e) {

        var fileName = '';
        if (this.files && this.files.length > 1)
            fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}', this.files.length);
        else
            fileName = e.target.value.split('\\').pop();
        if (fileName) {
            var el = document.getElementById('desc');
            label.parentElement.classList.add('is-primary');
            label.innerHTML = fileName;
        } else
            label.innerHTML = labelVal;
    });
});

/**
 * ********************************************************************************
 *                                       Functions to send AJAX
 * ********************************************************************************
 */

// Universal function to send JSON to server.
function send_data(data, site) {
    $.ajax({
        url: "http://localhost:5000/" + site,
        type: "POST",
        processData: false,
        cache: false,
        data: JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function (result) {
            console.log(result);
        }
    });

};


// Function for sending files when selected
// TODO: Maybe just send a path?
$('#attachments').change(function () {
    var formData = new FormData($("#upload-file")[0]);
    $.ajax({
        url: "http://localhost:5000/upload_files/",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function (result) {
            console.log('new images');
            $('output').append(result);
            $('#edit_menu_online').addClass('hide');
            $('#edit_menu_local').removeClass('hide');
            $('#attachments_button').addClass('hide');
        }
    });
});

/**
 * ********************************************************************************
 *                  Functions to invoked on buttons with global meaning
 * ********************************************************************************
 */


// EDITING HOOK to trigger save button on every CARD
$('#save_all').click(function () {
    $('.save-bt').each(function () {
        var first = $(this).parent().parent().find(".tags-1").val();
        var second = ',';
        var tags = first;
        $(this).parent().parent().html('Added with tags: ' + JSON.stringify(tags) + '<br>Undo');
        var data = {
            'id': $(this).parent().attr('id'),
            'action': 'add',
            'mode': 'selected',
            'tags': tags
        };
        send_data(data, 'change_state/');
        change_loaded_images(-1);
    });

});

// EDITING HOOK to trigger delete button on every CARD
$('#delete_all').click(function () {
    $('.delete-bt').each(function () {
        $(this).parent().parent().addClass('hide');
        var data = {
            'id': $(this).parent().attr('id'),
            'action': 'delete',
            'mode': 'selected'
        };
        send_data(data, 'change_state/');
        change_loaded_images(-1);
    })

});

// EDITING HOOK to add tag to every loaded CARD
$('#tags_all').click(function () {
    var tags = $('#tags_all_input').val();
    $('.tags-1').each(function () {
        var values = $(this).val();
        if (values.length == 0) {
            var sep = '';
        } else {
            var sep = ', ';
        }

        values = tags + sep + values + ' ';
        $(this).val(values);
    });

});

/**
 * ********************************************************************************
 *                        Functions working with a CARD
 * ********************************************************************************
 */

// CARD HOOK. If select button is pressed. It send AJAX selection it or unselecting
$('output').on('click', '.select-bt', function () {
    var selected = $(this).attr("triggered");
    console.log(selected);
    if (selected == 0) {
        var data = {
            'id': $(this).parent().attr('id'),
            'action': 'select',
            'mode': 'selected'
        };
        send_data(data, 'change_state/');
        $(this).parent().parent().parent().addClass('selected');
        $(this).html('Odznacz');
        $(this).attr('triggered', '1');
    } else {
        var data = {
            'id': $(this).parent().attr('id'),
            'action': 'unselect',
            'mode': 'selected'
        };
        send_data(data, 'change_state/')
        $(this).parent().parent().parent().removeClass('selected');
        $(this).html('Zaznacz');
        $(this).attr('triggered', '0');
    }

});

// CARD Hook. If Delete button pressed. It sends AJAX to delete its id from database
$('output').on('click', '.delete-bt', function () {
    $(this).parent().parent().addClass('hide');
    var data = {
        'id': $(this).parent().attr('id'),
        'action': 'delete',
        'mode': 'selected'
    };
    send_data(data, 'change_state/');
    change_loaded_images(-1);
});

// CARD Hook. If Save button pressed It sends AJAX to with tags in its input field.
$('output').on('click', '.save-bt', function () {
    var first = $(this).parent().parent().find(".tags-1").val();
    var tags = first;
    $(this).parent().parent().html('Added with tags: ' + JSON.stringify(tags) + '<br>Undo');
    var data = {
        'id': $(this).parent().attr('id'),
        'action': 'add',
        'mode': 'selected',
        'tags': tags
    };
    send_data(data, 'change_state/');
    change_loaded_images(-1);
});

// CARD Hook for saving if enter is pressed in editing
$('output').on('keypress', '.tags-1', function (e) {
    if (e.which == 13) {
        $(this).parents('.card').find('.save-bt').trigger("click");
    }
});

// CARD Hook for hiding tags and reveling its input field
$('output').on('click', '.edit-bt', function () {
    $(this).parent().parent().parent().find(".hidden_form").removeClass('hide');
    $(this).parent().parent().parent().find(".hidden_tags").addClass('hide');
    $(this).parent().find('.save-bt').removeClass('hide');
    $(this).addClass('hide');
});
