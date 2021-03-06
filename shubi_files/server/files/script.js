/**
 * Created by Bobi on 14.06.2017.
 * sorry i dont know how to make tests.
 */

/**
 * ********************************************************************************
 *                                 AJAX HOOK
 * ********************************************************************************
 * This hooks are for detecting if there are any uncompleted request that are still peding.
 */


var active_requests = 0;

$(document).ajaxSend(function () {
    active_requests = active_requests + 1;
    console.log(active_requests);
});


$(document).ajaxComplete(function () {
    active_requests = active_requests - 1;
    console.log(active_requests);
});


// If the number of images is 0 -> Reload the site
// Commented because sometime server dont have time to change state of all
// selected pictures so it stops in the middle of work leading to weird thinks.
// TODO: Change AJAX to fix this
var loaded_images = 0;
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
function send_data(data, site, callback) {
    $.ajax({
        url: document.location.origin  + "/" + site,
        type: "POST",
        processData: false,
        cache: false,
        data: JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function (result) {
            if (typeof callback === "undefined") {
                console.log(result);
            }
            else {
                callback(result)
            }
        }
    });

};


// Function for sending files when selected
// TODO: Maybe just send a path?
$('#attachments').change(function () {
    var formData = new FormData($("#upload-file")[0]);
    $.ajax({
        url: document.location.origin + "/upload_files/",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        success: function (result) {
            console.log('new images');
            console.log(result.length / 1400);
            $('output').html(result);
            // $('#edit_menu_online').addClass('hide');
            $('#edit_menu_local').removeClass('hide');
            // $('#attachments_button').addClass('hide');
        }
    });
});

$('.nav-toggle').click(function () {
    var parent = $(this).parent().find('.nav-menu');
    if (parent.hasClass('is-active')){
        console.log('removing');
        parent.removeClass('is-active');
    }
    else {
        console.log('adding');
        parent.addClass('is-active');
    }
});
/**
 * ********************************************************************************
 *                  Functions to that change statis
 * ********************************************************************************
 */

function delete_image(thisObj) {
    $(thisObj).parent().parent().addClass('hide');
    var data = {
        'id': $(thisObj).parent().attr('id'),
        'action': 'delete',
        'mode': 'selected'
    };
    send_data(data, 'change_state/');
    change_loaded_images(-1);
};

function save_image(thisObj) {
    var card = $(thisObj).closest('.card');
    var tags = card.find(".tags-1").val();
    var id = card.attr('image_id');
    console.log(id)
    var data = {
        'id': id,
        'action': 'add',
        'mode': 'selected',
        'tags': tags
    };
    send_data(data, 'change_state/', function (response) {
        card.replaceWith(response);
    });
    change_loaded_images(-1);
};

function select_image(thisObj) {

    var data = {
        'id': $(thisObj).closest('.card').attr('image_id'),
        'action': 'select',
        'mode': 'selected'
    };
    send_data(data, 'change_state/');
    $(thisObj).closest('.card').addClass('selected');
    $(thisObj).html('Odznacz');
    $(thisObj).attr('triggered', '1');
};

function unselect_image(thisObj) {
    var data = {
        'id': $(thisObj).closest('.card').attr('image_id'),
        'action': 'unselect',
        'mode': 'selected'
    };
    send_data(data, 'change_state/')
    $(thisObj).closest('.card').removeClass('selected');
    $(thisObj).html('Zaznacz');
    $(thisObj).attr('triggered', '0');
};
/**
 * ********************************************************************************
 *                  Functions to invoked on buttons with global meaning
 * ********************************************************************************
 */
// delete_all, save_all
function custom_click(thisObj, func) {
    var tries = thisObj.attr('tries');
    tries = parseInt(tries);
    if (tries == 0) {
        thisObj.attr('tries', '1');
        thisObj.removeClass('is-warning');
        thisObj.addClass('is-danger');
    } else {
        thisObj.attr('tries', '0');
        thisObj.removeClass('is-danger');
        thisObj.addClass('is-warning');
        func();
    }
};

// EDITING HOOK to unselect all selected TODO: Just send Query to database and delete output.
$('#unselect_all').click(function () {
    custom_click($(this), function () {
        $('.select-bt').each(function () {
            console.log($(this));
            unselect_image($(this));
        });
    })
});

// EDITING HOOK to trigger save button on every CARD
$('#delete_all').click(function () {
    custom_click($(this), function () {
        $('.delete-bt').each(function () {
            delete_image($(this));
        });
    })
});

// EDITING HOOK to trigger delete button on every CARD
$('#save_all').click(function () {
    custom_click($(this), function () {
        $('.save-bt').each(function () {
            save_image($(this));
        });
    })
});


// EDITING HOOK to add tag to every loaded CARD input field
$('#tags_all').click(function () {
    console.log('untag all');
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

// EDITING HOOK. if enter is pressed on global tags input it triggers click
$('#tags_all_input').keypress(function (e) {
    if (e.which == 13) {
        $('#tags_all').trigger('click')
    }
});


/**
 * ********************************************************************************
 *                        Hooks working with a CARD
 * ********************************************************************************
 */

// CARD HOOK. If select button is pressed. It send AJAX selection it or unselecting
$('output').on('click', '.select-bt', function () {
    var selected = $(this).attr("triggered");
    console.log(selected);
    if (selected == 0) {
        select_image($(this));
    } else {
        unselect_image($(this));
    }

});

// CARD Hook. If Delete button pressed. It sends AJAX to delete its id from database
$('output').on('click', '.delete-bt', function () {
    delete_image($(this))
});

// CARD Hook. If Save button pressed It sends AJAX to with tags in its input field.
$('output').on('click', '.save-bt', function () {
    save_image($(this))
});


// CARD Hook for saving if enter is pressed in editing
$('output').on('keypress', '.tags-1', function (e) {
    if (e.which == 13) {
        $(this).parents('.card').find('.save-bt').trigger("click");
    }
});

// CARD Hook for hiding tags and reveling its input field
$('output').on('click', '.edit-bt', function () {
    $(this).closest('.card').find(".hidden_form").removeClass('hide');
    $(this).closest('.card').find(".hidden_tags").addClass('hide');
    $(this).closest('.card').find('.save-bt').removeClass('hide');
    $(this).addClass('hide');
});
