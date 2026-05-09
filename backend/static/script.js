const messages = [];

let typingElement = null;


function scrollToBottom() {

    const chatBox = document.getElementById("chat-box");

    chatBox.scrollTop = chatBox.scrollHeight;
}


function addMessage(content, className) {

    const chatBox = document.getElementById("chat-box");

    const div = document.createElement("div");

    div.className = `message ${className}`;

    div.innerHTML = content;

    chatBox.appendChild(div);

    scrollToBottom();
}


function showTyping() {

    const chatBox = document.getElementById("chat-box");

    typingElement = document.createElement("div");

    typingElement.className = "message bot-message";

    typingElement.innerHTML = `
        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    chatBox.appendChild(typingElement);

    scrollToBottom();
}


function removeTyping() {

    if (typingElement) {
        typingElement.remove();
        typingElement = null;
    }
}


async function sendMessage() {

    const input = document.getElementById("user-input");

    const text = input.value.trim();

    if (!text) {
        return;
    }

    addMessage(text, "user-message");

    messages.push({
        role: "user",
        content: text
    });

    input.value = "";

    showTyping();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                messages: messages
            })
        });

        const data = await response.json();

        removeTyping();

        let botHTML = `
            <div>${data.reply}</div>
        `;

        if (data.recommendations.length > 0) {

            data.recommendations.forEach(item => {

                botHTML += `
                    <div class="recommendation-card">

                        <h3>${item.name}</h3>

                        <p>
                            Test Type: ${item.test_type}
                        </p>

                        <a href="${item.url}" target="_blank">
                            Open Assessment
                        </a>

                    </div>
                `;
            });
        }

        addMessage(botHTML, "bot-message");

        messages.push({
            role: "assistant",
            content: data.reply
        });

    } catch (error) {

        removeTyping();

        addMessage(
            "Something went wrong. Please try again.",
            "bot-message"
        );
    }
}


document
    .getElementById("user-input")
    .addEventListener("keypress", function(event) {

        if (event.key === "Enter") {
            sendMessage();
        }
    });