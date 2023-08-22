const postIt = document.getElementById("postIt");
const optionsContainer = document.getElementById("optionsContainer");
const colorPicker = document.getElementById("colorPicker");
const fontColorPicker = document.getElementById("fontColorPicker");
let offsetX, offsetY, isDragging = false;

postIt.addEventListener("mousedown", startDragging);
postIt.addEventListener("mouseup", stopDragging);
postIt.addEventListener("mousemove", drag);

function startDragging(event) {
  isDragging = true;
  offsetX = event.clientX - postIt.getBoundingClientRect().left;
  offsetY = event.clientY - postIt.getBoundingClientRect().top;
}

function stopDragging() {
  isDragging = false;
}

function drag(event) {
  if (!isDragging || optionsContainer.style.display !== "block") return;

  const x = event.clientX - offsetX;
  const y = event.clientY - offsetY;

  postIt.style.left = x + "px";
  postIt.style.top = y + "px";
}

function toggleOptions() {
  const optionsContainer = document.getElementById('optionsContainer');

  if (optionsContainer.style.display === "" || optionsContainer.style.display === "none") {
    optionsContainer.style.display = "block";
    optionsContainer.classList.remove('animate__fadeOutLeft');
    optionsContainer.classList.add('animate__fadeInLeft');
  } else {
    optionsContainer.classList.remove('animate__fadeInLeft');
    optionsContainer.classList.add('animate__fadeOutLeft');

    setTimeout(() => {
      optionsContainer.style.display = "none";
    }, 500);
  }
}

function toggleColorPicker() {
  colorPicker.click();
}

function toggleFontColorPicker() {
  fontColorPicker.click();
}

function changeColor(event) {
  const newColor = event.target.value;
  postIt.style.backgroundColor = newColor;
  optionsContainer.style.display = "none";
}

function changeFontColor(event) {
  const newFontColor = event.target.value;
  const postItContent = postIt.querySelector('p');
  postItContent.style.color = newFontColor;
  optionsContainer.style.display = 'none';
}

function editTitle() {
  const titleElement = document.querySelector('.menu-title');
  const currentTitle = titleElement.innerText;
  const newTitle = prompt('Edite o título (limite de 30 caracteres):', currentTitle);

  if (newTitle !== null) {
    const truncatedTitle = newTitle.substring(0, 30);
    titleElement.innerText = truncatedTitle;
  }
}

function editText() {
  const postItContent = postIt.querySelector("p");
  const currentText = postItContent.innerText;
  const newText = prompt("Edite seu texto:", currentText);
  if (newText !== null) {
    postItContent.innerText = newText;
  }
}

function deletePostIt() {
  postIt.remove();
  optionsContainer.style.display = "none";
}
