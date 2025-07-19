// User Profile Management
// =======================

let currentProfilePicture = null;

// Load existing profile data
function loadProfile() {
    const savedProfile = localStorage.getItem('chatgpt-user-profile');
    if (savedProfile) {
        const profile = JSON.parse(savedProfile);
        
        const usernameEl = document.getElementById('username');
        const preferredStyleEl = document.getElementById('preferredStyle');
        const currentNameEl = document.getElementById('currentName');
        
        if (usernameEl) usernameEl.value = profile.name || '';
        if (preferredStyleEl) preferredStyleEl.value = profile.chatStyle || 'friendly';
        if (currentNameEl) currentNameEl.textContent = profile.name || 'User';
        
        if (profile.profilePicture) {
            currentProfilePicture = profile.profilePicture;
            const profilePic = document.getElementById('profilePicture');
            const currentPicStatus = document.getElementById('currentPicStatus');
            
            if (profilePic) {
                profilePic.innerHTML = `<img src="${profile.profilePicture}" alt="Profile">`;
            }
            if (currentPicStatus) {
                currentPicStatus.textContent = 'Custom image';
            }
        }
    }
}

// Handle profile picture upload
function handleProfilePicUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
    }

    if (file.size > 5 * 1024 * 1024) {
        alert('Image size should be less than 5MB');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        currentProfilePicture = e.target.result;
        const profilePic = document.getElementById('profilePicture');
        const currentPicStatus = document.getElementById('currentPicStatus');
        
        if (profilePic) {
            profilePic.innerHTML = `<img src="${e.target.result}" alt="Profile">`;
        }
        if (currentPicStatus) {
            currentPicStatus.textContent = 'New image selected';
        }
    };
    reader.readAsDataURL(file);
}

// Save profile
function saveProfile(event) {
    event.preventDefault();
    
    const usernameEl = document.getElementById('username');
    const preferredStyleEl = document.getElementById('preferredStyle');
    
    const profile = {
        name: (usernameEl ? usernameEl.value.trim() : '') || 'User',
        chatStyle: preferredStyleEl ? preferredStyleEl.value : 'friendly',
        profilePicture: currentProfilePicture,
        lastUpdated: Date.now()
    };

    localStorage.setItem('chatgpt-user-profile', JSON.stringify(profile));
    
    // Show success message
    const successMsg = document.getElementById('successMessage');
    if (successMsg) {
        successMsg.style.display = 'block';
        setTimeout(() => {
            successMsg.style.display = 'none';
        }, 3000);
    }

    // Update current info
    loadProfile();
}

// Go back to chat
function goBack() {
    window.location.href = 'chatbot.html';
}

// Setup event listeners for profile page
function setupProfileEventListeners() {
    const profileForm = document.getElementById('profileForm');
    const profilePicInput = document.getElementById('profilePicInput');
    const backBtn = document.getElementById('backBtn');
    const uploadOverlay = document.getElementById('uploadOverlay');
    
    if (profileForm) {
        profileForm.addEventListener('submit', saveProfile);
    }
    
    if (profilePicInput) {
        profilePicInput.addEventListener('change', handleProfilePicUpload);
    }
    
    if (backBtn) {
        backBtn.addEventListener('click', goBack);
    }
    
    if (uploadOverlay) {
        uploadOverlay.addEventListener('click', function() {
            if (profilePicInput) {
                profilePicInput.click();
            }
        });
    }
}

// Initialize profile page
document.addEventListener('DOMContentLoaded', function() {
    loadProfile();
    setupProfileEventListeners();
});
