$( document ).on( "pageinit", "#demo-page", function() {
    $( ".stalls" ).on( "click", function() {
        var target = $( this ),
            brand = target.find( "h2" ).html(),
            model = target.find( "p" ).html(),
            short = target.attr( "id" ),
            closebtn = '<a href="#" data-rel="back" data-role="button" data-theme="a" data-icon="delete" data-iconpos="notext" data-shadow="false" data-iconshadow="false" class="ui-btn-right">Close</a>',
            header = '<div data-role="header"><h2>' + brand + ' ' + model + '</h2></div>',
            img = '<img src="../../_assets/img/' + short + '.jpg" alt="' + brand + '" class="photo">',
            popup = '<div data-role="popup" id="popup-' + short + '" data-short="' + short +'" data-theme="none" data-overlay-theme="a" data-corners="false" data-tolerance="15">' + closebtn + header + img + '</div>';
        // Create the popup. Trigger "pagecreate" instead of "create" because currently the framework doesn't bind the enhancement of toolbars to the "create" event (js/widgets/page.sections.js).
        $.mobile.activePage.append( popup ).trigger( "pagecreate" );
        // Wait with opening the popup until the popup image has been loaded in the DOM.
        // This ensures the popup gets the correct size and position
        $( ".photo", "#popup-" + short ).load(function() {
            var height = $( this ).height(),
                width = $( this ).width();
            // Set height and width attribute of the image
            $( this ).attr({ "height": height, "width": width });
            // Open the popup
            $( "#popup-" + short ).popup( "open" );
            // Clear the fallback
            clearTimeout( fallback );
        });
        // Fallback in case the browser doesn't fire a load event
        var fallback = setTimeout(function() {
            $( "#popup-" + short ).popup( "open" );
        }, 2000);
    });
    // Set a max-height to make large images shrink to fit the screen.
    $( document ).on( "popupbeforeposition", ".ui-popup", function() {
        // 68px: 2 * 15px for top/bottom tolerance, 38px for the header.
        var maxHeight = $( window ).height() - 68 + "px";
        $( "img.photo", this ).css( "max-height", maxHeight );
    });
    // Remove the popup after it has been closed to manage DOM size
    $( document ).on( "popupafterclose", ".ui-popup", function() {
        $( this ).remove();
    });
});

$(document).on("pageinit", function() {
    var nextId = 1;
    $("#add").click(function() {
        nextId++;
        var content = "<div data-role='collapsible' id='set" + nextId + "'><h3>Section " + nextId + "</h3><p>I am the collapsible content in a set so this feels like an accordion. I am hidden by default because I have the 'collapsed' state; you need to expand the header to see me.</p></div>";
        $("#set").append( content ).collapsibleset('refresh');
    });
    $("#expand").click(function() {
        $("#set").children(":last").trigger( "expand" );
    });
    $("#collapse").click(function() {
        $("#set").children(":last").trigger( "collapse" );
    });
});
