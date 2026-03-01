/**
 * PetCare Triage Assistant -- Frontend Logic
 *
 * Author: Syed Ali Turab
 * Date:   March 1, 2026
 *
 * Handles the chat interface, session management, and voice interaction
 * for the PetCare Triage & Smart Booking Agent.
 *
 * Voice Support (3 Tiers):
 *   Tier 1: Browser-native Web Speech API (free, no API key)
 *   Tier 2: OpenAI Whisper (STT) + OpenAI TTS (speech synthesis)
 *   Tier 3: OpenAI Realtime API (future — interactive voice)
 *
 * The voice tier is auto-detected based on browser support and
 * server capabilities (Tier 2 requires OPENAI_API_KEY on backend).
 */

// ---------------------------------------------------------------------------
// Global State
// ---------------------------------------------------------------------------

let sessionId = null;           // Active session UUID
let isRecording = false;        // Whether voice recording is active
let mediaRecorder = null;       // MediaRecorder instance for Tier 2
let audioChunks = [];           // Collected audio chunks during recording
let voiceTier = 1;              // Current voice tier (1=browser, 2=whisper)
let speechRecognition = null;   // Web Speech API instance (Tier 1)
let ttsEnabled = true;          // Whether to speak responses aloud

// ---------------------------------------------------------------------------
// Initialization
// ---------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', initApp);

/**
 * Initialize the application on page load.
 *
 * Sets up event listeners for text input (Enter key to send),
 * checks voice support, and starts a new intake session.
 */
async function initApp() {
    // Set up text input: Enter sends message, Shift+Enter adds newline
    const input = document.getElementById('user-input');
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Detect available voice capabilities
    await detectVoiceSupport();

    // Start a new intake session with the backend
    await startSession();
}

// ---------------------------------------------------------------------------
// Voice Support Detection
// ---------------------------------------------------------------------------

/**
 * Detect which voice tier is available.
 *
 * Tier 1: Browser Web Speech API (SpeechRecognition).
 *         Works in Chrome, Edge, Safari (partial). Free, no API key.
 *
 * Tier 2: OpenAI Whisper + TTS via backend endpoints.
 *         Requires OPENAI_API_KEY configured on the server.
 *         Works in all browsers (uses MediaRecorder for audio capture).
 *
 * Sets the global voiceTier variable and updates the UI accordingly.
 */
async function detectVoiceSupport() {
    // Check Tier 1: Browser-native speech recognition
    const SpeechRecognition = window.SpeechRecognition ||
                               window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        speechRecognition = new SpeechRecognition();
        speechRecognition.continuous = false;    // Stop after one utterance
        speechRecognition.interimResults = false; // Only final results
        speechRecognition.lang = 'en-US';

        // When speech is recognized, send it as a message
        speechRecognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById('user-input').value = transcript;
            sendMessage();
        };

        speechRecognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            stopRecording();
        };

        speechRecognition.onend = () => {
            stopRecording();
        };
    }

    // Check Tier 2: Backend Whisper/TTS support
    try {
        const res = await fetch('/api/health');
        const data = await res.json();
        if (data.voice_enabled) {
            voiceTier = 2; // Server has OPENAI_API_KEY configured
        }
    } catch (err) {
        console.warn('Could not check voice support:', err);
    }

    // Show voice button if any tier is available
    if (speechRecognition || voiceTier >= 2) {
        const voiceBtn = document.getElementById('voice-btn');
        if (voiceBtn) voiceBtn.classList.remove('hidden');
    }

    console.log(`Voice tier: ${voiceTier} (1=browser, 2=whisper+tts)`);
}

// ---------------------------------------------------------------------------
// Session Management
// ---------------------------------------------------------------------------

/**
 * Start a new intake session by calling the backend.
 *
 * The server creates a session with a unique ID and returns a
 * welcome message that asks the owner about their pet type.
 */
async function startSession() {
    try {
        const res = await fetch('/api/session/start', { method: 'POST' });
        const data = await res.json();
        sessionId = data.session_id;
        addMessage(data.message, 'assistant');

        // Speak the welcome message if TTS is available
        speakText(data.message);
    } catch (err) {
        addMessage(
            'Unable to connect to the server. Please try again later.',
            'assistant'
        );
        console.error('Failed to start session:', err);
    }
}

// ---------------------------------------------------------------------------
// Message Handling
// ---------------------------------------------------------------------------

/**
 * Send the current text input as a message to the backend.
 *
 * The message is sent to /api/session/<id>/message and the response
 * is displayed in the chat. If the response contains an emergency
 * flag, it's styled differently.
 *
 * The message source ('text' or 'voice') is tracked for analytics.
 */
async function sendMessage(source = 'text') {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message || !sessionId) return;

    // Clear input and show the user's message
    input.value = '';
    addMessage(message, 'user');

    // Disable send button and show typing indicator
    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    showTypingIndicator();

    try {
        const res = await fetch(`/api/session/${sessionId}/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, source })
        });
        const data = await res.json();
        removeTypingIndicator();

        // Check if this is an emergency escalation
        const isEmergency = data.emergency ||
            data.state === 'emergency' ||
            (data.message && data.message.includes('EMERGENCY'));

        addMessage(data.message, 'assistant', isEmergency);

        // Speak the response aloud
        speakText(data.message);

    } catch (err) {
        removeTypingIndicator();
        addMessage('Something went wrong. Please try again.', 'assistant');
        console.error('Failed to send message:', err);
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

// ---------------------------------------------------------------------------
// Voice Recording
// ---------------------------------------------------------------------------

/**
 * Toggle voice recording on/off.
 *
 * Behavior depends on the current voice tier:
 *   Tier 1: Uses Web Speech API (browser handles everything)
 *   Tier 2: Uses MediaRecorder to capture audio, then sends to
 *           backend /api/voice/transcribe for Whisper transcription
 */
function toggleVoice() {
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
}

/**
 * Start voice recording.
 *
 * Tier 1: Starts the Web Speech API recognition.
 * Tier 2: Requests microphone access and starts MediaRecorder.
 */
async function startRecording() {
    isRecording = true;
    updateVoiceButton(true);

    if (voiceTier === 1 && speechRecognition) {
        // Tier 1: Browser-native speech recognition
        speechRecognition.start();

    } else if (voiceTier >= 2) {
        // Tier 2: Record audio for Whisper transcription
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: true
            });

            mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm'
            });
            audioChunks = [];

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) audioChunks.push(e.data);
            };

            // When recording stops, send audio to Whisper
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, {
                    type: 'audio/webm'
                });
                await transcribeAudio(audioBlob);

                // Stop all microphone tracks
                stream.getTracks().forEach(t => t.stop());
            };

            mediaRecorder.start();
        } catch (err) {
            console.error('Microphone access denied:', err);
            addMessage(
                'Microphone access is required for voice input. ' +
                'Please allow microphone access and try again.',
                'assistant'
            );
            stopRecording();
        }
    }
}

/**
 * Stop voice recording.
 *
 * Tier 1: Stops the Web Speech API (onresult handler fires).
 * Tier 2: Stops MediaRecorder (onstop handler sends to Whisper).
 */
function stopRecording() {
    isRecording = false;
    updateVoiceButton(false);

    if (voiceTier === 1 && speechRecognition) {
        speechRecognition.stop();
    } else if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
}

/**
 * Send recorded audio to the backend for Whisper transcription.
 *
 * The audio blob is sent as a multipart form upload to
 * /api/voice/transcribe. The backend calls OpenAI Whisper API
 * and returns the transcribed text, which is then sent as a message.
 *
 * @param {Blob} audioBlob - The recorded audio data (WebM format)
 */
async function transcribeAudio(audioBlob) {
    showTypingIndicator();

    try {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');

        const res = await fetch('/api/voice/transcribe', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        removeTypingIndicator();

        if (data.text) {
            // Put transcribed text in the input and send it
            document.getElementById('user-input').value = data.text;
            await sendMessage('voice');
        } else {
            addMessage(
                'Could not understand the audio. Please try again.',
                'assistant'
            );
        }
    } catch (err) {
        removeTypingIndicator();
        console.error('Transcription failed:', err);
        addMessage(
            'Voice transcription failed. Please type your message instead.',
            'assistant'
        );
    }
}

// ---------------------------------------------------------------------------
// Text-to-Speech (Response Playback)
// ---------------------------------------------------------------------------

/**
 * Speak text aloud using the best available TTS method.
 *
 * Tier 1: Uses browser-native SpeechSynthesis API (free).
 * Tier 2: Uses OpenAI TTS API via backend (higher quality).
 *
 * TTS can be toggled off by the user via the speaker button.
 *
 * @param {string} text - The text to speak aloud
 */
async function speakText(text) {
    if (!ttsEnabled || !text) return;

    if (voiceTier >= 2) {
        // Tier 2: OpenAI TTS via backend
        try {
            const res = await fetch('/api/voice/synthesize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, voice: 'nova' })
            });

            if (res.ok) {
                const audioBlob = await res.blob();
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                audio.play();
                return;
            }
        } catch (err) {
            console.warn('OpenAI TTS failed, falling back to browser:', err);
        }
    }

    // Tier 1 fallback: Browser-native TTS
    if ('speechSynthesis' in window) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.95;   // Slightly slower for clarity
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        window.speechSynthesis.speak(utterance);
    }
}

/**
 * Toggle text-to-speech on/off.
 * Updates the speaker button icon to reflect the current state.
 */
function toggleTTS() {
    ttsEnabled = !ttsEnabled;
    const ttsBtn = document.getElementById('tts-btn');
    if (ttsBtn) {
        ttsBtn.textContent = ttsEnabled ? '🔊' : '🔇';
        ttsBtn.title = ttsEnabled ?
            'Speaker on (click to mute)' :
            'Speaker off (click to unmute)';
    }
}

// ---------------------------------------------------------------------------
// UI Helpers
// ---------------------------------------------------------------------------

/**
 * Add a message bubble to the chat container.
 *
 * @param {string} text - The message text
 * @param {string} role - 'user' or 'assistant'
 * @param {boolean} isEmergency - If true, styles as emergency alert
 */
function addMessage(text, role, isEmergency = false) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = `message ${role}`;
    if (isEmergency) div.classList.add('emergency');
    div.textContent = text;
    container.appendChild(div);

    // Auto-scroll to the latest message
    container.scrollTop = container.scrollHeight;
}

/**
 * Show a typing indicator (three bouncing dots) in the chat.
 * Indicates the agent is processing the message.
 */
function showTypingIndicator() {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = 'message assistant';
    div.id = 'typing-indicator';
    div.innerHTML =
        '<div class="typing-indicator">' +
        '<span></span><span></span><span></span>' +
        '</div>';
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

/**
 * Remove the typing indicator from the chat.
 * Called when the agent's response arrives.
 */
function removeTypingIndicator() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}

/**
 * Update the voice button appearance based on recording state.
 *
 * @param {boolean} recording - Whether voice recording is active
 */
function updateVoiceButton(recording) {
    const voiceBtn = document.getElementById('voice-btn');
    if (!voiceBtn) return;

    if (recording) {
        voiceBtn.classList.add('recording');
        voiceBtn.textContent = '⏹';
        voiceBtn.title = 'Stop recording';
    } else {
        voiceBtn.classList.remove('recording');
        voiceBtn.textContent = '🎤';
        voiceBtn.title = 'Start voice input';
    }
}
