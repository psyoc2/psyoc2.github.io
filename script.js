// When the page loads, initialize with the opening question
window.onload = () => {
    const chatBox = document.getElementById('chat-box');
    const openingMessage = document.createElement('div');
    openingMessage.className = 'bot-message';
    openingMessage.textContent = "Hello! Enter the current date and time (YYYY-MM-DD HH:MM:SS):";
    chatBox.appendChild(openingMessage);
};

// Handle user input and send to the server
document.getElementById('send-button').addEventListener('click', () => {
    const userInput = document.getElementById('user-input').value;
    const chatBox = document.getElementById('chat-box');

    if (!userInput) return;

    // Display user message
    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);

    // Clear input field
    document.getElementById('user-input').value = '';

    // Fetch response from backend
    fetch('/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: userInput })
    })
        .then(response => response.json())
        .then(data => {
            const botMessage = document.createElement('div');
            botMessage.className = 'bot-message';
            botMessage.textContent = data.response;
            chatBox.appendChild(botMessage);

            // Scroll chatbox to the bottom
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
            const botMessage = document.createElement('div');
            botMessage.className = 'bot-message';
            botMessage.textContent = "Sorry, something went wrong. Please try again.";
            chatBox.appendChild(botMessage);
        });
});
