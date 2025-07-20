// Model Selection Component
// ========================

let currentModel = 'gemma3';
let isDropdownOpen = false;

// Model configurations
const models = {
    'gemma3': {
        name: 'Gemma 3',
        description: 'Fast and efficient'
    },
    'deepseek-r1': {
        name: 'DeepSeek R1',
        description: 'Advanced reasoning'
    }
};

function toggleModelDropdown() {
    const dropdown = document.getElementById('modelDropdown');
    const icon = document.getElementById('dropdownIcon');
    
    if (!dropdown || !icon) return;
    
    isDropdownOpen = !isDropdownOpen;
    
    if (isDropdownOpen) {
        dropdown.classList.add('show');
        icon.style.transform = 'rotate(180deg)';
    } else {
        dropdown.classList.remove('show');
        icon.style.transform = 'rotate(0deg)';
    }
}

function selectModel(modelId, modelName) {
    currentModel = modelId;
    
    const currentModelEl = document.getElementById('currentModel');
    if (currentModelEl) {
        currentModelEl.textContent = modelName;
    }
    
    // Update active state in dropdown
    const options = document.querySelectorAll('.model-option');
    options.forEach(option => {
        option.classList.remove('active');
        if (option.dataset.model === modelId) {
            option.classList.add('active');
        }
    });
    
    // Close dropdown
    toggleModelDropdown();
    
    console.log(`Switched to model: ${modelName}`);
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const modelSelector = document.querySelector('.model-selector');
    const dropdown = document.getElementById('modelDropdown');
    
    if (modelSelector && dropdown && isDropdownOpen) {
        if (!modelSelector.contains(event.target)) {
            toggleModelDropdown();
        }
    }
});

// Initialize model selector
document.addEventListener('DOMContentLoaded', function() {
    // Set initial model
    const initialModel = models[currentModel];
    if (initialModel) {
        const currentModelEl = document.getElementById('currentModel');
        if (currentModelEl) {
            currentModelEl.textContent = initialModel.name;
        }
    }
});
