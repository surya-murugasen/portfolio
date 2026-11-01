// ==========================================
// Portfolio Interactive Scripts
// Author: Surya M
// Description: Accessible navigation, scroll animations,
// case study modals, and clipboard utilities.
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------------------------------
    // 00. Skeleton Loader Controller (Zero-Lag & Fail-Safe)
    // ----------------------------------------------------
    const skeletonLoader = document.getElementById('skeleton-loader');

    const dismissSkeleton = () => {
        if (!skeletonLoader || skeletonLoader.classList.contains('skeleton-fade-out')) return;
        skeletonLoader.classList.add('skeleton-fade-out');
        setTimeout(() => {
            skeletonLoader.style.display = 'none';
            skeletonLoader.setAttribute('aria-hidden', 'true');
            skeletonLoader.setAttribute('aria-busy', 'false');
        }, 450);
    };

    // Global method to test or preview the skeleton loader
    window.showSkeletonLoader = (duration = 2000) => {
        if (!skeletonLoader) return;
        skeletonLoader.style.display = 'block';
        skeletonLoader.setAttribute('aria-hidden', 'false');
        skeletonLoader.setAttribute('aria-busy', 'true');
        void skeletonLoader.offsetWidth; // Force browser reflow
        skeletonLoader.classList.remove('skeleton-fade-out');
        if (duration > 0) {
            setTimeout(dismissSkeleton, duration);
        }
    };

    // Real loading behavior & zero-delay fail-safe:
    // Dismiss as soon as DOM and critical assets are ready; never wait on slow external CDNs.
    const prefersReducedMotionInitial = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotionInitial) {
        dismissSkeleton();
    } else {
        const profileImg = document.querySelector('.profile-img');

        const triggerDismissal = () => {
            dismissSkeleton();
        };

        if (profileImg && !profileImg.complete) {
            // Wait for real image asset to load or error
            profileImg.addEventListener('load', triggerDismissal, { once: true });
            profileImg.addEventListener('error', triggerDismissal, { once: true });
        } else {
            // Image is already decoded/cached: brief micro-delay (~120ms) prevents harsh 1-frame strobe
            setTimeout(triggerDismissal, 120);
        }

        // Hard fail-safe: Content is never blocked longer than 800ms under any network condition
        setTimeout(dismissSkeleton, 800);
    }

    // ----------------------------------------------------
    // 0. Dark Mode & Light Mode Theme Controller
    // ----------------------------------------------------
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const themeToggleIcon = document.getElementById('theme-toggle-icon');
    const themeToggleMobile = document.getElementById('theme-toggle-mobile');
    const mobileThemeIcon = document.getElementById('mobile-theme-icon');
    const mobileThemeText = document.getElementById('mobile-theme-text');
    const mobileSwitchIcon = document.getElementById('mobile-switch-icon');

    const updateThemeUI = (theme) => {
        const isDark = theme === 'dark';
        if (themeToggleIcon) {
            themeToggleIcon.className = isDark ? 'fa-solid fa-moon' : 'fa-solid fa-sun text-amber-500';
        }
        if (themeToggleBtn) {
            themeToggleBtn.setAttribute('title', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
            themeToggleBtn.setAttribute('aria-label', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
        }
        if (mobileThemeIcon) {
            mobileThemeIcon.className = isDark ? 'fa-solid fa-moon text-accent' : 'fa-solid fa-sun text-amber-500';
        }
        if (mobileThemeText) {
            mobileThemeText.textContent = isDark ? 'Dark Mode' : 'Light Mode';
        }
        if (mobileSwitchIcon) {
            mobileSwitchIcon.className = isDark ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
        }
    };

    const applyTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
            document.documentElement.classList.remove('light');
        } else {
            document.documentElement.classList.add('light');
            document.documentElement.classList.remove('dark');
        }
        try {
            localStorage.setItem('portfolio-theme', theme);
        } catch (e) {}
        updateThemeUI(theme);
    };

    const currentTheme = document.documentElement.getAttribute('data-theme') ||
        localStorage.getItem('portfolio-theme') ||
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

    applyTheme(currentTheme);

    const toggleTheme = () => {
        const activeTheme = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
        applyTheme(activeTheme);
    };

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', toggleTheme);
    }
    if (themeToggleMobile) {
        themeToggleMobile.addEventListener('click', toggleTheme);
    }

    // Listen for OS theme preference changes if user has not explicitly chosen
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('portfolio-theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });

    // ----------------------------------------------------
    // 1. Mobile Navigation Drawer & Backdrop Controller
    // ----------------------------------------------------
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const mobileCloseBtn = document.getElementById('mobile-close-btn');
    const mobileBackdrop = document.getElementById('mobile-backdrop');

    if (navLinks) {
        const toggleMenu = (open) => {
            const isActive = open !== undefined ? open : !navLinks.classList.contains('active');
            if (hamburger) {
                hamburger.classList.toggle('active', isActive);
                hamburger.setAttribute('aria-expanded', isActive ? 'true' : 'false');
            }
            navLinks.classList.toggle('active', isActive);
            if (mobileBackdrop) {
                mobileBackdrop.classList.toggle('active', isActive);
            }
            document.body.style.overflow = isActive ? 'hidden' : '';
        };

        if (hamburger) {
            hamburger.addEventListener('click', () => toggleMenu());
        }
        if (mobileCloseBtn) {
            mobileCloseBtn.addEventListener('click', () => toggleMenu(false));
        }
        if (mobileBackdrop) {
            mobileBackdrop.addEventListener('click', () => toggleMenu(false));
        }

        // Close on link click
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => toggleMenu(false));
        });

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navLinks.classList.contains('active')) {
                toggleMenu(false);
                if (hamburger) hamburger.focus();
            }
        });
    }

    // ----------------------------------------------------
    // 1b. Scroll Progress Bar & Back to Top Controller
    // ----------------------------------------------------
    const scrollProgressBar = document.getElementById('scroll-progress-bar');
    const backToTopBtn = document.getElementById('back-to-top');
    const navbar = document.querySelector('.navbar');

    const handleScrollUpdates = () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        
        // Update Scroll Progress
        if (scrollProgressBar && docHeight > 0) {
            const scrollPercent = Math.min(100, Math.max(0, (scrollTop / docHeight) * 100));
            scrollProgressBar.style.width = `${scrollPercent}%`;
        }

        // Update Back to Top visibility
        if (backToTopBtn) {
            if (scrollTop > 350) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        }

        // Update Navbar Scrolled Style
        if (navbar) {
            if (scrollTop > 20) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    };

    window.addEventListener('scroll', handleScrollUpdates, { passive: true });
    handleScrollUpdates();

    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ----------------------------------------------------
    // 1c. Active Section Highlighting (Scrollspy)
    // ----------------------------------------------------
    const sections = document.querySelectorAll('section[id], footer[id]');
    const navItems = document.querySelectorAll('.nav-links a[href^="#"]');

    if (sections.length && navItems.length && 'IntersectionObserver' in window) {
        const spyObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const currentId = entry.target.getAttribute('id');
                    navItems.forEach(link => {
                        const href = link.getAttribute('href').replace('#', '');
                        if (href === currentId) {
                            link.classList.add('active');
                        } else {
                            link.classList.remove('active');
                        }
                    });
                }
            });
        }, {
            threshold: 0.25,
            rootMargin: '-80px 0px -50% 0px'
        });

        sections.forEach(section => spyObserver.observe(section));
    }

    // ----------------------------------------------------
    // 2. Intersection Observer for Scroll Animations
    // ----------------------------------------------------
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const faders = document.querySelectorAll('.fade-in, .observe-me');

    if (prefersReducedMotion) {
        // Immediately reveal all elements without transitions
        faders.forEach(el => el.classList.add('appear'));
    } else {
        const appearOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -40px 0px'
        };

        const appearOnScroll = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('appear');
                    if (entry.target.classList.contains('observe-me')) {
                        entry.target.classList.add('fade-in');
                        setTimeout(() => {
                            entry.target.classList.add('appear');
                        }, 20);
                    }
                    observer.unobserve(entry.target);
                }
            });
        }, appearOptions);

        faders.forEach(fader => appearOnScroll.observe(fader));

        // Initial viewport check
        setTimeout(() => {
            document.querySelectorAll('.fade-in').forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.top < window.innerHeight) {
                    el.classList.add('appear');
                }
            });
        }, 100);
    }

    // ----------------------------------------------------
    // 3. Technical Case Study Modals (Keyboard & A11y Friendly)
    // ----------------------------------------------------
    const modalTriggers = document.querySelectorAll('[data-case-study-target]');
    const closeButtons = document.querySelectorAll('[data-close-modal]');
    let lastActiveElement = null;

    const openCaseStudy = (modalId) => {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        lastActiveElement = document.activeElement;
        modal.classList.remove('hidden');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';

        const focusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (focusable) focusable.focus();
    };

    const closeCaseStudy = (modal) => {
        if (!modal) return;
        modal.classList.add('hidden');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
        if (lastActiveElement && typeof lastActiveElement.focus === 'function') {
            lastActiveElement.focus();
        }
    };

    modalTriggers.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = button.getAttribute('data-case-study-target');
            openCaseStudy(targetId);
        });
    });

    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = button.closest('.case-study-modal');
            closeCaseStudy(modal);
        });
    });

    // Close on backdrop click
    document.querySelectorAll('.case-study-modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeCaseStudy(modal);
            }
        });
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.case-study-modal:not(.hidden)');
            if (openModal) {
                closeCaseStudy(openModal);
            }
        }
    });

    // ----------------------------------------------------
    // 4. One-Click Email Copy Utility with Visual Feedback
    // ----------------------------------------------------
    const copyEmailBtn = document.getElementById('copy-email-btn');
    const copyEmailText = document.getElementById('copy-email-text');
    const emailToCopy = 'suryamurugasen135@gmail.com';

    if (copyEmailBtn) {
        copyEmailBtn.addEventListener('click', async () => {
            try {
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    await navigator.clipboard.writeText(emailToCopy);
                } else {
                    // Fallback for older browser security contexts
                    const tempInput = document.createElement('input');
                    tempInput.value = emailToCopy;
                    document.body.appendChild(tempInput);
                    tempInput.select();
                    document.execCommand('copy');
                    document.body.removeChild(tempInput);
                }

                if (copyEmailText) {
                    const originalText = copyEmailText.textContent;
                    copyEmailText.textContent = 'Copied to Clipboard!';
                    copyEmailBtn.classList.add('bg-emerald-600', 'text-white');
                    setTimeout(() => {
                        copyEmailText.textContent = originalText;
                        copyEmailBtn.classList.remove('bg-emerald-600', 'text-white');
                    }, 2500);
                }
            } catch (err) {
                console.error('Failed to copy email:', err);
            }
        });
    }

    // ----------------------------------------------------
    // 5. AI Portfolio Assistant Controller
    // ----------------------------------------------------
    const aiToggleBtn = document.getElementById('ai-assistant-toggle');
    const aiPanel = document.getElementById('ai-assistant-panel');
    const aiCloseBtn = document.getElementById('ai-close-btn');
    const aiClearBtn = document.getElementById('ai-clear-btn');
    const aiMessages = document.getElementById('ai-messages');
    const aiForm = document.getElementById('ai-form');
    const aiInput = document.getElementById('ai-input');
    const aiCharCount = document.getElementById('ai-char-count');
    const aiStatusIndicator = document.getElementById('ai-status-indicator');

    // Default API base: prioritize window global, meta tag, or local dev fallback
    const metaApiBase = document.querySelector('meta[name="ai-api-base"]')?.getAttribute('content')?.trim();
    const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    const AI_API_BASE = window.AI_API_BASE || (metaApiBase && metaApiBase !== '__AI_API_BASE__' ? metaApiBase : null) || (isLocalhost ? 'http://localhost:8000' : '');
    let conversationHistory = [];
    let isAwaitingResponse = false;

    // Sanitize user text against XSS before DOM insertion
    const escapeHTML = (str) => {
        const div = document.createElement('div');
        div.innerText = str;
        return div.innerHTML;
    };

    // Lightweight markdown formatter for assistant responses
    const formatMarkdown = (text) => {
        let formatted = escapeHTML(text);
        // Bold: **text**
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong class="text-white">$1</strong>');
        // Code: `code`
        formatted = formatted.replace(/`([^`]+)`/g, '<code class="px-1 py-0.5 rounded bg-black/40 text-accent font-mono text-xs">$1</code>');
        // Markdown Links: [label](url)
        formatted = formatted.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-accent underline hover:text-white">$1</a>');
        // Bullet points: lines starting with • or *
        formatted = formatted.replace(/^[•*]\s+(.*)$/gm, '<li class="ml-4 list-disc">$1</li>');
        // Newlines
        formatted = formatted.replace(/\n\n/g, '<br><br>').replace(/\n/g, '<br>');
        return formatted;
    };

    const toggleAiPanel = (open) => {
        if (!aiPanel) return;
        const shouldOpen = open !== undefined ? open : aiPanel.classList.contains('hidden');
        aiPanel.classList.toggle('hidden', !shouldOpen);
        aiPanel.setAttribute('aria-hidden', shouldOpen ? 'false' : 'true');
        if (aiToggleBtn) {
            aiToggleBtn.setAttribute('aria-expanded', shouldOpen ? 'true' : 'false');
        }
        if (shouldOpen) {
            setTimeout(() => aiInput && aiInput.focus(), 150);
        } else if (aiToggleBtn) {
            aiToggleBtn.focus();
        }
    };

    if (aiToggleBtn) {
        aiToggleBtn.addEventListener('click', () => toggleAiPanel());
    }
    if (aiCloseBtn) {
        aiCloseBtn.addEventListener('click', () => toggleAiPanel(false));
    }

    // Escape key closes panel
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && aiPanel && !aiPanel.classList.contains('hidden')) {
            toggleAiPanel(false);
        }
    });

    // Character counter
    if (aiInput && aiCharCount) {
        aiInput.addEventListener('input', () => {
            const len = aiInput.value.length;
            aiCharCount.textContent = `${len}/500`;
            aiCharCount.classList.toggle('text-amber-400', len > 450);
        });
    }

    // Scroll chat to bottom
    const scrollToBottom = () => {
        if (aiMessages) {
            aiMessages.scrollTop = aiMessages.scrollHeight;
        }
    };

    // Render User Bubble
    const appendUserMessage = (text) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'ai-msg ai-msg-user flex justify-end text-left';
        msgDiv.innerHTML = `
            <div class="bg-gradient-to-r from-accent to-indigo-600 text-white p-3 rounded-2xl rounded-tr-sm text-sm max-w-[85%] shadow-md">
                ${escapeHTML(text)}
            </div>
        `;
        aiMessages.appendChild(msgDiv);
        scrollToBottom();
    };

    // Render Loading Indicator
    const showLoadingIndicator = () => {
        const loadDiv = document.createElement('div');
        loadDiv.id = 'ai-loading-bubble';
        loadDiv.className = 'ai-msg ai-msg-bot flex gap-2.5 text-left items-center';
        loadDiv.innerHTML = `
            <div class="w-7 h-7 rounded-lg bg-accent/20 border border-accent/40 flex-shrink-0 flex items-center justify-center text-accent text-xs">
                <i class="fa-solid fa-robot"></i>
            </div>
            <div class="bg-slate-800/90 border border-white/10 px-3.5 py-2.5 rounded-2xl rounded-tl-sm flex items-center gap-1.5 shadow-md">
                <span class="ai-typing-dot"></span>
                <span class="ai-typing-dot"></span>
                <span class="ai-typing-dot"></span>
            </div>
        `;
        aiMessages.appendChild(loadDiv);
        scrollToBottom();
    };

    const removeLoadingIndicator = () => {
        const loader = document.getElementById('ai-loading-bubble');
        if (loader) loader.remove();
    };

    // Render Assistant Message with Optional Actions
    const appendBotMessage = (text, actions = null, isError = false) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'ai-msg ai-msg-bot flex gap-2.5 text-left';

        let actionsHTML = '';
        if (actions && Array.isArray(actions) && actions.length > 0) {
            const buttons = actions.map(act => {
                if (act.type === 'case_study') {
                    return `<button type="button" class="ai-action-btn text-xs px-2.5 py-1 rounded-full bg-accent/20 hover:bg-accent hover:text-white border border-accent/40 text-accent transition-colors font-medium flex items-center gap-1.5" data-action="case_study" data-target="${act.target}"><i class="fa-solid fa-file-lines text-[10px]"></i> ${act.label}</button>`;
                } else if (act.type === 'repo' || act.type === 'link') {
                    return `<a href="${act.url}" target="_blank" rel="noopener noreferrer" class="ai-action-btn text-xs px-2.5 py-1 rounded-full bg-white/5 hover:bg-white/15 border border-white/15 text-slate-200 transition-colors font-medium flex items-center gap-1.5"><i class="fa-brands fa-github text-[11px]"></i> ${act.label}</a>`;
                } else if (act.type === 'scroll') {
                    return `<a href="${act.target}" class="ai-action-btn text-xs px-2.5 py-1 rounded-full bg-indigo-500/20 hover:bg-indigo-500 hover:text-white border border-indigo-500/40 text-indigo-300 transition-colors font-medium flex items-center gap-1.5"><i class="fa-solid fa-arrow-down text-[10px]"></i> ${act.label}</a>`;
                }
                return '';
            }).join('');
            actionsHTML = `<div class="mt-2.5 pt-2.5 border-t border-white/10 flex flex-wrap gap-1.5">${buttons}</div>`;
        }

        const borderClass = isError ? 'border-rose-500/40 bg-rose-950/30' : 'border-white/10 bg-slate-800/90';

        msgDiv.innerHTML = `
            <div class="w-7 h-7 rounded-lg bg-accent/20 border border-accent/40 flex-shrink-0 flex items-center justify-center text-accent text-xs">
                <i class="fa-solid fa-robot"></i>
            </div>
            <div class="${borderClass} border p-3.5 rounded-2xl rounded-tl-sm text-slate-200 leading-relaxed max-w-[85%] shadow-md">
                <div class="text-xs sm:text-sm">${formatMarkdown(text)}</div>
                ${actionsHTML}
            </div>
        `;

        aiMessages.appendChild(msgDiv);

        // Bind case study action buttons inside assistant bubble
        msgDiv.querySelectorAll('[data-action="case_study"]').forEach(btn => {
            btn.addEventListener('click', () => {
                const targetModal = btn.getAttribute('data-target');
                if (targetModal) {
                    openCaseStudy(targetModal);
                }
            });
        });

        scrollToBottom();
    };

    // Send Query to AI Backend
    const sendQuery = async (queryText) => {
        if (!queryText || isAwaitingResponse) return;

        appendUserMessage(queryText);
        showLoadingIndicator();
        isAwaitingResponse = true;

        if (!AI_API_BASE) {
            removeLoadingIndicator();
            appendBotMessage(
                `ℹ️ **Service Notice:** The live AI Assistant cloud service endpoint is not configured for this domain yet.\n\n` +
                `• Explore the verified technical architecture in the **Technical Case Studies** above.\n` +
                `• Contact Surya directly for engineering opportunities: [suryamurugasen135@gmail.com](mailto:suryamurugasen135@gmail.com).`,
                null,
                false
            );
            isAwaitingResponse = false;
            return;
        }

        try {
            const res = await fetch(`${AI_API_BASE}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: queryText,
                    history: conversationHistory
                })
            });

            removeLoadingIndicator();

            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                const errMsg = errData.detail || `Server error (${res.status}).`;
                appendBotMessage(`⚠️ **Assistant Error:** ${errMsg}`, null, true);
                return;
            }

            const data = await res.json();
            conversationHistory.push({ role: 'user', content: queryText });
            conversationHistory.push({ role: 'assistant', content: data.reply });

            appendBotMessage(data.reply, data.suggested_actions);

        } catch (netErr) {
            removeLoadingIndicator();
            appendBotMessage(
                `⚠️ **Connection Notice:** Unable to reach the AI Assistant backend service at \`${AI_API_BASE}\`.\n\n` +
                `• **Local Dev:** Run \`python ai-service/main.py\` in terminal.\n` +
                `• **Direct Inquiries:** Contact Surya at [suryamurugasen135@gmail.com](mailto:suryamurugasen135@gmail.com).`,
                null,
                true
            );
        } finally {
            isAwaitingResponse = false;
        }
    };

    // Form submission
    if (aiForm && aiInput) {
        aiForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const text = aiInput.value.trim();
            if (text) {
                aiInput.value = '';
                if (aiCharCount) aiCharCount.textContent = '0/500';
                sendQuery(text);
            }
        });
    }

    // Reset Chat Button
    if (aiClearBtn) {
        aiClearBtn.addEventListener('click', () => {
            conversationHistory = [];
            if (aiMessages) {
                aiMessages.innerHTML = `
                    <div class="ai-msg ai-msg-bot flex gap-3 text-left">
                        <div class="w-7 h-7 rounded-lg bg-accent/20 border border-accent/40 flex-shrink-0 flex items-center justify-center text-accent text-xs">
                            <i class="fa-solid fa-robot"></i>
                        </div>
                        <div class="bg-slate-800/90 border border-white/10 p-3.5 rounded-2xl rounded-tl-sm text-slate-200 leading-relaxed max-w-[85%] shadow-md">
                            <p class="text-xs text-slate-400 mb-1 font-mono uppercase tracking-wider">Conversation Cleared</p>
                            <p>Hi! How can I help you explore Surya's technical projects, stack, or experience?</p>
                        </div>
                    </div>
                `;
            }
        });
    }

    // Bind initial suggestion chip clicks
    document.querySelectorAll('.ai-suggest-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const prompt = btn.getAttribute('data-prompt');
            if (prompt) {
                sendQuery(prompt);
            }
        });
    });
});