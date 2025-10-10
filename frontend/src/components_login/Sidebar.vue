<template>
    <aside class="sidebar">
        <div class="menu-section">
            <span class="menu-title">MENÚ</span>
            <ul>
                <li class="active">
                    <RouterLink to="audios" class="menu-link">
                        <i class="icon">🏠</i> <span>Audios</span>
                    </RouterLink>
                </li>
                <li>
                    <a href="#">
                        <i class="icon">🔍</i>
                        <span>Explorar</span>
                    </a>
                </li>
                <li>
                    <a href="#">
                        <i class="icon">📻</i>
                        <span>Radio</span>
                    </a>
                </li>
                <li>
                    <a href="#">
                        <i class="icon">📅</i>
                        <span>Programación</span>
                    </a>
                </li>
            </ul>
        </div>
        <div class="library-section">
            <span class="menu-title">TU BIBLIOTECA</span>
            <ul>
                <li>
                    <RouterLink to="streaming" class="menu-link">
                        <i class="icon">❤️</i>
                        <span>Streaming</span>
                    </RouterLink>
                </li>
                <li>
                    <a href="#">
                        <i class="icon">🕒</i>
                        <span>Recientes</span>
                    </a>
                </li>
                <li>
                    <a href="#">
                        <i class="icon">📄</i>
                        <span>Listas</span>
                    </a>
                </li>
            </ul>
        </div>
        <div class="logout-section">
            <a href="#" class="logout-btn" @click.prevent="logout">
                <i class="icon">➡️</i>
                <span>Cerrar Sesión</span>
            </a>
        </div>
    </aside>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
    // Borrar tokens
    localStorage.removeItem('auth_tokens')

    // Redirigir al login
    router.push('/login')
}
</script>

<style scoped>
.sidebar {
    width: 240px;
    background-color: #ffffff;
    padding: 24px;
    display: flex;
    flex-direction: column;
    /* QUITAMOS el gap general y lo manejamos con márgenes */
    /* gap: 30px; */
    height: 100vh;
    flex-shrink: 0;
}

/* Agregamos un margen inferior a las secciones existentes para separarlas */
.menu-section,
.library-section {
    margin-bottom: 30px;
}

.menu-title {
    font-size: 0.8rem;
    color: #888;
    margin-bottom: 15px;
    display: block;
    font-weight: bold;
}

ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

li a {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 10px 15px;
    border-radius: 8px;
    text-decoration: none;
    color: #555;
    font-weight: 500;
    transition: background-color 0.2s, color 0.2s;
}

li.active a {
    background-color: #e3f2fd;
    color: #03a9f4;
}

li a:hover {
    background-color: #f0f0f0;
}

.icon {
    font-style: normal;
}

/* ---------------------------------
   ESTILOS PARA CERRAR SESIÓN 
   ---------------------------------
*/

.logout-section {
    /* Esta es la clave: empuja el elemento al final del contenedor flexbox */
    margin-top: auto;
    padding-top: 24px;
    /* Opcional: agregar un poco de espacio arriba si es necesario */
}

.logout-btn {
    /* Reutilizamos el estilo general de los enlaces del menú */
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 10px 15px;
    border-radius: 8px;
    text-decoration: none;
    color: #d32f2f;
    /* Un color rojo para hacerlo destacar */
    font-weight: 500;
    transition: background-color 0.2s, color 0.2s;
    width: 100%;
    /* Asegura que ocupe todo el ancho para el hover */
}

.logout-btn:hover {
    background-color: #ffebee;
    /* Fondo rojo muy claro al pasar el ratón */
    color: #b71c1c;
}
</style>