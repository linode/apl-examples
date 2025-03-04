const host = window.location.host;
let socketUrl;
if (window.location.protocol === 'http:') {
    socketUrl = `ws://${host}/ws`
} else {
    socketUrl = `wss://${host}/ws`
}
const socket = new WebSocket(socketUrl);

function appendMessage(text) {
    const messages = document.getElementById('messages')
    const message = document.createElement('li')
    const content = document.createTextNode(text)
    message.appendChild(content)
    messages.appendChild(message)
}

function sendMessage() {
    const input = document.getElementById("messageText")
    socket.send(input.value)
    input.value = ''
    event.preventDefault()
}

socket.onopen = (event) => {
    appendMessage('Connected to WebSocket');
};

socket.onmessage = (event) => {
    appendMessage(event.data)
};

socket.onclose = (event) => {
    appendMessage('Disconnected from WebSocket');
};

window.sendMessage = sendMessage;
