document.getElementById("send").addEventListener("click", async () => {
    const input = document.getElementById("user-input").value;
    const chatContainer = document.getElementById("chat-container");

    if (!input) return;

    // Add user message to chat
    const userMessage = document.createElement("div");
    userMessage.className = "user-message chat-message";
    userMessage.textContent = input;
    chatContainer.appendChild(userMessage);

    try {
        const response = await fetch("/process", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input }),
        });

        const data = await response.json();

        // Add bot response to chat
        const botMessage = document.createElement("div");
        botMessage.className = "bot-message chat-message";

        if (response.ok) {
            botMessage.textContent = data.response;
        } else {
            botMessage.textContent = `Error: ${data.error}`;
        }

        chatContainer.appendChild(botMessage);

    } catch (error) {
        const errorMessage = document.createElement("div");
        errorMessage.className = "bot-message chat-message";
        errorMessage.textContent = `Network Error: ${error.message}`;
        chatContainer.appendChild(errorMessage);
    }

    // Clear input
    document.getElementById("user-input").value = "";
});
