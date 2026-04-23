// Main JavaScript file

// Flash message auto-hide
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');

    const dismissMessage = (message) => {
        if (!message || message.classList.contains('is-hiding')) return;
        message.classList.add('is-hiding');
        setTimeout(() => message.remove(), 260);
    };

    flashMessages.forEach((message) => {
        const closeButton = message.querySelector('[data-flash-close], .flash-close, .btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => dismissMessage(message));
        }

        let autoHideTimer = setTimeout(() => dismissMessage(message), 6000);

        message.addEventListener('mouseenter', () => {
            clearTimeout(autoHideTimer);
        });

        message.addEventListener('mouseleave', () => {
            autoHideTimer = setTimeout(() => dismissMessage(message), 3000);
        });
    });
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
