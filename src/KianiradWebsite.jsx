import { useEffect, useMemo, useState } from 'react'

const navLinks = [
  { id: 'home', label: 'Home' },
  { id: 'services', label: 'Services' },
  { id: 'projects', label: 'Projects' },
  { id: 'about', label: 'About' },
  { id: 'contact', label: 'Contact' },
]

const services = [
  {
    title: 'AI Automation Systems',
    description:
      'Design and deploy workflow automations that remove repetitive tasks and save teams hours every week.',
  },
  {
    title: 'Backend Development',
    description:
      'Build secure Python/Django backends with clear architecture, reliable APIs, and room to scale.',
  },
  {
    title: 'Telegram Bots',
    description:
      'Launch bot experiences for support, sales, and operations with real-time integrations.',
  },
  {
    title: 'SaaS Applications',
    description:
      'Ship focused SaaS products quickly with maintainable code, auth, billing, and analytics-ready data.',
  },
  {
    title: 'API Integrations',
    description:
      'Connect your stack with CRMs, payment gateways, AI services, and internal tools without fragile glue code.',
  },
]

const projects = [
  {
    title: 'LeadFlow AI Assistant',
    category: 'AI',
    problem: 'Sales teams manually qualified inbound leads and lost response time.',
    solution: 'Built an AI triage pipeline with scoring, enrichment, and instant routing.',
    result: 'Cut first-response time by 72% and increased qualified calls by 38%.',
    stack: ['Python', 'Django', 'OpenAI API', 'PostgreSQL'],
  },
  {
    title: 'OpsPulse Automation Hub',
    category: 'Backend',
    problem: 'Operations workflows were spread across spreadsheets and email threads.',
    solution: 'Created a backend orchestration platform with rule-based automations.',
    result: 'Reduced manual operations workload by 40% in the first quarter.',
    stack: ['Django', 'Celery', 'Redis', 'REST API'],
  },
  {
    title: 'SaaS Billing Engine',
    category: 'SaaS',
    problem: 'A startup needed reliable subscription management before launch.',
    solution: 'Delivered billing services, plans, webhooks, and invoice automation.',
    result: 'Enabled launch on time with near-zero billing support tickets.',
    stack: ['Python', 'Stripe API', 'Docker', 'React'],
  },
  {
    title: 'SupportBot for Telegram',
    category: 'Bots',
    problem: 'Customer support inquiries arrived 24/7 with delayed handling.',
    solution: 'Implemented a Telegram bot with intent routing and ticket creation.',
    result: 'Automated 61% of repetitive tickets and improved CSAT turnaround.',
    stack: ['Python', 'Telegram API', 'FastAPI', 'Webhook Workers'],
  },
]

const metrics = [
  { label: 'Automations Shipped', value: '35+' },
  { label: 'Avg. Time Saved', value: '18 hrs/week' },
  { label: 'Delivery Reliability', value: '99.9%' },
]

const tags = ['All', 'AI', 'Backend', 'SaaS', 'Bots']

export default function KianiradWebsite() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [activeSection, setActiveSection] = useState('home')
  const [filter, setFilter] = useState('All')
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'dark')
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id)
          }
        })
      },
      { threshold: 0.4 },
    )

    navLinks.forEach(({ id }) => {
      const section = document.getElementById(id)
      if (section) observer.observe(section)
    })

    return () => observer.disconnect()
  }, [])

  useEffect(() => {
    document.body.style.overflow = menuOpen ? 'hidden' : 'auto'
  }, [menuOpen])

  const filteredProjects = useMemo(() => {
    if (filter === 'All') return projects
    return projects.filter((project) => project.category === filter)
  }, [filter])

  return (
    <div className="site-shell">
      <header className={`site-header ${scrolled ? 'site-header--scrolled' : ''}`}>
        <div className="container nav-wrap">
          <a href="#home" className="brand">
            Kianirad
          </a>

          <nav className="desktop-nav" aria-label="Primary navigation">
            {navLinks.map((link) => (
              <a
                key={link.id}
                href={`#${link.id}`}
                className={activeSection === link.id ? 'is-active' : ''}
              >
                {link.label}
              </a>
            ))}
          </nav>

          <div className="nav-actions">
            <button
              type="button"
              className="theme-toggle"
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              aria-label="Toggle color theme"
            >
              {theme === 'dark' ? '☀️' : '🌙'}
            </button>
            <a href="#contact" className="btn btn-primary nav-cta">
              Start Project
            </a>
            <button
              type="button"
              className="menu-toggle"
              onClick={() => setMenuOpen(!menuOpen)}
              aria-expanded={menuOpen}
              aria-controls="mobile-menu"
            >
              {menuOpen ? 'Close' : 'Menu'}
            </button>
          </div>
        </div>

        {menuOpen && (
          <nav id="mobile-menu" className="mobile-menu" aria-label="Mobile navigation">
            {navLinks.map((link) => (
              <a key={link.id} href={`#${link.id}`} onClick={() => setMenuOpen(false)}>
                {link.label}
              </a>
            ))}
            <a href="#contact" className="btn btn-primary" onClick={() => setMenuOpen(false)}>
              Start Project
            </a>
          </nav>
        )}
      </header>

      <main>
        <section id="home" className="hero">
          <div className="hero-bg" aria-hidden="true" />
          <div className="container hero-grid">
            <div>
              <p className="eyebrow">AI Systems Architect · Backend Developer · Automation Builder</p>
              <h1>Building AI-powered systems that automate your business</h1>
              <p className="lead">
                I help startups and businesses reduce manual work and scale using backend systems,
                automation, and AI integrations.
              </p>
              <div className="hero-cta-row">
                <a href="#contact" className="btn btn-primary">
                  Book a Free Consultation
                </a>
                <a href="#projects" className="btn btn-secondary">
                  View Projects
                </a>
              </div>
              <p className="trust-line">Trusted by founders to ship reliable automation and revenue-ready systems.</p>
            </div>
            <div className="hero-panel" role="img" aria-label="Live system outcomes summary">
              <p className="panel-title">Current delivery focus</p>
              <ul>
                <li>AI workflows connected to real business KPIs</li>
                <li>Scalable Django backends and integrations</li>
                <li>Telegram bots for support, growth, and operations</li>
              </ul>
            </div>
          </div>
        </section>

        <section id="services" className="section">
          <div className="container">
            <div className="section-head">
              <h2>Services built for business outcomes</h2>
              <p>Pick one priority. I design and deliver the technical system behind it.</p>
            </div>
            <div className="grid">
              {services.map((service) => (
                <article key={service.title} className="card service-card">
                  <h3>{service.title}</h3>
                  <p>{service.description}</p>
                  <a href="#contact" className="text-link">
                    Let’s automate your business
                  </a>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section id="projects" className="section">
          <div className="container">
            <div className="section-head projects-head">
              <h2>Selected projects</h2>
              <p>Proof of delivery: each project shows problem, solution, and measurable result.</p>
              <div className="filter-row" role="group" aria-label="Project filters">
                {tags.map((tag) => (
                  <button
                    key={tag}
                    type="button"
                    className={`filter-btn ${filter === tag ? 'is-selected' : ''}`}
                    onClick={() => setFilter(tag)}
                  >
                    {tag}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid">
              {filteredProjects.map((project) => (
                <article key={project.title} className="card project-card">
                  <div className="project-shot" aria-hidden="true">
                    <span>{project.category}</span>
                  </div>
                  <h3>{project.title}</h3>
                  <p><strong>Problem:</strong> {project.problem}</p>
                  <p><strong>Solution:</strong> {project.solution}</p>
                  <p><strong>Result:</strong> {project.result}</p>
                  <div className="tag-row">
                    {project.stack.map((item) => (
                      <span key={item} className="tag">
                        {item}
                      </span>
                    ))}
                  </div>
                  <div className="action-row">
                    <a href="#contact" className="btn btn-secondary">
                      Live Demo
                    </a>
                    <a href="#contact" className="btn btn-ghost">
                      GitHub / Case Study
                    </a>
                  </div>
                </article>
              ))}
            </div>
            <div className="section-cta-wrap">
              <a href="#contact" className="btn btn-primary">
                Start your project
              </a>
            </div>
          </div>
        </section>

        <section id="about" className="section">
          <div className="container about-grid">
            <div className="profile-image" role="img" aria-label="Portrait placeholder for Kianirad" />
            <div>
              <h2>About Kianirad</h2>
              <p>
                AI-focused backend developer building scalable systems, automation tools, and SaaS
                products. I enjoy turning messy operations into predictable systems teams can trust.
              </p>
              <p>
                Right now I am focused on shipping intelligent automations for startups and growth-stage
                teams that need real outcomes fast.
              </p>
              <a href="#contact" className="btn btn-secondary">
                Book a call
              </a>
            </div>
          </div>
        </section>

        <section className="section trust-section">
          <div className="container">
            <h2>Trust & results</h2>
            <div className="grid metrics-grid">
              {metrics.map((metric) => (
                <article key={metric.label} className="card metric-card">
                  <p className="metric-value">{metric.value}</p>
                  <p>{metric.label}</p>
                </article>
              ))}
            </div>
            <div className="testimonial-placeholder card">
              <h3>Testimonials</h3>
              <p>
                Add verified client testimonials here. No fake reviews used — only real delivery proof.
              </p>
              <a href="#contact" className="text-link">
                Start your project
              </a>
            </div>
          </div>
        </section>

        <section id="contact" className="section">
          <div className="container contact-grid">
            <div>
              <h2>Let’s automate your business</h2>
              <p>
                Tell me your biggest operational bottleneck and I will propose a practical system plan.
              </p>
              <p className="reply-time">I reply within 24 hours.</p>
              <a href="mailto:kianirad2020@gmail.com" className="text-link">
                kianirad2020@gmail.com
              </a>
              <a href="https://t.me" className="btn btn-secondary telegram-btn">
                Message on Telegram
              </a>
            </div>
            <form className="card contact-form" onSubmit={(event) => event.preventDefault()}>
              <label htmlFor="name">Name</label>
              <input id="name" name="name" type="text" autoComplete="name" required />

              <label htmlFor="email">Email</label>
              <input id="email" name="email" type="email" autoComplete="email" required />

              <label htmlFor="message">Project goals</label>
              <textarea id="message" name="message" rows="4" required />

              <button type="submit" className="btn btn-primary">
                Book a Free Consultation
              </button>
            </form>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <div className="container footer-grid">
          <div>
            <p className="brand">Kianirad</p>
            <p>AI systems and backend solutions that help businesses grow faster with less manual work.</p>
          </div>
          <div className="footer-links">
            <a href="mailto:kianirad2020@gmail.com">Email</a>
            <a href="https://github.com">GitHub</a>
            <a href="https://linkedin.com">LinkedIn</a>
          </div>
          <p>© 2026 Kianirad</p>
        </div>
      </footer>
    </div>
  )
}
