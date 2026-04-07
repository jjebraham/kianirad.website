import React, { useState, useEffect } from 'react';

export default function KianiradWebsite() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [selectedProject, setSelectedProject] = useState(null);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close modal on escape key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') setSelectedProject(null);
    };
    if (selectedProject) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [selectedProject]);

  const portfolioItems = [
    { id: 1, title: 'E-Commerce Platform', category: 'Web Development', image: 'https://images.unsplash.com/photo-1547658719-da2b51169166?w=500', tall: false },
    { id: 2, title: 'SaaS Dashboard', category: 'UI/UX Design', image: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=500', tall: true },
    { id: 3, title: 'Code Editor Theme', category: 'Development', image: 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=500', tall: true },
    { id: 4, title: 'Fitness Tracker App', category: 'Mobile Design', image: 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=500', tall: false },
    { id: 5, title: 'API Console', category: 'Development', image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=500', tall: false },
    { id: 6, title: 'Creative Portfolio', category: 'Web Design', image: 'https://images.unsplash.com/photo-1593720213428-28a5b9e94613?w=500', tall: true },
  ];

  const navLinks = ['Home', 'Projects', 'Services', 'About', 'Contact'];

  // Prevent body scroll when modal is open
  useEffect(() => {
    if (selectedProject) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
  }, [selectedProject]);

  return (
    <div style={styles.container}>
      {/* Navigation */}
      <nav style={{
        ...styles.nav,
        background: scrolled ? 'white' : 'transparent',
        boxShadow: scrolled ? '0 2px 20px rgba(0,0,0,0.1)' : 'none',
        padding: scrolled ? '15px 0' : '25px 0'
      }}>
        <div style={styles.navContainer}>
          <div style={styles.logo}>KIANIRAD</div>

          {/* Desktop Menu */}
          <ul style={styles.desktopMenu} className="desktop-menu">
            {navLinks.map((item) => (
              <li key={item} style={styles.navItem}>
                <a href={`#${item.toLowerCase()}`} style={styles.navLink}>
                  {item}
                </a>
              </li>
            ))}
          </ul>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            style={styles.mobileMenuBtn}
            className="mobile-menu-btn"
            aria-label="Toggle menu"
          >
            {isMenuOpen ? '✕' : '☰'}
          </button>
        </div>

        {/* Mobile Menu Dropdown */}
        {isMenuOpen && (
          <div style={styles.mobileMenu}>
            {navLinks.map((item) => (
              <a
                key={item}
                href={`#${item.toLowerCase()}`}
                style={styles.mobileNavLink}
                onClick={() => setIsMenuOpen(false)}
              >
                {item}
              </a>
            ))}
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <header style={styles.hero} id="home">
        <div style={styles.heroContent}>
          <div style={styles.heroAvatar}>
            <span style={styles.heroAvatarText}>K</span>
          </div>

          <h1 style={styles.heroTitle}>Welcome to KIANIRAD</h1>

          <p style={styles.heroSubtitle}>Web Design & Development</p>

          <p style={styles.heroText}>
            From experimental passion projects to commissioned work for clients, my portfolio holds a diverse selection of creations that represent this dynamic industry.
          </p>

          <button style={styles.ctaButton}>
            Explore My Work →
          </button>
        </div>
      </header>

      {/* Services Section */}
      <section style={styles.section} id="services">
        <div style={styles.containerInner}>
          <div style={styles.servicesGrid}>
            {[
              { title: 'Web Development', desc: 'Custom websites built with modern technologies', icon: '💻' },
              { title: 'UI/UX Design', desc: 'Beautiful, user-centered interface design', icon: '🎨' },
              { title: 'Performance', desc: 'Fast, optimized web applications', icon: '⚡' }
            ].map((service, idx) => (
              <div key={idx} style={styles.serviceCard} className="service-card">
                <div style={styles.serviceIcon}>{service.icon}</div>
                <h3 style={styles.serviceTitle}>{service.title}</h3>
                <p style={styles.serviceDesc}>{service.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Portfolio Grid */}
      <section style={styles.section} id="projects">
        <div style={styles.containerInner}>
          <h2 style={styles.sectionTitle}>Recent Projects</h2>

          <div style={styles.portfolioGrid}>
            {portfolioItems.map((item) => (
              <div
                key={item.id}
                onClick={() => setSelectedProject(item)}
                style={{
                  ...styles.portfolioItem,
                  gridRow: item.tall ? 'span 2' : 'span 1'
                }}
                className="portfolio-item"
              >
                <img
                  src={item.image}
                  alt={item.title}
                  style={styles.portfolioImage}
                  loading="lazy"
                />
                <div style={styles.portfolioOverlay}>
                  <div style={styles.portfolioCategory}>{item.category}</div>
                  <div style={styles.portfolioTitle}>{item.title}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Inspiring Design Section */}
      <section style={{ ...styles.section, ...styles.whiteBg }} id="about">
        <div style={styles.containerInner}>
          <h2 style={styles.sectionTitle}>Inspiring Design</h2>
          <p style={styles.sectionSubtitle}>
            Creativity meets functionality in every project
          </p>

          <div style={styles.designGrid}>
            {[
              'https://images.unsplash.com/photo-1522542550221-31fd19575a2d?w=500',
              'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500',
              'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=500',
              'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=500'
            ].map((img, idx) => (
              <div key={idx} style={styles.designItem} className="design-item">
                <img
                  src={img}
                  alt={`Design showcase ${idx + 1}`}
                  style={styles.designImage}
                  loading="lazy"
                />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={styles.footer} id="contact">
        <h3 style={styles.footerTitle}>Kianirad Web Design & Development</h3>
        <a href="mailto:kianirad2020@gmail.com" style={styles.footerLink}>
          kianirad2020@gmail.com
        </a>
        <p style={styles.footerCopy}>
          ©2024 by Kiani Limited Liability Company.
        </p>
      </footer>

      {/* Project Modal */}
      {selectedProject && (
        <div
          onClick={() => setSelectedProject(null)}
          style={styles.modalOverlay}
          role="dialog"
          aria-modal="true"
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={styles.modalContent}
          >
            <div style={styles.modalHeader}>
              <div>
                <div style={styles.modalCategory}>{selectedProject.category}</div>
                <h2 style={styles.modalTitle}>{selectedProject.title}</h2>
              </div>
              <button
                onClick={() => setSelectedProject(null)}
                style={styles.modalClose}
                aria-label="Close modal"
              >
                ×
              </button>
            </div>

            <img
              src={selectedProject.image}
              alt={selectedProject.title}
              style={styles.modalImage}
            />

            <p style={styles.modalText}>
              This project showcases modern web development techniques and design principles, delivering an exceptional user experience with cutting-edge technology.
            </p>

            <button style={styles.modalButton}>
              View Live Project
            </button>
          </div>
        </div>
      )}

      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-15px); }
        }

        @keyframes scaleIn {
          from { transform: scale(0.9); opacity: 0; }
          to { transform: scale(1); opacity: 1; }
        }

        .service-card {
          transition: all 0.3s ease;
          cursor: pointer;
        }

        .service-card:hover {
          transform: translateY(-10px);
          box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }

        .portfolio-item {
          transition: all 0.3s ease;
        }

        .portfolio-item:hover {
          transform: scale(1.02);
          box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }

        .design-item {
          transition: all 0.3s ease;
          cursor: pointer;
        }

        .design-item:hover {
          transform: scale(1.05);
        }

        a:hover {
          color: #667eea !important;
        }

        @media (max-width: 768px) {
          .desktop-menu { display: none !important; }
          .mobile-menu-btn { display: block !important; }
        }
      `}</style>
    </div>
  );
}

// Styles object to prevent recreation on every render
const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)'
  },
  nav: {
    position: 'fixed',
    width: '100%',
    top: 0,
    zIndex: 1000,
    transition: 'all 0.3s ease'
  },
  navContainer: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 30px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  logo: {
    fontSize: '20px',
    fontWeight: 'bold',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text'
  },
  desktopMenu: {
    display: 'flex',
    gap: '30px',
    listStyle: 'none',
    margin: 0,
    padding: 0
  },
  navItem: {
    display: 'block'
  },
  navLink: {
    textDecoration: 'none',
    color: '#333',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'color 0.3s'
  },
  mobileMenuBtn: {
    display: 'none',
    background: 'none',
    border: 'none',
    fontSize: '24px',
    cursor: 'pointer'
  },
  mobileMenu: {
    position: 'absolute',
    top: '100%',
    left: 0,
    right: 0,
    background: 'white',
    padding: '20px',
    boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
    display: 'flex',
    flexDirection: 'column',
    gap: '15px'
  },
  mobileNavLink: {
    color: '#333',
    textDecoration: 'none',
    fontSize: '16px',
    padding: '10px 0',
    borderBottom: '1px solid #eee'
  },
  hero: {
    paddingTop: '150px',
    paddingBottom: '80px',
    textAlign: 'center'
  },
  heroContent: {
    maxWidth: '1000px',
    margin: '0 auto',
    padding: '0 30px'
  },
  heroAvatar: {
    width: '200px',
    height: '200px',
    margin: '0 auto 40px',
    borderRadius: '50%',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: '0 20px 60px rgba(102, 126, 234, 0.4)',
    animation: 'float 3s ease-in-out infinite'
  },
  heroAvatarText: {
    color: 'white',
    fontSize: '80px',
    fontWeight: 'bold'
  },
  heroTitle: {
    fontSize: '56px',
    fontWeight: 'bold',
    marginBottom: '20px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text'
  },
  heroSubtitle: {
    fontSize: '24px',
    color: '#666',
    marginBottom: '20px'
  },
  heroText: {
    fontSize: '18px',
    color: '#888',
    maxWidth: '700px',
    margin: '0 auto 40px',
    lineHeight: '1.6'
  },
  ctaButton: {
    padding: '18px 40px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '50px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
    boxShadow: '0 10px 30px rgba(102, 126, 234, 0.3)',
    transition: 'all 0.3s ease'
  },
  section: {
    padding: '60px 30px'
  },
  containerInner: {
    maxWidth: '1200px',
    margin: '0 auto'
  },
  whiteBg: {
    background: 'white'
  },
  servicesGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '30px'
  },
  serviceCard: {
    background: 'white',
    padding: '40px',
    borderRadius: '20px',
    boxShadow: '0 10px 30px rgba(0,0,0,0.1)'
  },
  serviceIcon: {
    fontSize: '48px',
    marginBottom: '20px'
  },
  serviceTitle: {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '10px',
    color: '#333'
  },
  serviceDesc: {
    color: '#666',
    lineHeight: '1.6'
  },
  sectionTitle: {
    fontSize: '42px',
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: '50px',
    color: '#333'
  },
  sectionSubtitle: {
    color: '#666',
    fontSize: '18px',
    maxWidth: '600px',
    margin: '0 auto 50px',
    textAlign: 'center'
  },
  portfolioGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '25px',
    gridAutoRows: '250px'
  },
  portfolioItem: {
    position: 'relative',
    borderRadius: '20px',
    overflow: 'hidden',
    cursor: 'pointer',
    boxShadow: '0 10px 30px rgba(0,0,0,0.1)'
  },
  portfolioImage: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    display: 'block'
  },
  portfolioOverlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: '25px',
    background: 'linear-gradient(to top, rgba(0,0,0,0.9), transparent)',
    color: 'white'
  },
  portfolioCategory: {
    fontSize: '12px',
    color: '#a78bfa',
    marginBottom: '5px',
    fontWeight: '600'
  },
  portfolioTitle: {
    fontSize: '20px',
    fontWeight: 'bold'
  },
  designGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '25px'
  },
  designItem: {
    borderRadius: '20px',
    overflow: 'hidden',
    boxShadow: '0 10px 30px rgba(0,0,0,0.1)'
  },
  designImage: {
    width: '100%',
    height: '280px',
    objectFit: 'cover',
    display: 'block'
  },
  footer: {
    background: '#1a1a1a',
    color: 'white',
    padding: '50px 30px',
    textAlign: 'center'
  },
  footerTitle: {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '15px'
  },
  footerLink: {
    color: '#a78bfa',
    textDecoration: 'none',
    fontSize: '16px'
  },
  footerCopy: {
    color: '#666',
    marginTop: '20px',
    fontSize: '14px'
  },
  modalOverlay: {
    position: 'fixed',
    inset: 0,
    background: 'rgba(0,0,0,0.8)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '30px',
    zIndex: 2000,
    backdropFilter: 'blur(5px)'
  },
  modalContent: {
    background: 'white',
    borderRadius: '30px',
    maxWidth: '700px',
    width: '100%',
    padding: '40px',
    animation: 'scaleIn 0.3s ease',
    maxHeight: '90vh',
    overflow: 'auto'
  },
  modalHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'start',
    marginBottom: '25px'
  },
  modalCategory: {
    color: '#667eea',
    fontWeight: '600',
    fontSize: '14px'
  },
  modalTitle: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#333',
    marginTop: '5px'
  },
  modalClose: {
    background: 'none',
    border: 'none',
    fontSize: '28px',
    cursor: 'pointer',
    color: '#999',
    lineHeight: 1
  },
  modalImage: {
    width: '100%',
    borderRadius: '20px',
    marginBottom: '25px'
  },
  modalText: {
    color: '#666',
    lineHeight: '1.8',
    marginBottom: '25px'
  },
  modalButton: {
    padding: '15px 35px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '50px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer'
  }
};
