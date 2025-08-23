// Like button functionality
document.addEventListener('DOMContentLoaded', function() {
    // Handle like buttons
    document.querySelectorAll('form[action*="/like/"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const form = this;
            const url = form.getAttribute('action');
            const method = form.getAttribute('method');
            const formData = new FormData(form);
            
            fetch(url, {
                method: method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const button = form.querySelector('button');
                    const icon = button.querySelector('i');
                    const countElement = button.querySelector('span') || button.nextElementSibling;
                    
                    // Update button appearance
                    if (data.action === 'liked') {
                        button.classList.remove('btn-outline-danger');
                        button.classList.add('btn-danger');
                        icon.classList.add('heart-beat');
                    } else {
                        button.classList.remove('btn-danger');
                        button.classList.add('btn-outline-danger');
                    }
                    
                    // Update like count if element exists
                    if (countElement) {
                        countElement.textContent =  ;
                    }
                    
                    // Remove animation class after it completes
                    setTimeout(() => {
                        icon.classList.remove('heart-beat');
                    }, 1000);
                }
            });
        });
    });
    
    // Auto-size textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
});
