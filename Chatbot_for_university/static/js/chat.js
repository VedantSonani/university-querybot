// Chat elements
const chatContainer = document.getElementById('chat-container');
const chatDisplay = document.getElementById('chat-display');
const messageInput = document.getElementById('message-input');

// Toggle chat window visibility
function toggleChat() {
    chatContainer.style.display = 
        chatContainer.style.display === 'none' || 
        chatContainer.style.display === '' ? 'flex' : 'none';
    
    if (chatContainer.style.display === 'flex') {
        messageInput.focus();
        // Add welcome message if chat is empty
        if (chatDisplay.children.length === 0) {
            addMessage('Hello! How can I help you today?', 'bot');
        }
    }
}

// Send message function
// function sendMessage() {
//     const message = messageInput.value.trim();
    
//     if (message) {
//         // Add user message to chat
//         addMessage(message, 'user');
        
//         // Send message to Flask backend
//         fetch('/chat', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-Requested-With': 'XMLHttpRequest'  // For Flask to detect AJAX request
//             },
//             body: JSON.stringify({ message: message })
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             // Add bot response to chat
//             addMessage(data.response, 'bot');
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             addMessage('Sorry, there was an error processing your message. Please try again.', 'bot');
//         });

//         // Clear input
//         messageInput.value = '';
//     }
// }

function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        addMessage(message, 'user');
        messageInput.value = '';
        
        fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({message: message}),
        })
        .then(response => response.json())
        .then(data => {
            addMessage(data.response, false);
        })
        .catch((error) => {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request.', false);
        });
    }
}


// Add message to chat display
function addMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    
    // Create text content
    const textSpan = document.createElement('span');
    textSpan.textContent = message;
    messageDiv.appendChild(textSpan);
    
    // Add timestamp
    const timestamp = document.createElement('div');
    timestamp.classList.add('message-timestamp');
    timestamp.textContent = new Date().toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    messageDiv.appendChild(timestamp);
    
    // Add to chat display
    chatDisplay.appendChild(messageDiv);
    
    // Scroll to bottom
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

// Handle enter key in input
messageInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); // Prevent default to avoid new line
        sendMessage();
    }
});

// Handle click outside chat container to close
document.addEventListener('click', function(e) {
    if (!chatContainer.contains(e.target) && 
        !e.target.classList.contains('chatbot-icon')) {
        chatContainer.style.display = 'none';
    }
});

// Add loading indicator
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('message', 'bot-message', 'loading');
    loadingDiv.textContent = 'Typing...';
    chatDisplay.appendChild(loadingDiv);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
    return loadingDiv;
}

function removeLoading(loadingDiv) {
    if (loadingDiv && loadingDiv.parentNode) {
        loadingDiv.parentNode.removeChild(loadingDiv);
    }
}

// Add these styles to your CSS
const styles = `
.message-timestamp {
    font-size: 0.7em;
    color: #666;
    margin-top: 4px;
}

.loading {
    color: #666;
    font-style: italic;
}

.user-message {
    background-color: #003366;
    color: white;
    margin-left: auto;
    padding: 10px 15px;
}

.bot-message {
    background-color: #e9ecef;
    color: #333;
    margin-right: auto;
    padding: 10px 15px;
}

.message {
    max-width: 80%;
    margin: 10px 0;
    border-radius: 10px;
    word-wrap: break-word;
}
`;

// Add error handling for network issues
window.addEventListener('online', function() {
    addMessage('Connection restored. You can continue chatting.', 'bot');
});

window.addEventListener('offline', function() {
    addMessage('Connection lost. Please check your internet connection.', 'bot');
});

// Initialize chat
document.addEventListener('DOMContentLoaded', function() {
    // Reset chat display
    chatDisplay.innerHTML = '';
    
    // Make sure chat is hidden by default
    chatContainer.style.display = 'none';
});
