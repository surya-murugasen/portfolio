// ==========================================
// Portfolio Interactive Scripts
// Author: Surya M
// Description: Accessible navigation, scroll animations,
// case study modals, and clipboard utilities.
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------------------------------
    // 1. Mobile Navigation Toggle with ARIA Accessibility
    // ----------------------------------------------------
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        const toggleMenu = (open) => {
            const isActive = open !== undefined ? open : !hamburger.classList.contains('active');
            hamburger.classList.toggle('active', isActive);
            navLinks.classList.toggle('active', isActive);
            hamburger.setAttribute('aria-expanded', isActive ? 'true' : 'false');
            document.body.style.overflow = isActive ? 'hidden' : '';
        };

        hamburger.addEventListener('click', () => toggleMenu());

        // Close on link click
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => toggleMenu(false));
        });

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && hamburger.classList.contains('active')) {
                toggleMenu(false);
                hamburger.focus();
            }
        });
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
});