// Configuration
const CONFIG = {
    API_URL: '/api/chat',
    MODEL: 'gemma3'
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
        
        // Add copy button for assistant messages
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.title = 'Copy message';
        copyButton.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
        `;
        
        copyButton.addEventListener('click', () => copyMessage(copyButton, content));
        messageContent.appendChild(copyButton);
    }
    
    message.appendChild(avatar);
    message.appendChild(messageContent);
    messageContainer.appendChild(message);
    
    chatMessages.appendChild(messageContainer);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Copy message function
function copyMessage(button, content) {
    // Extract text content from HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = content;
    const textContent = tempDiv.textContent || tempDiv.innerText || '';
    
    navigator.clipboard.writeText(textContent).then(() => {
        // Show success state
        button.classList.add('copied');
        button.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20,6 9,17 4,12"></polyline>
            </svg>
        `;
        button.title = 'Copied!';
        
        // Reset after 2 seconds
        setTimeout(() => {
            button.classList.remove('copied');
            button.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
            `;
            button.title = 'Copy message';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = textContent;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            button.classList.add('copied');
            button.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20,6 9,17 4,12"></polyline>
                </svg>
            `;
            button.title = 'Copied!';
            
            setTimeout(() => {
                button.classList.remove('copied');
                button.innerHTML = `
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                `;
                button.title = 'Copy message';
            }, 2000);
        } catch (err) {
            console.error('Fallback copy failed: ', err);
        }
        document.body.removeChild(textArea);
    });
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
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message
            }),
        });
        
        const data = await response.json();
        removeTyping();
        
        if (!response.ok) {
            throw new Error(data.error?.message || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        const botResponse = data.response || 'Sorry, I couldn\'t process your request.';
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
