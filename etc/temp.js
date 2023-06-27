const fs = require('fs');

function wikiFetch(url){
    fetch(url)
    .then(function(response){return response.json();})
    .then(function(response){
        fs.writeFile("data.json", JSON.stringify(response), (error) => {
            // throwing the error
            // in case of a writing problem
            if (error) {
              // logging the error
              console.error(error);
          
              throw error;
            }
          
            console.log("data.json written correctly");
          })
    })
    .catch(function(error){console.log(error);});
  }

wikiFetch("https://commons.wikimedia.org/w/api.php?action=sitematrix&smtype=language&format=json")

/* const data = JSON.stringify(test)

fs.writeFile("data.json", data, (error) => {
    // throwing the error
    // in case of a writing problem
    if (error) {
      // logging the error
      console.error(error);
  
      throw error;
    }
  
    console.log("data.json written correctly");
  }); */