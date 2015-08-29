var progressBarDiv = $( '.player-loading-box' );
var controls = $( '.player-box > .col-xs-1' );
var progressBar = progressBarDiv.find( '.progress-bar' );

// Seconds to minutes and seconds string
function toMinSec(num) {
    var minutes = Math.floor(num / 60).toString();
    var seconds = Math.floor(num % 60);

    // No more "5:3" when you mean "5:03"
    if (seconds < 10) {
        seconds = '0' + seconds.toString();
    }
    else {
        seconds = seconds.toString();
    }

    return minutes.toString() + ':' + seconds;
}

// Simple waveform player with functionality for controls.
var wavesurfer = Object.create(WaveSurfer);

// Set initial parameters here
wavesurfer.init({
    container: document.querySelector('#wave'),
    height: 300,
    waveColor: 'aqua',
    progressColor: 'blue',
    loaderColor: 'navy',
    fillParent: true
});


// Events go here. Make sure play/pause button is showing the right icons, and that duration updates smoothly

// The loading bar for when a file is being downloaded to a user's computer
wavesurfer.on('loading', function (percent) {
    progressBar.css( 'width', percent + '%' );
});

wavesurfer.on('ready', function () {
    // Hide that progress bar; we don't need it anymore
    progressBarDiv.hide();
    controls.css('visibility', 'visible');

    $( '#position' ).html('0:00/' + toMinSec(wavesurfer.getDuration()));
    wavesurfer.play();
});

wavesurfer.on('play', function () {
    $( '.play-pause' ).switchClass('glyphicon-play', 'glyphicon-pause');
    updateTime();
});

wavesurfer.on('pause', function () {
    $( '.play-pause' ).switchClass('glyphicon-pause', 'glyphicon-play');
    updateTime();
});

wavesurfer.on('finish', function () {
    $( '.play-pause' ).switchClass('glyphicon-pause', 'glyphicon-play');
    updateTime();
});

wavesurfer.on('seek', function () {
    updateTime();
});

wavesurfer.on('scroll', function () {
    updateTime();
});

wavesurfer.on('destroy', function () {
    progressBarDiv.hide()
});

wavesurfer.on('error', function () {
    progressBarDiv.hide()
});

$(document).ready( function ( e ) {
    $( '#pause' ).click(function ( e ) {
        wavesurfer.playPause();
    });
});

function updateTime() {
    $('#position').html(toMinSec(wavesurfer.getCurrentTime()) + '/' + toMinSec(wavesurfer.getDuration()));
    if ( !wavesurfer.backend.isPaused() ) {
        setTimeout(updateTime, 500);
    }
}

// Hide controls by default until track is loaded
controls.css('visibility', 'hidden');

// Specify the actual track to load here
wavesurfer.load('/media/{{ track.file }}');