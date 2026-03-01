/**
 * PetCare Triage Assistant -- Frontend Logic
 */

let sessionId = null;

document.addEventListener('DOMContentLoaded', initApp);

async function initApp() {
    const input = document.getElementById('user-input');
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    await startSession();
}

async function startSession() {
    try {
        const res = await fetch('/api/session/start', { method: 'POST' });
        const data = await res.json();
        sessionId = data.session_id;
        addMessage(data.message, 'assistant');
    } catch (err) {
        addMessage('Unable to connect to the server. Please try again later.', 'assistant');
        console.error('Failed to start session:', err);
    }
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message || !sessionId) return;

    input.value = '';
    addMessage(message, 'user');

    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    showTypingIndicator();

    try {
        const res = await fetch(`/api/session/${sessionId}/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await res.json();
        removeTypingIndicator();

        const isEmergency = data.state === 'emergency' ||
            (data.message && data.message.includes('EMERGENCY'));

        addMessage(data.message, 'assistant', isEmergency);
    } catch (err) {
        removeTypingIndicator();
        addMessage('Something went wrong. Please try again.', 'assistant');
        console.error('Failed to send message:', err);
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

function addMessage(text, role, isEmergency = false) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = `message ${role}`;
    if (isEmergency) div.classList.add('emergency');
    div.textContent = text;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function showTypingIndicator() {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = 'message assistant';
    div.id = 'typing-indicator';
    div.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function removeTypingIndicator() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}
