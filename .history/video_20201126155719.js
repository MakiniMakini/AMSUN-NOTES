// get video id from link
function getId(url) {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);

    return (match && match[2].length === 11)
      ? match[2]
      : null;
  }


        // extracts id from link
        function getInputValue(){
            var inputVal = document.getElementById("userInput").value;  
        }
        var idKali = getId(inputVal)


        // <!-- <form action="https://www.google.com/search" method="get">
        //     <div class="form-group">
        //       <input name="q" type="text" class="form-control"  aria-describedby="emailHelp" placeholder="search">
        //       <small id="emailHelp" class="form-text ">Search for videos or websites in this window</small>
        //     </div>
        //     <div class="form-group form-check">
        //       <input type="checkbox" class="form-check-input" id="exampleCheck1">
        //       <label class="form-check-label" for="exampleCheck1">Am not a Robot</label>
        //     </div>
        //     <button type="submit" class="btn btn-primary">Search</button>
        //   </form> -->