document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    // Display the initial question on page load
    appendMessage("Hello! Enter the current date and time (YYYY-MM-DD HH:MM:SS):", "bot");

    sendButton.addEventListener("click", async function () {
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        appendMessage(userMessage, "user");
        userInput.value = "";

        try {
            const response = await fetch("/process", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();
            appendMessage(data.message, "bot");
        } catch (error) {
            appendMessage("Sorry, something went wrong. Please try again.", "bot");
        }
    });

    function appendMessage(message, sender) {
        const messageElement = document.createElement("div");
        messageElement.className = `message ${sender}`;
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
