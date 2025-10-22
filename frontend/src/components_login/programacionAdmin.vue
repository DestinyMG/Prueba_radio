<template>
    <BaseAdmin>
        <div class="admin-container">
            <!-- Header de la página -->
            <div class="page-header">
                <h1><i class="fas fa-calendar-alt"></i> Programación</h1>
                <div class="header-actions">
                    <button class="upload-button" @click="openCreateModal">
                        <i class="fas fa-plus"></i> Nuevo Programa
                    </button>
                </div>
            </div>

            <!-- Mensaje de estado -->
            <div v-if="statusMessage" class="status-message" :class="{ error: statusMessage.includes('Error') }">
                {{ statusMessage }}
            </div>

            <!-- Estadísticas -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-broadcast-tower"></i>
                    </div>
                    <div class="stat-info">
                        <h3>{{ activeProgramsCount }}</h3>
                        <p>Programas Activos</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">
                        <i class="fas fa-calendar-day"></i>
                    </div>
                    <div class="stat-info">
                        <h3>{{ todayProgramsCount }}</h3>
                        <p>Programas Hoy</p>
                    </div>
                </div>
            </div>

            <!-- Grid de programas -->
            <div v-if="programas.length > 0" class="programs-grid">
                <div v-for="programa in programas" :key="programa.id" class="program-card">
                    <div class="card-image-container">
                        <img :src="programa.imagen_url || '/default-program.jpg'" :alt="programa.nombre"
                            class="program-image" @error="handleImageError">
                        <div class="image-overlay"></div>
                        <div class="program-badge">{{ programa.label }}</div>
                    </div>
                    <div class="card-main-content">
                        <div class="card-content">
                            <h3 class="card-title">{{ programa.nombre }}</h3>
                            <p class="card-description">{{ programa.descripcion }}</p>
                            <div class="program-details">
                                <div class="time-slot">
                                    <i class="far fa-clock"></i>
                                    {{ formatTimeForDisplay(programa.hora_inicio) }} - {{
                                    formatTimeForDisplay(programa.hora_fin) }}
                                </div>
                                <!-- ELIMINADO: program-host section -->
                            </div>
                            <p class="card-status" :class="programa.is_active ? 'active' : 'inactive'">
                                <i class="fas" :class="programa.is_active ? 'fa-check-circle' : 'fa-times-circle'"></i>
                                {{ programa.is_active ? 'Activo' : 'Inactivo' }}
                            </p>
                        </div>
                    </div>
                    <div class="card-footer">
                        <div class="card-actions">
                            <button class="action-button edit-button" @click="editPrograma(programa)">
                                <i class="fas fa-edit"></i> Editar
                            </button>
                            <button class="action-button delete-button" @click="deletePrograma(programa.id)">
                                <i class="fas fa-trash"></i> Eliminar
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Estado vacío -->
            <div v-else class="empty-state">
                <div class="empty-icon">
                    <i class="fas fa-calendar-times"></i>
                </div>
                <h2>No hay programas creados</h2>
                <p>Comienza creando tu primer programa de radio.</p>
                <button class="upload-button" @click="openCreateModal">
                    <i class="fas fa-plus"></i> Crear Primer Programa
                </button>
            </div>

            <!-- Modal para crear/editar programa -->
            <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click="closeModal">
                <div class="modal-content" @click.stop>
                    <div class="modal-header">
                        <h2>
                            <i class="fas" :class="isEditing ? 'fa-edit' : 'fa-plus'"></i>
                            {{ isEditing ? 'Editar Programa' : 'Crear Nuevo Programa' }}
                        </h2>
                        <button class="close-button" @click="closeModal">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>

                    <div class="modal-body">
                        <form @submit.prevent="savePrograma" class="program-form">
                            <!-- Información Básica -->
                            <div class="form-section">
                                <h3 class="section-title">
                                    <i class="fas fa-info-circle"></i> Información Básica
                                </h3>
                                <div class="form-grid">
                                    <div class="form-group">
                                        <label for="nombre">
                                            <i class="fas fa-heading"></i> Nombre del Programa *
                                        </label>
                                        <input type="text" id="nombre" v-model="currentPrograma.nombre"
                                            placeholder="Ej: Música Relajante, Éxitos del Momento..." required>
                                    </div>

                                    <div class="form-group">
                                        <label for="label">
                                            <i class="fas fa-tag"></i> Género/Etiqueta *
                                        </label>
                                        <input type="text" id="label" v-model="currentPrograma.label"
                                            placeholder="Ej: Música, Jazz, Rock, Latina..." required>
                                    </div>
                                </div>

                                <div class="form-group full-width">
                                    <label for="descripcion">
                                        <i class="fas fa-comment"></i> Descripción del Programa *
                                    </label>
                                    <textarea id="descripcion" v-model="currentPrograma.descripcion"
                                        placeholder="Describe el contenido del programa..." rows="3"
                                        required></textarea>
                                </div>
                            </div>

                            <!-- Horario -->
                            <div class="form-section">
                                <h3 class="section-title">
                                    <i class="fas fa-clock"></i> Horario
                                </h3>
                                <div class="form-grid"> <!-- ELIMINADO: class="triple" -->
                                    <div class="form-group">
                                        <label for="hora_inicio">
                                            <i class="far fa-clock"></i> Hora de Inicio *
                                        </label>
                                        <input type="time" id="hora_inicio" v-model="currentPrograma.hora_inicio"
                                            required>
                                    </div>

                                    <div class="form-group">
                                        <label for="hora_fin">
                                            <i class="far fa-clock"></i> Hora de Fin *
                                        </label>
                                        <input type="time" id="hora_fin" v-model="currentPrograma.hora_fin" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Imagen -->
                            <div class="form-section">
                                <h3 class="section-title">
                                    <i class="fas fa-image"></i> Imagen del Programa
                                </h3>
                                <div class="form-group full-width">
                                    <label for="imagen" class="file-label">
                                        <i class="fas fa-upload"></i> Seleccionar Imagen
                                    </label>
                                    <input type="file" id="imagen" ref="imagenInput" accept="image/*"
                                        @change="handleImageUpload" class="file-input">
                                    <small class="file-hint">Formatos: JPG, PNG, GIF. Tamaño máximo: 5MB</small>

                                    <!-- Vista previa -->
                                    <div v-if="imagePreview" class="image-preview">
                                        <p class="preview-label">Vista previa:</p>
                                        <img :src="imagePreview" alt="Vista previa" class="preview-image">
                                        <button type="button" class="remove-image-btn" @click="removeImage">
                                            <i class="fas fa-times"></i> Eliminar imagen
                                        </button>
                                    </div>

                                    <!-- Imagen actual -->
                                    <div v-if="isEditing && currentPrograma.imagen_url && !imagePreview"
                                        class="current-image">
                                        <p class="preview-label">Imagen actual:</p>
                                        <img :src="currentPrograma.imagen_url" alt="Imagen actual"
                                            class="preview-image">
                                    </div>
                                </div>
                            </div>

                            <!-- Configuración (solo edición) -->
                            <div class="form-section" v-if="isEditing">
                                <h3 class="section-title">
                                    <i class="fas fa-cog"></i> Configuración
                                </h3>
                                <div class="form-group full-width">
                                    <label class="checkbox-container">
                                        <input type="checkbox" v-model="currentPrograma.is_active">
                                        <span class="checkmark"></span>
                                        <span class="checkbox-label">Programa Activo</span>
                                    </label>
                                    <small>Los programas inactivos no se mostrarán en la programación principal</small>
                                </div>
                            </div>

                            <!-- Acciones -->
                            <div class="form-actions">
                                <button type="button" class="cancel-button" @click="closeModal">
                                    <i class="fas fa-times"></i> Cancelar
                                </button>
                                <button type="submit" class="save-button" :disabled="saving">
                                    <i class="fas" :class="saving ? 'fa-spinner fa-spin' : 'fa-save'"></i>
                                    {{ saving ? 'Guardando...' : 'Guardar Programa' }}
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

// Constante base para la API
const API_BASE_URL = 'https://prueba-radio.onrender.com/api5';

// Variables reactivas
const programas = ref([]);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const isEditing = ref(false);
const saving = ref(false);
const statusMessage = ref('');
const imagePreview = ref(null);
const imagenInput = ref(null);

const currentPrograma = ref({
    nombre: '',
    descripcion: '',
    label: '',
    imagen: null,
    imagen_url: '',
    hora_inicio: '',
    hora_fin: '',
    // ELIMINADO: dj_host: '',
    is_active: true
});

// Computed properties
const activeProgramsCount = computed(() => {
    return programas.value.filter(programa => programa.is_active).length;
});

const todayProgramsCount = computed(() => {
    return programas.value.length;
});

// Funciones para manejo de horas
const formatTimeForInput = (timeString) => {
    if (!timeString) return '';

    // Si ya está en formato 24h (HH:MM), retornar tal cual
    if (timeString.match(/^\d{2}:\d{2}$/)) {
        return timeString;
    }

    // Convertir de formato 12h (AM/PM) a 24h para el input
    const [time, modifier] = timeString.split(' ');
    let [hours, minutes] = time.split(':');

    hours = parseInt(hours);

    if (modifier === 'PM' && hours < 12) {
        hours += 12;
    }
    if (modifier === 'AM' && hours === 12) {
        hours = 0;
    }

    return `${hours.toString().padStart(2, '0')}:${minutes}`;
};

const formatTimeForDisplay = (timeString) => {
    if (!timeString) return '';

    // Si ya está en formato AM/PM, retornar tal cual
    if (timeString.includes('AM') || timeString.includes('PM')) {
        return timeString;
    }

    // Convertir de formato 24h a 12h (AM/PM)
    const [hours, minutes] = timeString.split(':');
    let hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';

    // Convertir a formato 12h
    hour = hour % 12;
    hour = hour === 0 ? 12 : hour; // 0 se convierte en 12

    return `${hour}:${minutes} ${ampm}`;
};

// Funciones de la API
const fetchProgramas = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/programas/`);
        if (response.ok) {
            const data = await response.json();
            programas.value = data;
        } else {
            throw new Error('Error al cargar los programas');
        }
    } catch (error) {
        console.error('Error:', error);
        statusMessage.value = 'Error al cargar los programas';
        setTimeout(() => statusMessage.value = '', 3000);
    }
};

const createPrograma = async (programaData) => {
    try {
        const formData = new FormData();

        // Agregar campos al FormData
        Object.keys(programaData).forEach(key => {
            if (key === 'imagen' && programaData[key]) {
                formData.append('imagen', programaData[key]);
            } else if (key !== 'imagen_url' && key !== 'imagen') {
                formData.append(key, programaData[key]);
            }
        });

        const response = await fetch(`${API_BASE_URL}/programas/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken()
            },
            body: formData
        });

        if (response.ok) {
            return await response.json();
        } else {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Error al crear el programa');
        }
    } catch (error) {
        throw error;
    }
};

const updatePrograma = async (id, programaData) => {
    try {
        const formData = new FormData();

        // Agregar campos al FormData
        Object.keys(programaData).forEach(key => {
            if (key === 'imagen' && programaData[key]) {
                formData.append('imagen', programaData[key]);
            } else if (key !== 'imagen_url' && key !== 'imagen') {
                formData.append(key, programaData[key]);
            }
        });

        const response = await fetch(`${API_BASE_URL}/programas/${id}/`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': getCsrfToken()
            },
            body: formData
        });

        if (response.ok) {
            return await response.json();
        } else {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Error al actualizar el programa');
        }
    } catch (error) {
        throw error;
    }
};

const deletePrograma = async (id) => {
    if (!confirm("¿Estás seguro de eliminar este programa?")) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/programas/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        });

        if (response.ok) {
            await fetchProgramas();
            statusMessage.value = 'Programa eliminado correctamente';
        } else {
            throw new Error('Error al eliminar el programa');
        }
    } catch (error) {
        console.error('Error:', error);
        statusMessage.value = 'Error al eliminar el programa';
    } finally {
        setTimeout(() => statusMessage.value = '', 3000);
    }
};

// Funciones de la UI
const openCreateModal = () => {
    isEditing.value = false;
    showCreateModal.value = true;
};

const editPrograma = (programa) => {
    currentPrograma.value = {
        ...programa,
        hora_inicio: programa.hora_inicio ? formatTimeForInput(programa.hora_inicio) : '',
        hora_fin: programa.hora_fin ? formatTimeForInput(programa.hora_fin) : '',
        imagen: null
    };
    isEditing.value = true;
    showEditModal.value = true;
    imagePreview.value = null;
};

const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
        // Validar tipo de archivo
        if (!file.type.match('image.*')) {
            statusMessage.value = 'Error: Solo se permiten archivos de imagen';
            setTimeout(() => statusMessage.value = '', 3000);
            return;
        }

        // Validar tamaño (5MB máximo)
        if (file.size > 5 * 1024 * 1024) {
            statusMessage.value = 'Error: La imagen no puede superar los 5MB';
            setTimeout(() => statusMessage.value = '', 3000);
            return;
        }

        currentPrograma.value.imagen = file;

        // Crear vista previa
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.value = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

const removeImage = () => {
    currentPrograma.value.imagen = null;
    imagePreview.value = null;
    if (imagenInput.value) {
        imagenInput.value.value = '';
    }
};

const handleImageError = (event) => {
    event.target.src = '/default-program.jpg';
};

const savePrograma = async () => {
    saving.value = true;

    try {
        // Validación
        if (!currentPrograma.value.nombre?.trim()) {
            throw new Error('El campo Nombre es requerido');
        }
        if (!currentPrograma.value.label?.trim()) {
            throw new Error('El campo Género/Etiqueta es requerido');
        }

        if (isEditing.value) {
            await updatePrograma(currentPrograma.value.id, currentPrograma.value);
            statusMessage.value = 'Programa actualizado correctamente';
        } else {
            await createPrograma(currentPrograma.value);
            statusMessage.value = 'Programa creado correctamente';
        }

        await fetchProgramas();
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
    imagePreview.value = null;
    currentPrograma.value = {
        nombre: '',
        descripcion: '',
        label: '',
        imagen: null,
        hora_inicio: '',
        hora_fin: '',
        // ELIMINADO: dj_host: '',
        is_active: true
    };

    // Limpiar input de archivo
    if (imagenInput.value) {
        imagenInput.value.value = '';
    }
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
    fetchProgramas();
});
</script>

<style scoped>
.admin-container {
    padding: 20px;
    max-width: 1400px;
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
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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

.programs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 25px;
}

.program-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: all 0.3s ease;
    border: 1px solid #e9ecef;
}

.program-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.card-image-container {
    position: relative;
    height: 200px;
    overflow: hidden;
}

.program-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.program-card:hover .program-image {
    transform: scale(1.05);
}

.image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.1) 100%);
}

.program-badge {
    position: absolute;
    top: 15px;
    left: 15px;
    background: #3498db;
    color: white;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.card-main-content {
    padding: 20px;
}

.card-content {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.card-title {
    margin: 0;
    color: #2c3e50;
    font-size: 18px;
    font-weight: 700;
    line-height: 1.3;
}

.card-description {
    margin: 0;
    color: #6c757d;
    font-size: 14px;
    line-height: 1.5;
}

.program-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.time-slot,
.program-host {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #495057;
    font-size: 14px;
    font-weight: 500;
}

.time-slot i,
.program-host i {
    color: #3498db;
    width: 16px;
}

.card-status {
    margin: 0;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
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
}

.card-actions {
    display: flex;
    gap: 10px;
}

.action-button {
    padding: 8px 16px;
    border: 1px solid #ddd;
    border-radius: 6px;
    background: white;
    color: #6c757d;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 6px;
    flex: 1;
    justify-content: center;
}

.edit-button:hover {
    border-color: #3498db;
    color: #3498db;
    background: #e3f2fd;
}

.delete-button:hover {
    border-color: #e74c3c;
    color: #e74c3c;
    background: #fdedec;
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

/* Modal Styles - Mejorado y Organizado */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}

.modal-content {
    width: 90%;
    max-width: 600px;
    max-height: 90vh;
    background: white;
    border-radius: 12px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.modal-header {
    padding: 20px 24px;
    border-bottom: 1px solid #e9ecef;
    background: #f8f9fa;
    flex-shrink: 0;
}

.modal-header h2 {
    margin: 0;
    color: #2c3e50;
    font-size: 20px;
    font-weight: 600;
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
    padding: 8px;
    border-radius: 4px;
    transition: all 0.2s ease;
}

.close-button:hover {
    background: #e9ecef;
    color: #2c3e50;
}

.modal-body {
    flex: 1;
    overflow-y: auto;
    padding: 0;
}

.program-form {
    padding: 24px;
}

/* Secciones del formulario */
.form-section {
    margin-bottom: 32px;
}

.form-section:last-of-type {
    margin-bottom: 0;
}

.section-title {
    font-size: 16px;
    color: #2c3e50;
    margin: 0 0 20px 0;
    padding: 0;
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
}

.section-title i {
    color: #3498db;
    font-size: 14px;
}

/* Grid del formulario */
.form-grid {
    display: grid;
    gap: 20px;
    margin-bottom: 20px;
}

.form-grid {
    grid-template-columns: 1fr 1fr;
}

.form-grid.triple {
    grid-template-columns: 1fr 1fr 1fr;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group.full-width {
    grid-column: 1 / -1;
}

.form-group label {
    margin-bottom: 8px;
    font-weight: 600;
    color: #2c3e50;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.form-group label i {
    color: #3498db;
    width: 16px;
    text-align: center;
}

.form-group input,
.form-group textarea {
    padding: 12px;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 14px;
    transition: all 0.3s ease;
    background: white;
    font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-group textarea {
    resize: vertical;
    min-height: 100px;
}

/* Estilos para archivos */
.file-label {
    cursor: pointer;
    padding: 12px;
    border: 2px dashed #e9ecef;
    border-radius: 8px;
    text-align: center;
    transition: all 0.3s ease;
    background: #fafbfc;
}

.file-label:hover {
    border-color: #3498db;
    background: #f8f9fa;
}

.file-input {
    display: none;
}

.file-hint {
    margin-top: 8px;
    color: #6c757d;
    font-size: 12px;
    text-align: center;
}

/* Checkbox */
.checkbox-container {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 8px 0;
}

.checkbox-container input[type="checkbox"] {
    width: 18px;
    height: 18px;
    margin: 0;
}

.checkbox-label {
    font-weight: 500;
    color: #2c3e50;
}

/* Vista previa de imagen */
.image-preview,
.current-image {
    margin-top: 16px;
    padding: 16px;
    border: 2px dashed #e9ecef;
    border-radius: 8px;
    background: #fafbfc;
    text-align: center;
}

.preview-label {
    margin: 0 0 12px 0;
    font-size: 14px;
    color: #495057;
    font-weight: 500;
}

.preview-image {
    max-width: 100%;
    max-height: 200px;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 12px;
}

.remove-image-btn {
    background: #e74c3c;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s ease;
}

.remove-image-btn:hover {
    background: #c0392b;
    transform: translateY(-1px);
}

/* Acciones del formulario */
.form-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid #e9ecef;
}

.cancel-button,
.save-button {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    min-width: 140px;
    justify-content: center;
}

.cancel-button {
    background: #6c757d;
    color: white;
}

.cancel-button:hover {
    background: #5a6268;
    transform: translateY(-1px);
}

.save-button {
    background: #3498db;
    color: white;
}

.save-button:hover:not(:disabled) {
    background: #2980b9;
    transform: translateY(-1px);
}

.save-button:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
    transform: none;
}

/* Scrollbar personalizado */
.modal-body::-webkit-scrollbar {
    width: 6px;
}

.modal-body::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.modal-body::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}

/* Responsive */
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

    .programs-grid {
        grid-template-columns: 1fr;
    }

    .modal-content {
        width: 95%;
        max-height: 95vh;
    }

    .program-form {
        padding: 20px;
    }

    .form-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    .form-grid.triple {
        grid-template-columns: 1fr;
    }

    .form-actions {
        flex-direction: column;
    }

    .cancel-button,
    .save-button {
        width: 100%;
        min-width: auto;
    }

    .modal-header {
        padding: 16px 20px;
    }
}

@media (max-width: 480px) {
    .program-form {
        padding: 16px;
    }

    .form-section {
        margin-bottom: 24px;
    }

    .section-title {
        font-size: 15px;
        margin-bottom: 16px;
    }
}
</style>