<template>
    <BaseAdmin>
        <div class="admin-container">
            <!-- Indicador de estado -->
            <div v-if="statusMessage" class="status-message" :class="{ error: statusMessage.includes('Error') }">
                {{ statusMessage }}
            </div>

            <div class="page-header">
                <h1><i class="fas fa-newspaper"></i> Gestión de Noticias</h1>
                <div class="header-actions">
                    <button class="upload-button" @click="showCreateModal = true">
                        <i class="fas fa-plus"></i> Crear Nueva Noticia
                    </button>
                </div>
            </div>

            <!-- Estadísticas rápidas -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-newspaper"></i></div>
                    <div class="stat-info">
                        <h3>{{ newsItems.length }}</h3>
                        <p>Noticias Totales</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-eye"></i></div>
                    <div class="stat-info">
                        <h3>{{ activeNewsCount }}</h3>
                        <p>Noticias Activas</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-clock"></i></div>
                    <div class="stat-info">
                        <h3>{{ recentNewsCount }}</h3>
                        <p>Recientes (7 días)</p>
                    </div>
                </div>
            </div>

            <!-- Grid de noticias -->
            <div class="news-grid" v-if="newsItems.length > 0">
                <div v-for="news in newsItems" :key="news.id" class="news-card">
                    <div class="card-main-content">
                        <div class="card-icon" :class="getNewsTypeClass(news.label)">
                            <i class="fas" :class="getNewsTypeIcon(news.label)"></i>
                        </div>
                        <div class="card-content">
                            <div class="news-badge">{{ news.label }}</div>
                            <h3 class="card-title">{{ news.message }}</h3>
                            <p class="card-url">
                                <i class="fas fa-link"></i>
                                <a :href="news.url" target="_blank" class="news-link">{{ news.shortUrl }}</a>
                            </p>
                            <p class="card-date">
                                <i class="fas fa-calendar"></i>
                                Creada: {{ formatDate(news.created_at) }}
                            </p>
                            <p class="card-status" :class="{ active: news.is_active, inactive: !news.is_active }">
                                <i class="fas" :class="news.is_active ? 'fa-check-circle' : 'fa-times-circle'"></i>
                                {{ news.is_active ? 'Activa' : 'Inactiva' }}
                            </p>
                        </div>
                    </div>

                    <div class="card-footer">
                        <div class="card-actions">
                            <button class="action-button edit-button" @click="editNews(news)">
                                <i class="fas fa-edit"></i> Editar
                            </button>
                            <button class="action-button delete-button" @click="deleteNews(news.id)">
                                <i class="fas fa-trash"></i> Eliminar
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Estado vacío -->
            <div v-else class="empty-state">
                <div class="empty-icon"><i class="fas fa-newspaper"></i></div>
                <h2>No hay noticias creadas</h2>
                <p>Comienza creando tu primera noticia para mostrar en el panel</p>
                <button class="upload-button" @click="showCreateModal = true">
                    <i class="fas fa-plus"></i> Crear Primera Noticia
                </button>
            </div>

            <!-- Modal para crear/editar noticia -->
            <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click="closeModal">
                <div class="modal-content" @click.stop>
                    <div class="modal-header">
                        <h2>
                            <i class="fas" :class="isEditing ? 'fa-edit' : 'fa-plus'"></i>
                            {{ isEditing ? 'Editar Noticia' : 'Crear Nueva Noticia' }}
                        </h2>
                        <button class="close-button" @click="closeModal">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="form-container">
                        <form @submit.prevent="saveNews">
                            <div class="form-group">
                                <label for="label">
                                    <i class="fas fa-tag"></i> Label
                                </label>
                                <input 
                                    type="text" 
                                    id="label" 
                                    v-model="currentNews.label" 
                                    placeholder="Ej: DW, BBC, Actualidad..."
                                    maxlength="10"
                                    required
                                >
                                <small>Máximo 10 caracteres</small>
                            </div>

                            <div class="form-group">
                                <label for="message">
                                    <i class="fas fa-comment"></i> Mensaje de la Noticia
                                </label>
                                <textarea 
                                    id="message" 
                                    v-model="currentNews.message" 
                                    placeholder="Ingresa el contenido de la noticia..."
                                    rows="4"
                                    required
                                ></textarea>
                            </div>

                            <div class="form-group">
                                <label for="url">
                                    <i class="fas fa-link"></i> URL de la Noticia
                                </label>
                                <input 
                                    type="url" 
                                    id="url" 
                                    v-model="currentNews.url" 
                                    placeholder="https://ejemplo.com/noticia"
                                    required
                                >
                            </div>

                            <div class="form-group" v-if="isEditing">
                                <label class="checkbox-label">
                                    <input type="checkbox" v-model="currentNews.is_active">
                                    <span class="checkmark"></span>
                                    Noticia Activa
                                </label>
                                <small>Las noticias inactivas no se mostrarán en el panel principal</small>
                            </div>

                            <div class="form-actions">
                                <button type="button" class="cancel-button" @click="closeModal">
                                    <i class="fas fa-times"></i> Cancelar
                                </button>
                                <button type="submit" class="save-button" :disabled="saving">
                                    <i class="fas" :class="saving ? 'fa-spinner fa-spin' : 'fa-save'"></i>
                                    {{ saving ? 'Guardando...' : 'Guardar Noticia' }}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </BaseAdmin>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import BaseAdmin from './BaseAdmin.vue';

// Constante base para la API - ÚSALA EN TODAS LAS FUNCIONES
const API_BASE_URL = 'http://localhost:8000/api4';

// Variables reactivas
const newsItems = ref([]);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const isEditing = ref(false);
const saving = ref(false);
const statusMessage = ref('');
const currentNews = ref({
    label: '',
    message: '',
    url: '',
    is_active: true
});

// Computed properties
const activeNewsCount = computed(() => {
    return newsItems.value.filter(news => news.is_active).length;
});

const inactiveNewsCount = computed(() => {
    return newsItems.value.filter(news => !news.is_active).length;
});

const recentNewsCount = computed(() => {
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
    return newsItems.value.filter(news => new Date(news.created_at) > oneWeekAgo).length;
});

// Funciones auxiliares
const getNewsTypeClass = (label) => {
    const classes = {
        'DW': 'type-dw',
        'BBC': 'type-bbc',
        'OTRO': 'type-other'
    };
    return classes[label] || 'type-other';
};

const getNewsTypeIcon = (label) => {
    const icons = {
        'DW': 'fa-globe-europe',
        'BBC': 'fa-globe-americas',
        'OTRO': 'fa-newspaper'
    };
    return icons[label] || 'fa-newspaper';
};

const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleString("es-ES", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
    });
};

// Funciones de la API - TODAS USAN LA MISMA URL BASE
const fetchNews = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/news/`);
        if (response.ok) {
            newsItems.value = await response.json();
        } else {
            throw new Error('Error al cargar las noticias');
        }
    } catch (error) {
        console.error('Error:', error);
        statusMessage.value = 'Error al cargar las noticias';
        setTimeout(() => statusMessage.value = '', 3000);
    }
};

const createNews = async (newsData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/news/`, {  // ← CORREGIDO
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(newsData)
        });

        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('Error al crear la noticia');
        }
    } catch (error) {
        throw error;
    }
};

const updateNews = async (id, newsData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/news/${id}/`, {  // ← CORREGIDO
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(newsData)
        });

        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('Error al actualizar la noticia');
        }
    } catch (error) {
        throw error;
    }
};

const deleteNews = async (id) => {
    if (!confirm("¿Estás seguro de eliminar esta noticia?")) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/news/${id}/`, {  // ← CORREGIDO
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        });

        if (response.ok) {
            await fetchNews();
            statusMessage.value = 'Noticia eliminada correctamente';
        } else {
            throw new Error('Error al eliminar la noticia');
        }
    } catch (error) {
        console.error('Error:', error);
        statusMessage.value = 'Error al eliminar la noticia';
    } finally {
        setTimeout(() => statusMessage.value = '', 3000);
    }
};

// Funciones de la UI
const editNews = (news) => {
    currentNews.value = { ...news };
    isEditing.value = true;
    showEditModal.value = true;
};

const toggleNewsStatus = async (news) => {
    try {
        const updatedNews = { ...news, is_active: !news.is_active };
        await updateNews(news.id, updatedNews);
        await fetchNews();
        statusMessage.value = `Noticia ${updatedNews.is_active ? 'activada' : 'desactivada'} correctamente`;
    } catch (error) {
        console.error('Error:', error);
        statusMessage.value = 'Error al cambiar el estado de la noticia';
    } finally {
        setTimeout(() => statusMessage.value = '', 3000);
    }
};

const saveNews = async () => {
    saving.value = true;
    
    try {
        // Validación adicional
        if (!currentNews.value.label?.trim()) {
            throw new Error('El campo Label es requerido');
        }
        
        if (isEditing.value) {
            await updateNews(currentNews.value.id, currentNews.value);
            statusMessage.value = 'Noticia actualizada correctamente';
        } else {
            await createNews(currentNews.value);
            statusMessage.value = 'Noticia creada correctamente';
        }
        
        await fetchNews();
        closeModal();
    } catch (error) {
        console.error('Error:', error);
        statusMessage.value = `Error: ${error.message}`;
    } finally {
        saving.value = false;
        setTimeout(() => statusMessage.value = '', 3000);
    }
};

const closeModal = () => {
    showCreateModal.value = false;
    showEditModal.value = false;
    isEditing.value = false;
    currentNews.value = {
        label: '',
        message: '',
        url: '',
        is_active: true
    };
};

// Función para obtener el token CSRF
const getCsrfToken = () => {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
};

// Inicialización
onMounted(() => {
    fetchNews();
});
</script>

<style scoped>
.admin-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

.status-message {
    padding: 12px 16px;
    border-radius: 6px;
    background-color: #d4edda;
    color: #155724;
    font-weight: 500;
    text-align: center;
    margin-bottom: 20px;
}

.status-message.error {
    background-color: #f8d7da;
    color: #721c24;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #e9ecef;
}

.page-header h1 {
    color: #e9ecef;
    font-size: 28px;
    margin: 0;
}

.page-header h1 i {
    margin-right: 10px;
    color: #3498db;
}

.header-actions {
    display: flex;
    gap: 15px;
}

.upload-button {
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    background: #3498db;
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}

.upload-button:hover {
    background: #2980b9;
    transform: translateY(-2px);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    gap: 15px;
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-3px);
}

.stat-icon {
    font-size: 24px;
    width: 50px;
    height: 50px;
    background: #f8f9fa;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.stat-info h3 {
    margin: 0;
    font-size: 24px;
    font-weight: 700;
}

.stat-info p {
    margin: 5px 0 0 0;
    color: #6c757d;
    font-size: 14px;
}

.news-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 20px;
}

.news-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    overflow: hidden;
    transition: all 0.3s ease;
}

.news-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.card-main-content {
    padding: 20px;
    display: flex;
    align-items: flex-start;
    gap: 15px;
}

.card-icon {
    font-size: 20px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 2px;
}

.card-icon.type-dw {
    background: #e3f2fd;
    color: #1976d2;
}

.card-icon.type-bbc {
    background: #fff3e0;
    color: #f57c00;
}

.card-icon.type-other {
    background: #f3e5f5;
    color: #7b1fa2;
}

.card-content {
    flex: 1;
}

.news-badge {
    display: inline-block;
    padding: 4px 8px;
    background: #3498db;
    color: white;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 10px;
}

.card-title {
    margin: 0 0 12px 0;
    color: #2c3e50;
    font-size: 16px;
    font-weight: 600;
    line-height: 1.4;
}

.card-url, .card-date, .card-status {
    margin: 0 0 8px 0;
    color: #6c757d;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.news-link {
    color: #3498db;
    text-decoration: none;
}

.news-link:hover {
    text-decoration: underline;
}

.card-status.active {
    color: #27ae60;
}

.card-status.inactive {
    color: #e74c3c;
}

.card-footer {
    padding: 15px 20px;
    background: #f8f9fa;
    border-top: 1px solid #e9ecef;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
}

.card-actions {
    display: flex;
    gap: 10px;
}

.action-button {
    padding: 6px 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    background: white;
    color: #6c757d;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.edit-button:hover {
    border-color: #3498db;
    color: #3498db;
}

.delete-button:hover {
    border-color: #e74c3c;
    color: #e74c3c;
}

.toggle-button {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    background: #6c757d;
    color: white;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 6px;
    min-width: 120px;
    justify-content: center;
}

.toggle-button:hover {
    background: #5a6268;
    transform: translateY(-1px);
}

.toggle-button.active {
    background: #27ae60;
}

.toggle-button.active:hover {
    background: #219a52;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #6c757d;
}

.empty-icon {
    font-size: 64px;
    color: #bdc3c7;
    margin-bottom: 20px;
}

.empty-state h2 {
    color: #2c3e50;
    margin-bottom: 10px;
}

.empty-state p {
    margin-bottom: 30px;
    font-size: 16px;
}

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}

.modal-content {
    background: white;
    border-radius: 12px;
    width: 100%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.modal-header {
    padding: 20px 24px;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h2 {
    margin: 0;
    color: #2c3e50;
    font-size: 20px;
}

.modal-header h2 i {
    margin-right: 8px;
    color: #3498db;
}

.close-button {
    background: none;
    border: none;
    font-size: 18px;
    color: #6c757d;
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
}

.close-button:hover {
    background: #f8f9fa;
    color: #2c3e50;
}

.form-container {
    padding: 24px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #2c3e50;
}

.form-group label i {
    margin-right: 6px;
    color: #3498db;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-group textarea {
    resize: vertical;
    min-height: 80px;
}

.checkbox-label {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-weight: normal;
}

.checkbox-label input[type="checkbox"] {
    width: auto;
}

.form-group small {
    display: block;
    margin-top: 4px;
    color: #6c757d;
    font-size: 12px;
}

.form-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
    margin-top: 30px;
}

.cancel-button, .save-button {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 6px;
}

.cancel-button {
    background: #6c757d;
    color: white;
}

.cancel-button:hover {
    background: #5a6268;
}

.save-button {
    background: #3498db;
    color: white;
}

.save-button:hover:not(:disabled) {
    background: #2980b9;
}

.save-button:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
}

@media (max-width: 768px) {
    .admin-container {
        padding: 15px;
    }
    
    .page-header {
        flex-direction: column;
        gap: 15px;
        align-items: flex-start;
    }
    
    .header-actions {
        width: 100%;
    }
    
    .news-grid {
        grid-template-columns: 1fr;
    }
    
    .card-footer {
        flex-direction: column;
        align-items: stretch;
    }
    
    .card-actions {
        justify-content: center;
        margin-bottom: 10px;
    }
    
    .form-actions {
        flex-direction: column;
    }
}
</style>