document.getElementById("chatbot-send").addEventListener("click", async () => {
    const input = document.getElementById("chatbot-input").value.trim();
    const messagesDiv = document.getElementById("chatbot-messages");

    if (!input) {
        messagesDiv.innerHTML += `<p><strong>Sid:</strong> Please enter a message to ask the chatbot.</p>`;
        return;
    }

    // Display user's message in the chat
    messagesDiv.innerHTML += `<p><strong>You:</strong> ${input}</p>`;

    try {
        // Send the user message to the server
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input }),
        });

        // Process the server's response
        if (response.ok) {
            const data = await response.json();
            messagesDiv.innerHTML += `<p><strong>Sid:</strong> ${data.reply}</p>`;
        } else {
            messagesDiv.innerHTML += `<p><strong>Sid:</strong> Sorry, I couldn't process your request. Please try again.</p>`;
        }

        // Clear the input field and auto-scroll chatbox
        document.getElementById("chatbot-input").value = "";
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    } catch (error) {
        console.error("Error communicating with chatbot:", error);
        messagesDiv.innerHTML += `<p><strong>Sid:</strong> Sorry, I encountered an error while processing your request.</p>`;
    }
});
