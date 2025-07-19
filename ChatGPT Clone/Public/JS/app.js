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
    } else {
        userProfile = {
            name: 'User',
            chatStyle: 'friendly',
            profilePicture: null
        };
        console.log('Created default user profile:', userProfile); // Debug log
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
        const role = msg.isUser ? 'User' : 'You';
        const content = msg.content.replace(/<[^>]*>/g, '').trim();
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
        avatar.innerHTML = `<img src="${userProfile.profilePicture}" alt="User" style="width: 100%; height: 100%; border-radius: 2px; object-fit: cover;">`;
    } else {
        avatar.innerHTML = isUser ? '<i class="fas fa-user"></i>' : 'AI';
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
    
    message.appendChild(avatar);
    message.appendChild(messageContent);
    messageContainer.appendChild(message);
    
    chatMessages.appendChild(messageContainer);
    chatMessages.scrollTop = chatMessages.scrollHeight;
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
    } finally {
        sendButton.disabled = false;
    }
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
