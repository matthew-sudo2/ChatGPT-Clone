// UI Utilities and Event Handlers
// ================================

// Event handler for image upload button
function handleImageUploadClick() {
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.click();
    }
}

// Event handler for textarea input
function handleTextareaInput() {
    adjustTextareaHeight();
}

// Event handler for send button click
function handleSendClick() {
    sendMessage();
}

// Event handler for new chat button
function handleNewChatClick() {
    newChat();
}

// Event handler for profile section click
function handleProfileClick() {
    openProfile();
}

// Event handler for remove image button
function handleRemoveImageClick() {
    removeImage();
}

// Event handler for cancel button
function handleCancelClick() {
    // Clear any pending operations
    if (window.currentController) {
        window.currentController.abort();
        window.currentController = null;
    }
    
    // Remove typing indicator if present
    const typingMessage = document.getElementById('typingMessage');
    if (typingMessage) {
        typingMessage.remove();
    }
    
    // Clear input
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.value = '';
        userInput.style.height = 'auto';
    }
    
    // Remove any image preview
    removeImage();
    
    // Hide cancel button and enable send button
    toggleCancelButton(false);
    
    // Re-enable send button
    const sendButton = document.getElementById('sendButton');
    if (sendButton) {
        sendButton.disabled = false;
    }
}

// Utility to toggle cancel button visibility
function toggleCancelButton(show) {
    const cancelButton = document.getElementById('cancelButton');
    if (cancelButton) {
        cancelButton.style.display = show ? 'flex' : 'none';
    }
}

// Utility to setup all event listeners
function setupEventListeners() {
    // Image upload button
    const imageUploadBtn = document.querySelector('.image-upload-btn');
    if (imageUploadBtn) {
        imageUploadBtn.addEventListener('click', handleImageUploadClick);
    }
    
    // Image input change
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.addEventListener('change', handleImageUpload);
    }
    
    // Textarea events
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.addEventListener('input', handleTextareaInput);
        userInput.addEventListener('keydown', handleKeyDown);
    }
    
    // Send button
    const sendButton = document.getElementById('sendButton');
    if (sendButton) {
        sendButton.addEventListener('click', handleSendClick);
    }
    
    // Cancel button
    const cancelButton = document.getElementById('cancelButton');
    if (cancelButton) {
        cancelButton.addEventListener('click', handleCancelClick);
    }
    
    // New chat button
    const newChatBtn = document.querySelector('.new-chat-btn');
    if (newChatBtn) {
        newChatBtn.addEventListener('click', handleNewChatClick);
    }
    
    // Profile click handlers
    const userInfo = document.querySelector('.user-info');
    const profileBtn = document.querySelector('.profile-btn');
    
    if (userInfo) {
        userInfo.addEventListener('click', handleProfileClick);
    }
    if (profileBtn) {
        profileBtn.addEventListener('click', handleProfileClick);
    }
    
    // Model selector click
    const modelSelector = document.querySelector('.model-selector');
    if (modelSelector) {
        modelSelector.addEventListener('click', toggleModelDropdown);
    }
    
    // Model option clicks
    const modelOptions = document.querySelectorAll('.model-option');
    modelOptions.forEach(option => {
        option.addEventListener('click', function() {
            const modelId = this.dataset.model;
            const modelName = this.dataset.name;
            selectModel(modelId, modelName);
        });
    });
    
    // Remove image button
    const removeImageBtn = document.querySelector('.remove-image-btn');
    if (removeImageBtn) {
        removeImageBtn.addEventListener('click', handleRemoveImageClick);
    }
}

// Initialize UI when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});
