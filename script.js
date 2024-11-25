document.getElementById("send-btn").addEventListener("click", function () {
    const userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return;

    // Add user message to the chatbox
    addMessageToChatbox(userInput, "user");

    // Clear the input field
    document.getElementById("user-input").value = "";

    // Send the user input to the server
    fetch("/process", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            if (data.response) {
                addMessageToChatbox(data.response, "bot");
            } else {
                throw new Error("Invalid response from server");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            addMessageToChatbox("Sorry, something went wrong. Please try again.", "bot");
        });
});

function addMessageToChatbox(message, sender) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.className = sender;
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
