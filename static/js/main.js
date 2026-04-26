document.addEventListener('DOMContentLoaded', () => {
    // --- 1. Global Document Loading & Core Logic ---
    const uploadForm = document.getElementById('upload-form-ui');
    const loader = document.getElementById('loader-overlay');
    const fileInput = document.getElementById('file-input');
    const heroTrigger = document.getElementById('hero-upload-trigger');
    const navTrigger = document.getElementById('nav-upload-trigger');
    const dropZone = document.getElementById('drop-zone');

    // Show loader on form submission
    if (uploadForm && loader) {
        uploadForm.addEventListener('submit', () => {
            loader.style.display = 'flex';
        });
    }

    // Generic file dialog opener
    const openFileDialog = () => { if (fileInput) fileInput.click(); };
    if (heroTrigger) heroTrigger.addEventListener('click', openFileDialog);
    if (navTrigger) navTrigger.addEventListener('click', openFileDialog);

    // Handle file selection
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                if (uploadForm) uploadForm.submit();
            }
        });
    }

    // --- 2. Advanced Drag & Drop Interaction ---
    if (dropZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-over'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-over'), false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0 && fileInput) {
                fileInput.files = files;
                if (uploadForm) uploadForm.submit();
            }
        }, false);
    }

    // --- 3. Premium UI Interactions (Scroll & Animations) ---
    
    // Navbar Scroll Effect
    const nav = document.getElementById('main-nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });

    // Reveal Animations using Intersection Observer
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card').forEach(card => {
        revealObserver.observe(card);
    });

    // --- 4. Micro-interactions & Visual Effects ---

    // FIX: Typing Animation for Hero Subtitle (Preserving Spaces)
    const subtitle = document.getElementById('hero-subtitle');
    if (subtitle) {
        const text = subtitle.textContent.trim(); // Use textContent for cleaner extraction
        subtitle.textContent = '';
        let i = 0;
        const type = () => {
            if (i < text.length) {
                subtitle.textContent += text.charAt(i);
                i++;
                // Randomize slightly for natural feel
                setTimeout(type, 10 + Math.random() * 20);
            }
        };
        // Start typing after a short delay for hero entrance
        setTimeout(type, 1000);
    }

    // --- 5. Result Dashboard Logic (Preserved from previous main.js) ---
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    const tabContents = document.querySelectorAll('.tab-content');

    const switchTab = (targetTab) => {
        sidebarLinks.forEach(l => l.classList.remove('active'));
        const activeLink = document.querySelector(`.sidebar-link[data-tab="${targetTab}"]`);
        if (activeLink) activeLink.classList.add('active');

        tabContents.forEach(content => {
            content.classList.toggle('active', content.id === `${targetTab}-tab`);
        });

        if (targetTab === 'clauses') animateConfidenceBars();
    };

    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetTab = link.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });

    const animateConfidenceBars = () => {
        const bars = document.querySelectorAll('.conf-inner');
        bars.forEach(bar => {
            const level = bar.getAttribute('data-confidence') || 0;
            setTimeout(() => { bar.style.width = `${level}%`; }, 100);
        });
    };

    // --- AI ASSISTANT V2 LOGIC (Cache Busting) ---
    const aiToggle = document.getElementById('ai-toggle-v2');
    const aiWindow = document.getElementById('ai-window-v2');
    const aiClose = document.getElementById('ai-close-v2');
    const aiInput = document.getElementById('ai-input-v2');
    const aiSend = document.getElementById('ai-send-v2');
    const aiMessages = document.getElementById('ai-messages-v2');

    if(aiToggle && aiWindow) {
        aiToggle.addEventListener('click', () => {
            aiWindow.classList.toggle('active');
        });
    }

    if(aiClose && aiWindow) {
        aiClose.addEventListener('click', () => {
            aiWindow.classList.remove('active');
        });
    }

    function addAiMessage(text, isBot = false) {
        if(!aiMessages) return;
        const msgDiv = document.createElement('div');
        msgDiv.className = `ai-v2-msg ${isBot ? 'ai-v2-bot' : 'ai-v2-user'}`;
        msgDiv.textContent = text;
        aiMessages.appendChild(msgDiv);
        aiMessages.scrollTop = aiMessages.scrollHeight;
    }

    async function handleAiChat(forcedMsg = null) {
        const message = forcedMsg || aiInput.value.trim();
        if(!message) return;

        addAiMessage(message, false);
        aiInput.value = '';

        const typingId = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'ai-v2-msg ai-v2-bot';
        typingDiv.id = typingId;
        typingDiv.textContent = 'Analyzing...';
        aiMessages.appendChild(typingDiv);
        aiMessages.scrollTop = aiMessages.scrollHeight;

        try {
            const docText = document.getElementById('doc-text-payload')?.textContent || "";
            const summaryText = document.getElementById('summary-text-payload')?.textContent || "";

            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    question: message,
                    document_text: docText,
                    summary_text: summaryText
                })
            });
            const data = await response.json();
            
            const tipEl = document.getElementById(typingId);
            if(tipEl) tipEl.remove();
            addAiMessage(data.answer || data.response || "No response found.", true);
        } catch (error) {
            const tipEl = document.getElementById(typingId);
            if(tipEl) tipEl.remove();
            addAiMessage("Connection error. Please try again.", true);
        }
    }

    document.querySelectorAll('.ai-v2-suggest-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            handleAiChat(btn.getAttribute('data-q'));
        });
    });

    if(aiSend) aiSend.addEventListener('click', () => handleAiChat());
    if(aiInput) aiInput.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') handleAiChat();
    });

    // Handle suggested questions
    document.querySelectorAll('.suggest-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            handleChat(btn.getAttribute('data-q'));
        });
    });

    if(chatSend) {
        chatSend.addEventListener('click', () => handleChat());
    }
    if(chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if(e.key === 'Enter') handleChat();
        });
    }
});
