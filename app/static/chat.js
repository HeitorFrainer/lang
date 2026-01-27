// Chat functionality
document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const messageInput = document.getElementById('message-input');
    const messageText = messageInput.value.trim();
    
    if (!messageText) return;
    
    // Add user message to chat
    addMessage(messageText, 'user');
    messageInput.value = '';
    
    // Send message to server
    try {
        const response = await fetch('/api/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: messageText })
        });
        
        const data = await response.json();
        
        // Add bot response
        addMessage(data.response, 'bot');
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, there was an error. Please try again.', 'bot');
    }
});

function addMessage(text, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = `<p>${escapeHtml(text)}</p>`;
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
