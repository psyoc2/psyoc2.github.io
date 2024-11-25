document.getElementById("send").addEventListener("click", async () => {
    const input = document.getElementById("user-input").value;
    const responseDiv = document.getElementById("response");

    if (!input) {
        responseDiv.textContent = "Please enter a question.";
        return;
    }

    // Clear the response area and show a loading message
    responseDiv.textContent = "Loading...";

    try {
        const response = await fetch("/process", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input }),
        });

        const data = await response.json();

        if (response.ok) {
            responseDiv.textContent = data.response;
        } else {
            responseDiv.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        responseDiv.textContent = `Network Error: ${error.message}`;
    }
});
