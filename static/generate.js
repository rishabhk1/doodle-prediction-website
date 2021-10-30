var topics=['banana','apple','bicycle','car','chair','shoe','lollipop','sandwich','headphones','eyeglasses','tshirt','diamond'];
function generate(){
    let x = Math.floor((Math.random() * 12));
    document.getElementById("generate").innerHTML = topics[x];
    document.getElementById("result").innerHTML ="";
    $("#clearButton").click()
}
window.addEventListener('load', (event) => {
    generate();
    
  })