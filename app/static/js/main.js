// Main JavaScript file

// Flash message auto-hide
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Add slide out animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideOut {
            to {
                transform: translateY(-100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});

// Utility functions
const utils = {
    // Show loading state on button
    showLoading(button) {
        button.classList.add('loading');
        button.disabled = true;
    },

    // Hide loading state on button
    hideLoading(button) {
        button.classList.remove('loading');
        button.disabled = false;
    },

    // Display error message
    showError(element, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'validation-error';
        errorDiv.textContent = message;
        element.parentNode.appendChild(errorDiv);
        element.classList.add('input-error');
    },

    // Clear errors
    clearErrors(form) {
        form.querySelectorAll('.validation-error').forEach(el => el.remove());
        form.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));
    },

    // Debounce function for performance
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Export for use in other files
window.utils = utils;