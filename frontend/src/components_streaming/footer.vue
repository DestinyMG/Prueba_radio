<template>
  <footer class="main-footer">
    <div class="footer-content">
      <div class="footer-grid">
        <!-- Columna 1: Logo y descripción -->
        <div class="footer-col brand-col">
          <div class="logo-container">
            <i class="fas fa-broadcast-tower"></i>
            <span class="brand-name">KyeroRadio</span>
          </div>
          <p class="brand-tagline">Tu estación de radio las 24 horas</p>
        </div>

        <!-- Columna 2: Redes sociales y acción alineados a la derecha -->
        <div class="footer-col right-col">
          <div class="social-section">
            <h4 class="col-title">Síguenos</h4>
            <div class="social-links">
              <a href="#" class="social-link" aria-label="Facebook">
                <i class="fab fa-facebook-f"></i>
              </a>
              <a href="#" class="social-link" aria-label="Twitter">
                <i class="fab fa-twitter"></i>
              </a>
              <a href="#" class="social-link" aria-label="Instagram">
                <i class="fab fa-instagram"></i>
              </a>
              <a href="#" class="social-link" aria-label="YouTube">
                <i class="fab fa-youtube"></i>
              </a>
            </div>
          </div>
          
          <button class="action-btn" @click="scrollToTop">
            <i class="fas fa-arrow-up"></i>
            <span class="btn-text">Volver Arriba</span>
          </button>
        </div>
      </div>

      <!-- Línea divisoria -->
      <div class="footer-divider"></div>

      <!-- Copyright -->
      <div class="footer-copyright">
        <p>&copy; 2025 KyeroRadio. Todos los derechos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}
</script>

<style scoped>
.main-footer {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.98) 0%, 
    rgba(240, 247, 255, 0.95) 50%, 
    rgba(230, 244, 255, 0.92) 100%);
  color: #2d3748;
  position: relative;
  overflow: hidden;
  border-top: 1px solid rgba(0, 157, 219, 0.3);
  backdrop-filter: blur(15px);
  box-shadow: 0 -4px 25px rgba(0, 125, 184, 0.15);
}

.main-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(0, 157, 219, 0.05) 0%, 
    rgba(0, 125, 184, 0.03) 50%, 
    rgba(255, 255, 255, 0.1) 100%);
  pointer-events: none;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 15px 12px;
  position: relative;
  z-index: 1;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 30px;
  align-items: start;
  margin-bottom: 12px;
}

.footer-col {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.brand-col {
  max-width: 250px;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 700;
}

.logo-container i {
  font-size: 18px;
  background: linear-gradient(135deg, #009DDB, #007DB8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-name {
  background: linear-gradient(135deg, #009DDB, #007DB8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-tagline {
  font-size: 12px;
  color: #5F6C7B;
  line-height: 1.4;
}

/* Columna derecha - Redes y botón alineados */
.right-col {
  align-items: flex-end;
  gap: 12px;
}

.social-section {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.col-title {
  font-size: 13px;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.social-links {
  display: flex;
  gap: 6px;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, rgba(0, 157, 219, 0.1), rgba(0, 125, 184, 0.08));
  border: 1px solid rgba(0, 157, 219, 0.25);
  border-radius: 6px;
  color: #009DDB;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 12px;
}

.social-link:hover {
  background: linear-gradient(135deg, rgba(0, 157, 219, 0.2), rgba(0, 125, 184, 0.15));
  border-color: rgba(0, 157, 219, 0.5);
  color: #007DB8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 157, 219, 0.2);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: linear-gradient(135deg, rgba(0, 157, 219, 0.12), rgba(0, 125, 184, 0.1));
  border: 1px solid rgba(0, 157, 219, 0.3);
  border-radius: 6px;
  color: #009DDB;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.action-btn:hover {
  background: linear-gradient(135deg, rgba(0, 157, 219, 0.2), rgba(0, 125, 184, 0.15));
  border-color: rgba(0, 157, 219, 0.5);
  color: #007DB8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 157, 219, 0.2);
}

.btn-text {
  display: inline;
}

.footer-divider {
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(0, 157, 219, 0.3) 50%, 
    transparent 100%);
  margin: 12px 0 10px;
}

.footer-copyright {
  text-align: center;
}

.footer-copyright p {
  font-size: 10px;
  color: #5F6C7B;
  margin: 0;
}

/* Responsive mejorado */
@media (max-width: 768px) {
  .footer-content {
    padding: 15px 12px 10px;
  }

  .footer-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    text-align: center;
  }

  .brand-col {
    max-width: 100%;
    align-items: center;
  }

  .right-col {
    align-items: center;
    gap: 15px;
  }

  .social-section {
    align-items: center;
  }

  .social-links {
    justify-content: center;
  }

  .logo-container {
    justify-content: center;
  }

  .action-btn {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .footer-content {
    padding: 12px 10px 8px;
  }

  .footer-grid {
    gap: 15px;
  }

  .social-links {
    gap: 5px;
  }

  .social-link {
    width: 26px;
    height: 26px;
    font-size: 11px;
  }

  .action-btn {
    padding: 6px 10px;
    font-size: 10px;
    gap: 4px;
  }

  .logo-container {
    font-size: 15px;
    gap: 5px;
  }

  .logo-container i {
    font-size: 16px;
  }

  .brand-name {
    font-size: 15px;
  }

  .brand-tagline {
    font-size: 11px;
  }

  .col-title {
    font-size: 12px;
  }

  .footer-copyright p {
    font-size: 9px;
  }
}

/* Para móviles muy pequeños */
@media (max-width: 360px) {
  .footer-content {
    padding: 10px 8px 6px;
  }

  .action-btn {
    padding: 5px 8px;
    font-size: 9px;
  }

  .social-link {
    width: 24px;
    height: 24px;
    font-size: 10px;
  }

  .logo-container {
    font-size: 14px;
  }

  .brand-name {
    font-size: 14px;
  }
}
</style>