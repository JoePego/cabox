// SocketIO integration for chat
const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

socket.on('message', (msg) => {
  displayMessage(msg, 'incoming-message');
});

// Get elements
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const chatBox = document.getElementById('chat-box');
const menuToggle = document.getElementById("menu-toggle");
const wrapper = document.getElementById("main-wrapper"); // Updated ID
const profileForm = document.getElementById("profile-form");
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');
const sidebar = document.querySelector("#sidebar");
const hide_sidebar = document.querySelector(".hide-sidebar");
const new_chat_button = document.querySelector(".new-chat");

hide_sidebar.addEventListener( "click", function() {
  sidebar.classList.toggle( "hidden" );
} );

// Add event listeners
messageInput.addEventListener("keyup", (event) => {
  if (event.key === "Enter") {
    sendMessage();
  }
});

sendButton.addEventListener("click", sendMessage);

// Get the dropdown toggle button
const dropdownToggle = document.querySelector('.dropdown-toggle');

// Get the dropdown menu
const dropdownMenu = document.querySelector('.dropdown-menu');

// Add an event listener to the dropdown toggle button
dropdownToggle.addEventListener('click', () => {
  // Toggle the dropdown menu
  dropdownMenu.classList.toggle('show');
});

// Functions
function sendMessage() {
  const msg = messageInput.value.trim();
  if (msg !== "") {
    displayMessage(`You: ${msg}`, 'outgoing-message');
    socket.send(msg);
    messageInput.value = '';
  }
}

function displayMessage(msg, messageType) {
  const newMessage = document.createElement('div');
  newMessage.classList.add('message', messageType);
  newMessage.innerHTML = `<div class="message">${msg}</div>`;
  chatBox.appendChild(newMessage);
  chatBox.scrollTop = chatBox.scrollHeight;
}

new_chat_button.addEventListener("click", function() {
  show_view( ".new-chat-view" );
});

