// Fem-MultiModel Frontend Application
class FemMultiModel {
    constructor() {
        this.isProcessing = false;
        this.currentResponse = '';
        this.init();
    }

    formatResponse(text) {
        // Format the response text with proper line breaks and styling
        return text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    }

    init() {
        this.bindEvents();
        this.showEmptyState();
    }

    bindEvents() {
        const form = document.getElementById('problemForm');
        const solveBtn = document.getElementById('solveBtn');
        const textarea = document.getElementById('problemInput');

        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.solveProblem();
            });
        }

        // Auto-resize textarea
        if (textarea) {
            textarea.addEventListener('input', () => {
                textarea.style.height = 'auto';
                textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
            });
        }

        // Example problem selection
        document.querySelectorAll('.suggestion-btn').forEach(item => {
            item.addEventListener('click', () => {
                const exampleType = item.dataset.example;
                const exampleText = this.getExampleText(exampleType);
                if (textarea) {
                    textarea.value = exampleText;
                    textarea.style.height = 'auto';
                    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
                    textarea.focus();
                }
            });
        });

        // Attach button (example)
        const attachBtn = document.querySelector('.attach-btn');
        if (attachBtn) {
            attachBtn.addEventListener('click', () => {
                const exampleText = "A 1D bar of length 2 m, cross-sectional area A = 0.01 m², and Young's modulus E = 200 GPa is fixed at the left end and subjected to an axial force of 1000 N at the right end. Discretize the bar into 2 equal elements, and use linear shape functions. Find the displacement at the free end (right end).";
                if (textarea) {
                    textarea.value = exampleText;
                    textarea.style.height = 'auto';
                    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
                    textarea.focus();
                }
            });
        }
    }

    getExampleText(type) {
        const examples = {
            '1D bar structural analysis': "A 1D bar of length 2 m, cross-sectional area A = 0.01 m², and Young's modulus E = 200 GPa is fixed at the left end and subjected to an axial force of 1000 N at the right end. Discretize the bar into 2 equal elements, and use linear shape functions. Find the displacement at the free end (right end).",
            'Beam bending analysis': "A simply supported beam of length 4 m with rectangular cross-section (width = 0.2 m, height = 0.3 m) is subjected to a uniformly distributed load of 10 kN/m. The beam material has Young's modulus E = 25 GPa. Use beam elements to find the maximum deflection and bending moments.",
            'Truss structure analysis': "Analyze a 2D truss structure with 3 nodes forming a triangular configuration. Node 1 is fixed, Node 2 is pinned, and Node 3 has a vertical load of 5000 N. All members have cross-sectional area A = 0.001 m² and Young's modulus E = 200 GPa. Find the nodal displacements and member forces."
        };
        return examples[type] || examples['1D bar structural analysis'];
    }

    showEmptyState() {
        const chatMessages = document.getElementById('chatMessages');
        if (chatMessages) {
            chatMessages.style.display = 'none';
            chatMessages.classList.remove('active');
            this.clearChatMessages();
        }
    }

    hideEmptyState() {
        const chatMessages = document.getElementById('chatMessages');
        if (chatMessages) {
            chatMessages.style.display = 'block';
            chatMessages.classList.add('active');
        }
    }

    clearChatMessages() {
        const chatMessages = document.getElementById('chatMessages');
        if (chatMessages) {
            // Remove all messages except empty state
            const messages = chatMessages.querySelectorAll('.chat-message, .typing-indicator');
            messages.forEach(msg => msg.remove());
        }
    }

    addUserMessage(message) {
        this.hideEmptyState();
        const chatMessages = document.getElementById('chatMessages');
        if (chatMessages) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'chat-message message-user';
            messageDiv.innerHTML = `
                <div class="message-bubble">
                    ${message}
                </div>
            `;
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    addAssistantMessage(message, isTyping = false) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;
        
        if (isTyping) {
            // Add typing indicator
            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing-indicator';
            typingDiv.innerHTML = `
                <div class="message-bubble">
                    <div class="typing-dots">
                        <div class="spinner-border spinner-border-sm me-2" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        Processing with AI models...
                    </div>
                </div>
            `;
            chatMessages.appendChild(typingDiv);
        } else {
            // Remove typing indicator
            const typingIndicator = chatMessages.querySelector('.typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
            
            // Add assistant message
            const messageDiv = document.createElement('div');
            messageDiv.className = 'chat-message message-assistant';
            messageDiv.innerHTML = `
                <div class="message-bubble">
                    ${message}
                </div>
            `;
            chatMessages.appendChild(messageDiv);
        }
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    showStatus(message) {
        const statusDisplay = document.getElementById('statusDisplay');
        const statusMessage = document.getElementById('statusMessage');
        if (statusDisplay && statusMessage) {
            statusDisplay.style.display = 'block';
            statusMessage.textContent = message;
        }
    }

    hideStatus() {
        const statusDisplay = document.getElementById('statusDisplay');
        if (statusDisplay) {
            statusDisplay.style.display = 'none';
        }
    }

    updateModelStatus(model, status) {
        const statusMap = {
            'ready': { class: 'model-badge', text: 'Ready' },
            'processing': { class: 'model-badge processing', text: 'Processing...' },
            'complete': { class: 'model-badge complete', text: 'Complete' },
            'error': { class: 'model-badge error', text: 'Error' }
        };

        const statusInfo = statusMap[status] || statusMap['ready'];
        
        if (model === 'gemini-1.5') {
            const badge = document.getElementById('gemini15Status');
            if (badge) {
                badge.className = statusInfo.class;
                badge.textContent = statusInfo.text;
            }
        } else if (model === 'gemini-2.0') {
            const badge = document.getElementById('gemini25Status');
            if (badge) {
                badge.className = statusInfo.class;
                badge.textContent = statusInfo.text;
            }
        }
    }

    showIndividualResponses() {
        const section = document.getElementById('individualResponses');
        if (section) {
            section.style.display = 'block';
        }
    }

    showFinalResponse() {
        const section = document.getElementById('finalResponseSection');
        if (section) {
            section.style.display = 'block';
        }
    }

    displayGeminiResponse(content, model) {
        if (model === '1.5') {
            const element = document.getElementById('gemini15Content');
            if (element) {
                element.textContent = content;
                this.updateModelStatus('gemini-1.5', 'complete');
            }
        } else if (model === '2.0') {
            const element = document.getElementById('gemini25Content');
            if (element) {
                element.textContent = content;
                this.updateModelStatus('gemini-2.0', 'complete');
            }
        }
    }

    appendToFinalResponse(content) {
        const finalResponse = document.getElementById('finalResponse');
        if (finalResponse) {
            finalResponse.textContent += content;
            // Auto-scroll to bottom
            finalResponse.scrollTop = finalResponse.scrollHeight;
        }
    }

    clearFinalResponse() {
        const finalResponse = document.getElementById('finalResponse');
        if (finalResponse) {
            finalResponse.textContent = '';
        }
    }

    resetUI() {
        // Reset model statuses
        this.updateModelStatus('gemini-1.5', 'ready');
        this.updateModelStatus('gemini-2.0', 'ready');
        
        // Clear previous responses
        const gemini15Content = document.getElementById('gemini15Content');
        const gemini25Content = document.getElementById('gemini25Content');
        if (gemini15Content) gemini15Content.textContent = '';
        if (gemini25Content) gemini25Content.textContent = '';
        this.clearFinalResponse();
        
        // Hide sections
        const individualResponses = document.getElementById('individualResponses');
        const finalResponseSection = document.getElementById('finalResponseSection');
        if (individualResponses) individualResponses.style.display = 'none';
        if (finalResponseSection) finalResponseSection.style.display = 'none';
    }

    toggleSolveButton(disabled) {
        const btn = document.getElementById('solveBtn');
        if (!btn) return;
        
        btn.disabled = disabled;
        
        if (disabled) {
            btn.innerHTML = `
                <div class="spinner-border spinner-border-sm me-2" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                Processing...
            `;
        } else {
            btn.innerHTML = `Solve it →`;
        }
    }

    showError(message) {
        this.addAssistantMessage(`<strong>Error:</strong> ${message}`);
    }

    async solveProblem() {
        if (this.isProcessing) return;

        const problemInput = document.getElementById('problemInput');
        if (!problemInput) return;

        const problem = problemInput.value.trim();

        if (!problem) {
            this.showError('Please enter a problem description');
            return;
        }

        this.isProcessing = true;
        this.addUserMessage(problem);
        this.resetUI();
        this.toggleSolveButton(true);

        try {
            // Start streaming
            const response = await fetch('/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ problem: problem })
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server error: ${response.status} - ${errorText}`);
            }

            // Handle streaming response
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            this.handleStreamData(data);
                        } catch (e) {
                            console.error('Failed to parse stream data:', e);
                        }
                    }
                }
            }

        } catch (error) {
            console.error('Error solving problem:', error);
            this.showError(`${error.message}`);
        } finally {
            this.isProcessing = false;
            this.toggleSolveButton(false);
            this.hideStatus();
        }
    }

    handleStreamData(data) {
        switch (data.type) {
            case 'status':
                this.showStatus(data.message);
                
                // Update model status based on message
                if (data.message.includes('Gemini 1.5-flash')) {
                    this.updateModelStatus('gemini-1.5', 'processing');
                } else if (data.message.includes('Gemini 2.0-flash')) {
                    this.updateModelStatus('gemini-2.0', 'processing');
                }
                break;

            case 'gemini_response':
                this.showIndividualResponses();
                this.displayGeminiResponse(data.content, '1.5');
                break;

            case 'openai_response':
                this.displayGeminiResponse(data.content, '2.0');
                break;

            case 'final_start':
                this.hideStatus();
                this.showFinalResponse();
                this.clearFinalResponse();
                break;

            case 'final_chunk':
                this.appendToFinalResponse(data.content);
                break;

            case 'complete':
                this.hideStatus();
                console.log('Problem solving completed');
                break;

            case 'error':
                this.showError(data.message);
                break;

            default:
                console.log('Unknown stream data type:', data.type);
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.femApp = new FemMultiModel();
});
