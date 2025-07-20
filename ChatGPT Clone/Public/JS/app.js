// ChatGPT Clone - Main Application Logic
// ====================================

// Global Variables
let currentChatId = null;
let chats = {};
let currentImage = null;
let userProfile = null;

// ====================================
// USER PROFILE MANAGEMENT
// ====================================

function loadUserProfile() {
    const savedProfile = localStorage.getItem('chatgpt-user-profile');
    if (savedProfile) {
        userProfile = JSON.parse(savedProfile);
        console.log('Loaded user profile:', userProfile); // Debug log
        updateUserDisplay();
        
        // Apply saved theme
        applyTheme(userProfile.theme || 'dark');
    } else {
        userProfile = {
            name: 'User',
            chatStyle: 'friendly',
            theme: 'dark',
            profilePicture: null
        };
        console.log('Created default user profile:', userProfile); // Debug log
        applyTheme('dark');
    }
}

function updateUserDisplay() {
    if (!userProfile) return;
    
    // Update user name in sidebar
    const userNameEl = document.getElementById('userName');
    if (userNameEl) {
        userNameEl.textContent = userProfile.name || 'User';
    }
    
    // Update user avatar in sidebar
    const userAvatarSmall = document.getElementById('userAvatarSmall');
    if (userAvatarSmall) {
        if (userProfile.profilePicture) {
            userAvatarSmall.innerHTML = `<img src="${userProfile.profilePicture}" alt="Profile">`;
        } else {
            userAvatarSmall.innerHTML = '<i class="fas fa-user"></i>';
        }
    }
}

function openProfile() {
    window.location.href = 'profile.html';
}

// ====================================
// THEME MANAGEMENT
// ====================================

function applyTheme(theme) {
    if (theme === 'light') {
        document.body.classList.add('light-mode');
    } else {
        document.body.classList.remove('light-mode');
    }
}

// ====================================
// CONTEXT AND PERSONALIZATION
// ====================================

function getPersonalizedSystemPrompt() {
    if (!userProfile || !userProfile.name || userProfile.name === 'User') {
        console.log('No personalized prompt - using default profile');
        return '';
    }
    
    const currentChat = chats[currentChatId];
    const userMessageCount = currentChat ? currentChat.messages.filter(m => m.isUser).length : 0;
    
    // Only add personalized context for first 2-3 user messages
    if (userMessageCount > 2) {
        console.log('Skipping personalized prompt - too many messages');
        return '';
    }
    
    // Use the actual name directly, not as a template variable
    const userName = userProfile.name;
    console.log('Creating personalized prompt for user:', userName);
    let prompt = `IMPORTANT: The user's name is "${userName}" (this is their actual name, not a placeholder). Always use this exact name "${userName}" when referring to them. Never use any other name. Be consistent. `;
    
    switch (userProfile.chatStyle) {
        case 'professional':
            prompt += 'Maintain a professional and courteous tone.';
            break;
        case 'helpful':
            prompt += 'Provide detailed, helpful explanations and be thorough.';
            break;
        case 'creative':
            prompt += 'Be creative, fun, and engaging. Use emojis when appropriate.';
            break;
        case 'friendly':
        default:
            prompt += 'Be friendly, casual, and conversational.';
            break;
    }
    
    console.log('Generated prompt:', prompt);
    return prompt + ' ';
}

function getConversationContext() {
    if (!currentChatId || !chats[currentChatId]) return '';
    
    const currentChat = chats[currentChatId];
    const recentMessages = currentChat.messages.slice(-4);
    
    if (recentMessages.length < 2) return '';
    
    // For name-related questions, don't include previous conversation context
    // to avoid AI confusion from previous responses
    const lastUserMessage = recentMessages.filter(m => m.isUser).pop();
    if (lastUserMessage && lastUserMessage.content.toLowerCase().includes('name')) {
        return '';
    }
    
    let context = 'Recent conversation context:\n';
    recentMessages.forEach((msg, index) => {
        const role = msg.isUser ? 'User' : 'Assistant';
        let content = msg.content.replace(/<[^>]*>/g, '').trim();
        // Clean up any role prefixes from stored content
        content = content.replace(/^You:\s*/gi, '')
                        .replace(/\nYou:\s*/gi, '\n')
                        .replace(/^Assistant:\s*/gi, '')
                        .replace(/\nAssistant:\s*/gi, '\n');
        context += `${role}: ${content}\n`;
    });
    
    context += '\nContinue the conversation naturally, staying on topic. ';
    
    return context;
}

// ====================================
// IMAGE HANDLING
// ====================================

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        alert('Image size should be less than 10MB');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        currentImage = e.target.result.split(',')[1];
        
        const preview = document.getElementById('imagePreview');
        const previewImg = document.getElementById('previewImage');
        if (preview && previewImg) {
            previewImg.src = e.target.result;
            preview.style.display = 'block';
        }
    };
    reader.readAsDataURL(file);
}

function removeImage() {
    currentImage = null;
    const preview = document.getElementById('imagePreview');
    const input = document.getElementById('imageInput');
    
    if (preview) preview.style.display = 'none';
    if (input) input.value = '';
}

// ====================================
// CHAT PERSISTENCE
// ====================================

function loadChats() {
    const savedChats = localStorage.getItem('chatgpt-chats');
    if (savedChats) {
        chats = JSON.parse(savedChats);
    }
}

function saveChats() {
    localStorage.setItem('chatgpt-chats', JSON.stringify(chats));
}

function generateChatId() {
    return 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function getChatTitle(messages) {
    if (messages.length > 0) {
        const firstMessage = messages[0].content;
        return firstMessage.length > 30 ? firstMessage.substring(0, 30) + '...' : firstMessage;
    }
    return 'New Chat';
}

// ====================================
// CHAT MANAGEMENT
// ====================================

function newChat() {
    // Save current chat if it exists
    if (currentChatId && chats[currentChatId]) {
        chats[currentChatId].lastUpdated = Date.now();
        saveChats();
    }

    // Create new chat
    currentChatId = generateChatId();
    chats[currentChatId] = {
        id: currentChatId,
        title: 'New Chat',
        messages: [],
        created: Date.now(),
        lastUpdated: Date.now()
    };

    // Clear chat area
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    
    if (chatMessages) chatMessages.innerHTML = '';
    if (userInput) {
        userInput.value = '';
        adjustTextareaHeight();
    }

    // Add welcome message if user has a name
    if (userProfile && userProfile.name && userProfile.name !== 'User') {
        const welcomeMessages = [
            `Hey ${userProfile.name}! What's on your mind? 💭`,
            `Hi there! How can I help you today?`,
            `Ready to chat, ${userProfile.name}? 😊`,
            `What would you like to explore today?`,
            `Hey! What can I help you with?`
        ];
        const randomWelcome = welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)];
        addMessageToDOM(randomWelcome, false);
    }

    updateChatHistory();
    saveChats();
}

function loadChat(chatId) {
    // Save current chat first
    if (currentChatId && chats[currentChatId]) {
        chats[currentChatId].lastUpdated = Date.now();
        saveChats();
    }

    currentChatId = chatId;
    const chat = chats[chatId];
    
    if (!chat) return;

    // Clear and load messages
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.innerHTML = '';
        chat.messages.forEach(msg => {
            addMessageToDOM(msg.content, msg.isUser, msg.imageData);
        });
    }

    updateChatHistory();
}

function deleteChat(chatId, event) {
    event.stopPropagation();
    
    if (confirm('Are you sure you want to delete this chat?')) {
        delete chats[chatId];
        
        if (currentChatId === chatId) {
            newChat();
        } else {
            updateChatHistory();
        }
        
        saveChats();
    }
}

function updateChatHistory() {
    const chatHistory = document.getElementById('chatHistory');
    if (!chatHistory) return;
    
    chatHistory.innerHTML = '';

    const sortedChats = Object.values(chats).sort((a, b) => b.lastUpdated - a.lastUpdated);

    sortedChats.forEach(chat => {
        const chatItem = document.createElement('div');
        chatItem.className = `chat-item ${chat.id === currentChatId ? 'active' : ''}`;
        chatItem.onclick = () => loadChat(chat.id);
        
        chatItem.innerHTML = `
            <i class="fas fa-message"></i>
            <span class="chat-title">${chat.title}</span>
            <button class="delete-chat-btn" onclick="deleteChat('${chat.id}', event)" title="Delete chat">
                <i class="fas fa-trash"></i>
            </button>
        `;
        
        chatHistory.appendChild(chatItem);
    });

    if (sortedChats.length === 0) {
        newChat();
    }
}

// ====================================
// UI UTILITIES
// ====================================

function adjustTextareaHeight() {
    const textarea = document.getElementById('userInput');
    if (textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 168) + 'px';
    }
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// ====================================
// MESSAGE HANDLING
// ====================================

function addMessage(content, isUser = false, imageData = null) {
    let displayContent = content;
    if (!isUser) {
        // Clean up system prompts that might leak through
        displayContent = content.replace(/Conversation context[\s\S]*?Current user message:/gi, '')
                               .replace(/Previous conversation context:[\s\S]*?Current user message:/gi, '')
                               .replace(/You are chatting with[\s\S]*?Current user message:/gi, '')
                               .replace(/IMPORTANT:[\s\S]*?discussed\./gi, '')
                               .replace(/IMPORTANT:[\s\S]*?different\./gi, '')
                               .replace(/^You:\s*/gmi, '') // Remove "You:" at start (multiline)
                               .replace(/\nYou:\s*/gi, '\n') // Remove "You:" after line breaks
                               .replace(/You:\s*You:\s*/gi, '') // Remove "You: You:" duplications
                               .replace(/^You:\s*You:\s*/gmi, '') // Remove "You: You:" at start (multiline)
                               .replace(/^Assistant:\s*/gmi, '') // Remove "Assistant:" at start (multiline)
                               .replace(/\nAssistant:\s*/gi, '\n') // Remove "Assistant:" after line breaks
                               .replace(/Assistant:\s*Assistant:\s*/gi, '') // Remove "Assistant: Assistant:" duplications
                               .replace(/^Assistant:\s*Assistant:\s*/gmi, '') // Remove duplicate at start
                               .trim();
        
        if (displayContent.length === 0) {
            displayContent = content;
        }
    }
    
    // Add to current chat's messages
    if (currentChatId && chats[currentChatId]) {
        chats[currentChatId].messages.push({
            content: displayContent,
            isUser: isUser,
            imageData: imageData,
            timestamp: Date.now()
        });

        // Update chat title based on first user message
        if (isUser && chats[currentChatId].messages.filter(m => m.isUser).length === 1) {
            chats[currentChatId].title = getChatTitle([{content: displayContent}]);
            updateChatHistory();
        }

        chats[currentChatId].lastUpdated = Date.now();
        saveChats();
    }

    addMessageToDOM(displayContent, isUser, imageData);
}

function addMessageToDOM(content, isUser = false, imageData = null) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    const messageContainer = document.createElement('div');
    messageContainer.className = `message-container ${isUser ? 'user-message-container' : 'assistant-message-container'}`;
    
    const message = document.createElement('div');
    message.className = 'message';
    
    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${isUser ? 'user-avatar' : 'assistant-avatar'}`;
    
    if (isUser && userProfile && userProfile.profilePicture) {
        avatar.innerHTML = `<img src="${userProfile.profilePicture}" alt="User">`;
    } else {
        avatar.innerHTML = isUser ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    }
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // Add image if present
    if (imageData) {
        const img = document.createElement('img');
        img.src = `data:image/jpeg;base64,${imageData}`;
        img.className = 'message-image';
        messageContent.appendChild(img);
    }
    
    // Add text content
    if (content) {
        const textDiv = document.createElement('div');
        if (isUser) {
            textDiv.textContent = content;
        } else {
            textDiv.innerHTML = content;
        }
        messageContent.appendChild(textDiv);
    }

    // Add copy button for assistant messages
    if (!isUser) {
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
    
    return messageContainer;
}

async function addMessageWithTypewriter(content, isUser = false, imageData = null) {
    if (isUser) {
        // For user messages, use normal display
        addMessage(content, isUser, imageData);
        return;
    }
    
    // Add to chat history first
    if (currentChatId && chats[currentChatId]) {
        let displayContent = content;
        // Clean up system prompts that might leak through
        displayContent = content.replace(/Conversation context[\s\S]*?Current user message:/gi, '')
                               .replace(/Previous conversation context:[\s\S]*?Current user message:/gi, '')
                               .replace(/You are chatting with[\s\S]*?Current user message:/gi, '')
                               .replace(/IMPORTANT:[\s\S]*?discussed\./gi, '')
                               .replace(/IMPORTANT:[\s\S]*?different\./gi, '')
                               .replace(/^You:\s*/gmi, '') // Remove "You:" at start (multiline)
                               .replace(/\nYou:\s*/gi, '\n') // Remove "You:" after line breaks
                               .replace(/You:\s*You:\s*/gi, '') // Remove "You: You:" duplications
                               .replace(/^You:\s*You:\s*/gmi, '') // Remove "You: You:" at start (multiline)
                               .replace(/^Assistant:\s*/gmi, '') // Remove "Assistant:" at start (multiline)
                               .replace(/\nAssistant:\s*/gi, '\n') // Remove "Assistant:" after line breaks
                               .replace(/Assistant:\s*Assistant:\s*/gi, '') // Remove "Assistant: Assistant:" duplications
                               .replace(/^Assistant:\s*Assistant:\s*/gmi, '') // Remove duplicate at start
                               .trim();
        
        if (displayContent.length === 0) {
            displayContent = content;
        }
        
        chats[currentChatId].messages.push({
            content: displayContent,
            isUser: isUser,
            imageData: imageData,
            timestamp: Date.now()
        });

        chats[currentChatId].lastUpdated = Date.now();
        saveChats();
    }
    
    // Create message container for AI response
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    const messageContainer = document.createElement('div');
    messageContainer.className = 'message-container assistant-message-container';
    
    const message = document.createElement('div');
    message.className = 'message';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar assistant-avatar';
    avatar.innerHTML = '<i class="fas fa-robot"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // Add image if present
    if (imageData) {
        const img = document.createElement('img');
        img.src = `data:image/jpeg;base64,${imageData}`;
        img.className = 'message-image';
        messageContent.appendChild(img);
    }
    
    // Create text container
    const textDiv = document.createElement('div');
    messageContent.appendChild(textDiv);
    
    message.appendChild(avatar);
    message.appendChild(messageContent);
    messageContainer.appendChild(message);
    
    chatMessages.appendChild(messageContainer);
    
    // Clean the content for display (same cleanup as other functions)
    let cleanContent = content.replace(/Conversation context[\s\S]*?Current user message:/gi, '')
                             .replace(/Previous conversation context:[\s\S]*?Current user message:/gi, '')
                             .replace(/You are chatting with[\s\S]*?Current user message:/gi, '')
                             .replace(/IMPORTANT:[\s\S]*?discussed\./gi, '')
                             .replace(/IMPORTANT:[\s\S]*?different\./gi, '')
                             .replace(/^You:\s*/gmi, '') // Remove "You:" at start (multiline)
                             .replace(/\nYou:\s*/gi, '\n') // Remove "You:" after line breaks
                             .replace(/You:\s*You:\s*/gi, '') // Remove "You: You:" duplications
                             .replace(/^You:\s*You:\s*/gmi, '') // Remove "You: You:" at start (multiline)
                             .replace(/^Assistant:\s*/gmi, '') // Remove "Assistant:" at start (multiline)
                             .replace(/\nAssistant:\s*/gi, '\n') // Remove "Assistant:" after line breaks
                             .replace(/Assistant:\s*Assistant:\s*/gi, '') // Remove "Assistant: Assistant:" duplications
                             .replace(/^Assistant:\s*Assistant:\s*/gmi, '') // Remove duplicate at start
                             .trim();
    
    if (cleanContent.length === 0) {
        cleanContent = content;
    }
    
    // Typewriter effect
    const plainText = cleanContent.replace(/<[^>]*>/g, ''); // Remove HTML tags for typing
    let currentIndex = 0;
    
    // Start with empty content
    textDiv.innerHTML = '';
    
    const typeInterval = setInterval(() => {
        if (currentIndex < plainText.length) {
            // Add next character
            const partialText = plainText.substring(0, currentIndex + 1);
            
            // Convert back to HTML for proper rendering (simplified approach)
            // For more complex HTML, you'd need a more sophisticated parser
            let displayText = partialText;
            
            // Handle basic markdown/HTML formatting
            displayText = displayText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            displayText = displayText.replace(/\*(.*?)\*/g, '<em>$1</em>');
            displayText = displayText.replace(/\n/g, '<br>');
            
            textDiv.innerHTML = displayText + '<span class="typewriter-cursor">|</span>';
            
            currentIndex++;
            
            // Auto-scroll as text appears
            chatMessages.scrollTop = chatMessages.scrollHeight;
        } else {
            // Typing complete
            clearInterval(typeInterval);
            textDiv.innerHTML = cleanContent; // Use cleaned formatted content
        }
    }, 7); // Made faster: changed from 30ms to 15ms
}

function showTyping() {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
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

// ====================================
// API COMMUNICATION
// ====================================

async function sendMessage() {
    const input = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    if (!input || !sendButton) return;
    
    const message = input.value.trim();
    
    if (!message && !currentImage) {
        return;
    }
    
    sendButton.disabled = true;
    // Show cancel button and create abort controller
    toggleCancelButton(true);
    window.currentController = new AbortController();
    
    const userMessage = message || "What's in this image?"; 
    addMessage(userMessage, true, currentImage);
    input.value = '';
    adjustTextareaHeight();
    
    const imageToSend = currentImage;
    if (currentImage) {
        removeImage();
    }
    
    showTyping();
    
    try {
        let messageToSend = userMessage;
        const personalizedContext = getPersonalizedSystemPrompt();
        const conversationContext = getConversationContext();
        
        // For name-related questions, always include personalized context
        const isNameQuestion = userMessage.toLowerCase().includes('name');
        let forcePersonalizedContext = '';
        if (isNameQuestion && userProfile && userProfile.name && userProfile.name !== 'User') {
            forcePersonalizedContext = `REMEMBER: The user's name is "${userProfile.name}". This is their actual name. `;
        }
        
        if (personalizedContext || conversationContext || forcePersonalizedContext) {
            let fullContext = '';
            
            if (forcePersonalizedContext) {
                fullContext += forcePersonalizedContext + '\n';
            }
            
            if (personalizedContext) {
                fullContext += personalizedContext + '\n';
            }
            
            if (conversationContext) {
                fullContext += conversationContext + '\n';
            }
            
            messageToSend = fullContext + '\nCurrent user message: ' + userMessage;
        }
        
        const requestBody = {
            message: messageToSend
        };
        
        if (imageToSend) {
            requestBody.image = imageToSend;
        }
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
            signal: window.currentController?.signal
        });
        
        const data = await response.json();
        removeTyping();
        
        if (!response.ok) {
            throw new Error(data.error?.message || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        const botResponse = data.response || 'Sorry, I couldn\'t process your request.';
        const formattedResponse = marked.parse(botResponse);
        
        // Add message with typewriter effect for AI responses
        addMessageWithTypewriter(formattedResponse, false);
    } catch (error) {
        removeTyping();
        // Don't show error message if user intentionally cancelled
        // Check for various abort-related error types and messages
        const isAbortError = error.name === 'AbortError' || 
                           error.message.includes('aborted') || 
                           error.message.includes('abort') ||
                           error.code === 20; // DOMException.ABORT_ERR
        
        if (!isAbortError) {
            addMessage(`<p><strong>Error:</strong> ${error.message}</p>`, false);
        }
    } finally {
        sendButton.disabled = false;
        // Hide cancel button and cleanup
        toggleCancelButton(false);
        window.currentController = null;
    }
}

// ====================================
// COPY MESSAGE FUNCTIONALITY
// ====================================

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
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2 2v1"></path>
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

// ====================================
// INITIALIZATION
// ====================================

function initializeApp() {
    adjustTextareaHeight();
    loadUserProfile();
    loadChats();
    
    if (Object.keys(chats).length === 0) {
        newChat();
    } else {
        const sortedChats = Object.values(chats).sort((a, b) => b.lastUpdated - a.lastUpdated);
        if (sortedChats.length > 0) {
            loadChat(sortedChats[0].id);
        }
    }
    
    updateChatHistory();
}

// Start the application when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeApp);
