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