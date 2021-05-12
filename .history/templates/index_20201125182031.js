{% extends "layout.html" %}

{% block title %}
    Buy
{% endblock %}

{% block main %}

<div class="split left">
        <object type="text/html" data="https://www.medscape.com/medicalstudents" width="100%" height="100%">
        </object>
  </div>
  
  <div class="split right">
    <div class="centered">
    <div id="player"></div>
  <div>
        <div class="form-group">
          <label for="userInput">You-Tube Link</label>
          <input type="text" class="form-control" id="userInput" placeholder="url">
          <button type="button" onclick="getInputValue();" class="btn btn-primary">Search video</button>
        </div>
  </div>
    </div>

      <script>
      function getInputValue(){
          var inputVal = document.getElementById("userInput").value;    
            // get video id from url
            function getId(url) {
              const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
              const match = url.match(regExp);

              return (match && match[2].length === 11)
                ? match[2]
                : null;
            }
      } 
             
              // 2. This code loads the IFrame Player API code asynchronously.
              var tag = document.createElement('script');

              tag.src = "https://www.youtube.com/iframe_api";
              var firstScriptTag = document.getElementsByTagName('script')[0];
              firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

              // 3. This function creates an <iframe> (and YouTube player)
              //    after the API code downloads.
              var player;
              function onYouTubeIframeAPIReady() {
                const videoIdd = getId(inputVal);
                player = new YT.Player('player', {
                  height: '390',
                  width: '640',
                  videoId: videoIdd,
                  events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                  }
                });
              }

              // 4. The API will call this function when the video player is ready.
              function onPlayerReady(event) {
                event.target.playVideo();
              }

              // 5. The API calls this function when the player's state changes.
              //    The function indicates that when playing a video (state=1),
              //    the player should play for six seconds and then stop.
              var done = false;
              function onPlayerStateChange(event) {
                if (event.data == YT.PlayerState.PLAYING && !done) {
                  setTimeout(stopVideo, 6000);
                  done = true;
                }
              }
              function stopVideo() {
                player.stopVideo();
              }
              function getInputValue(){
          var inputVal = document.getElementById("userInput").value;    
            // get video id from url
            function getId(url) {
              const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
              const match = url.match(regExp);

              return (match && match[2].length === 11)
                ? match[2]
                : null;
            }
      } 
      
      </script>
        <!-- <form action="https://www.google.com/search" method="get">
            <div class="form-group">
              <input name="q" type="text" class="form-control"  aria-describedby="emailHelp" placeholder="search">
              <small id="emailHelp" class="form-text ">Search for videos or websites in this window</small>
            </div>
            <div class="form-group form-check">
              <input type="checkbox" class="form-check-input" id="exampleCheck1">
              <label class="form-check-label" for="exampleCheck1">Am not a Robot</label>
            </div>
            <button type="submit" class="btn btn-primary">Search</button>
          </form> -->
    </div>
  </div>
    
{% endblock %}
