

// Podgląd url
function previewURL(input_id, div_name, link) {
  var input = document.getElementById(input_id)
  var div = document.getElementById(div_name);
  var URL = link + input.value;
  div.innerHTML = `
  <div class='py-3'>
    <span class='text-dark fw-bold' style='font-size: 0.8rem;'>CURRENT LINK PREVIEW: </span><br>
    <span class='font-weight-bold text-primary'>${URL}</span>
  </div>`;
}

// Czyszczenie podglądu
function clearURL(div_name) {
  var div = document.getElementById(div_name);
  div.innerHTML = "";
}
