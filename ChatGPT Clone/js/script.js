// Configuration
const CONFIG = {
    API_URL: 'https://openrouter.ai/api/v1/chat/completions',
    API_KEY: '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',
    MODEL: 'deepseek/deepseek-r1:free',
    SITE_NAME: 'SiteName',
    SITE_URL: 'https://www.sitename.com'
};

// DOM Elements
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');

// Utility Functions
function adjustTextareaHeight() {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 168) + 'px';
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function newChat() {
    chatMessages.innerHTML = '';
    userInput.value = '';
    adjustTextareaHeight();
}

// Message Functions
function addMessage(content, isUser = false) {
    const messageContainer = document.createElement('div');
    messageContainer.className = `message-container ${isUser ? 'user-message-container' : 'assistant-message-container'}`;
    
    const message = document.createElement('div');
    message.className = 'message';
    
    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${isUser ? 'user-avatar' : 'assistant-avatar'}`;
    avatar.innerHTML = isUser ? '<i class="fas fa-user"></i>' : 'AI';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (isUser) {
        messageContent.textContent = content;
    } else {
        messageContent.innerHTML = content;
    }
    
    message.appendChild(avatar);
    message.appendChild(messageContent);
    messageContainer.appendChild(message);
    
    chatMessages.appendChild(messageContainer);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
    const messageContainer = document.createElement('div');
    messageContainer.className = 'message-container assistant-message-container';
    messageContainer.id = 'typingMessage';
    
    const message = document.createElement('div');
    message.className = 'message';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar assistant-avatar';
    avatar.textContent = 'AI';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = `
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    
    message.appendChild(avatar);
    message.appendChild(messageContent);
    messageContainer.appendChild(message);
    
    chatMessages.appendChild(messageContainer);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTyping() {
    const typingMessage = document.getElementById('typingMessage');
    if (typingMessage) {
        typingMessage.remove();
    }
}

// API Functions
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Disable send button and clear input
    sendButton.disabled = true;
    addMessage(message, true);
    userInput.value = '';
    adjustTextareaHeight();
    
    // Show typing indicator
    showTyping();
    
    try {
        const response = await fetch(CONFIG.API_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${CONFIG.API_KEY}`,
                'HTTP-Referer': CONFIG.SITE_URL,
                'X-Title': CONFIG.SITE_NAME,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model: CONFIG.MODEL,
                messages: [{ role: 'user', content: message }],
            }),
        });
        
        const data = await response.json();
        removeTyping();
        
        if (!response.ok) {
            throw new Error(data.error?.message || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        const botResponse = data.choices?.[0]?.message?.content || 'Sorry, I couldn\'t process your request.';
        const formattedResponse = marked.parse(botResponse);
        addMessage(formattedResponse, false);
    } catch (error) {
        removeTyping();
        addMessage(`<p><strong>Error:</strong> ${error.message}</p>`, false);
        console.error('API Error:', error);
    } finally {
        sendButton.disabled = false;
    }
}

// Event Listeners
userInput.addEventListener('keydown', handleKeyDown);
userInput.addEventListener('input', adjustTextareaHeight);
sendButton.addEventListener('click', sendMessage);

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    adjustTextareaHeight();
    
    // Focus on input when page loads
    userInput.focus();
});
