// ==================== Global Variables ====================
let educationModules = [];
let thesisData = {};
let courseworks = [];
let practicalWorks = [];

// ==================== Initialize ====================
document.addEventListener('DOMContentLoaded', async function () {
    // Initialize AOS
    AOS.init({
        duration: 800,
        once: true,
        offset: 100
    });

    // Initialize Particles.js
    if (document.getElementById('particles-js')) {
        particlesJS('particles-js', {
            particles: {
                number: {
                    value: 80,
                    density: {
                        enable: true,
                        value_area: 800
                    }
                },
                color: {
                    value: '#3b82f6'
                },
                shape: {
                    type: 'circle'
                },
                opacity: {
                    value: 0.5,
                    random: false
                },
                size: {
                    value: 3,
                    random: true
                },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: '#3b82f6',
                    opacity: 0.2,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 2,
                    direction: 'none',
                    random: false,
                    straight: false,
                    out_mode: 'out',
                    bounce: false
                }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: {
                        enable: true,
                        mode: 'grab'
                    },
                    onclick: {
                        enable: true,
                        mode: 'push'
                    },
                    resize: true
                },
                modes: {
                    grab: {
                        distance: 140,
                        line_linked: {
                            opacity: 0.5
                        }
                    },
                    push: {
                        particles_nb: 4
                    }
                }
            },
            retina_detect: true
        });
    }

    // Hide preloader
    setTimeout(() => {
        const preloader = document.getElementById('preloader');
        if (preloader) {
            preloader.classList.add('hidden');
        }
    }, 1000);

    // Load data from JSON files
    await loadAllData();

    // Initialize navigation
    initNavigation();

    // Initialize scroll animations
    initScrollAnimations();

    // Initialize counter animation
    initCounters();

    // Initialize back to top button
    initBackToTop();
});

// ==================== Load Data ====================
async function loadAllData() {
    try {
        // Load education modules
        const modulesResponse = await fetch('public/data/education_modules.json');
        if (modulesResponse.ok) {
            educationModules = await modulesResponse.json();
            renderEducationModules();
        }

        // Load thesis
        const thesisResponse = await fetch('public/data/thesis.json');
        if (thesisResponse.ok) {
            thesisData = await thesisResponse.json();
            renderThesis();
        }

        // Load courseworks
        const courseworksResponse = await fetch('public/data/courseworks.json');
        if (courseworksResponse.ok) {
            courseworks = await courseworksResponse.json();
            renderCourseworks();
        }

        // Load practical works
        const practicalResponse = await fetch('public/data/practical_works.json');
        if (practicalResponse.ok) {
            practicalWorks = await practicalResponse.json();
            renderPracticalWorks();
        }
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// ==================== Render Functions ====================
function renderEducationModules() {
    const container = document.getElementById('educationModules');
    if (!container || !educationModules.length) return;

    container.innerHTML = educationModules.map((module, index) => `
        <div class="module-card" data-aos="fade-up" data-aos-delay="${index * 100}">
            <div class="module-header" onclick="toggleModule(${index})">
                <div class="module-title">
                    <span>📚 ${module.title}</span>
                    <span class="module-toggle">
                        <i class="fas fa-chevron-down" id="module-icon-${index}"></i>
                    </span>
                </div>
            </div>
            <div class="module-content" id="module-content-${index}" style="display: none;">
                ${module.semesters.map(semester => `
                    <div class="semester-section">
                        <div class="semester-title">
                            <i class="fas fa-calendar-alt"></i>
                            ${semester.title}
                        </div>
                        <div class="labs-list">
                            ${semester.labs.map(lab => `
                                <div class="lab-item">
                                    <a href="${lab.link}" target="_blank">
                                        <i class="fas fa-flask"></i>
                                        ${lab.title}
                                    </a>
                                    <i class="fas fa-external-link-alt"></i>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
}

function renderThesis() {
    const container = document.getElementById('thesisContent');
    if (!container || !thesisData.title) return;

    container.innerHTML = `
        <div class="thesis-card" data-aos="fade-up">
            <div class="thesis-info">
                <h3>${thesisData.title}</h3>
                <p class="thesis-topic">
                    <i class="fas fa-graduation-cap"></i>
                    ${thesisData.topic}
                </p>
                <p class="thesis-description">${thesisData.description}</p>
                <div class="thesis-features">
                    <h4>Основные разделы:</h4>
                    <ul>
                        ${thesisData.keyFeatures.map(feature => `
                            <li>
                                <i class="fas fa-check-circle"></i>
                                ${feature}
                            </li>
                        `).join('')}
                    </ul>
                </div>
                <a href="${thesisData.link}" class="thesis-link" target="_blank">
                    <i class="fas fa-file-alt"></i>
                    Открыть работу
                </a>
            </div>
        </div>
    `;
}

function renderCourseworks() {
    const container = document.getElementById('courseworksList');
    if (!container || !courseworks.length) return;

    container.innerHTML = courseworks.map((work, index) => `
        <div class="work-card" data-aos="fade-up" data-aos-delay="${index * 100}">
            <div class="work-header">
                <h3 class="work-title">${work.title}</h3>
                <span class="work-semester">
                    <i class="fas fa-calendar"></i>
                    ${work.semester}
                </span>
            </div>
            <p class="work-description">${work.description}</p>
            <div class="work-technologies">
                <strong>Технологии:</strong>
                <div class="tech-tags">
                    ${work.technologies.map(tech => `
                        <span class="tech-tag">${tech}</span>
                    `).join('')}
                </div>
            </div>
            <a href="${work.link}" class="work-link" target="_blank">
                Подробнее
                <i class="fas fa-arrow-right"></i>
            </a>
        </div>
    `).join('');
}

function renderPracticalWorks() {
    const container = document.getElementById('practicalsList');
    if (!container || !practicalWorks.length) return;

    container.innerHTML = practicalWorks.map((work, index) => `
        <div class="work-card" data-aos="fade-up" data-aos-delay="${index * 100}">
            <div class="work-header">
                <h3 class="work-title">${work.title}</h3>
                <span class="work-semester">
                    <i class="fas fa-calendar"></i>
                    ${work.semester}
                </span>
            </div>
            <p class="work-description">${work.description}</p>
            <div class="work-items">
                <strong>Работы:</strong>
                <div class="items-list">
                    ${work.items.map(item => `
                        <div class="item-entry">
                            <i class="fas fa-code"></i>
                            ${item}
                        </div>
                    `).join('')}
                </div>
            </div>
            <a href="${work.link}" class="work-link" target="_blank">
                Открыть все работы
                <i class="fas fa-arrow-right"></i>
            </a>
        </div>
    `).join('');
}

// ==================== Navigation ====================
function initNavigation() {
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Mobile menu toggle
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // Close mobile menu on link click
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Update active nav link
        updateActiveNavLink();
    });
}

function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            if (navLink) navLink.classList.add('active');
        }
    });
}

// ==================== Toggle Module ====================
function toggleModule(index) {
    const content = document.getElementById(`module-content-${index}`);
    const icon = document.getElementById(`module-icon-${index}`);

    if (content && icon) {
        if (content.style.display === 'none') {
            content.style.display = 'block';
            icon.style.transform = 'rotate(180deg)';
        } else {
            content.style.display = 'none';
            icon.style.transform = 'rotate(0deg)';
        }
    }
}

// ==================== Scroll Animations ====================
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// ==================== Counter Animation ====================
function initCounters() {
    const counters = document.querySelectorAll('.stat-number');
    const speed = 200;

    const animateCounter = (counter) => {
        const target = +counter.getAttribute('data-count');
        const increment = target / speed;

        const updateCount = () => {
            const count = +counter.innerText;
            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(updateCount, 1);
            } else {
                counter.innerText = target;
            }
        };
        updateCount();
    };

    const observerOptions = {
        threshold: 1,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    counters.forEach(counter => {
        observer.observe(counter);
    });
}

// ==================== Back to Top ====================
function initBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');

    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });

        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// ==================== Smooth Scroll ====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});