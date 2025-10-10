import axios from 'axios'

// Crear instancia de Axios
const api = axios.create({
    baseURL: 'https://api.kyeroradio.com/api/',
    headers: {
        'Content-Type': 'application/json'
    }
})

// Función para obtener tokens del localStorage
const getTokens = () => {
    const stored = localStorage.getItem('auth_tokens')
    return stored ? JSON.parse(stored) : null
}

// Interceptor de petición: agregar access token
api.interceptors.request.use(config => {
    const tokens = getTokens()
    if (tokens && tokens.access) {
        config.headers['Authorization'] = `Bearer ${tokens.access}`
    }
    return config
})

// Interceptor de respuesta: renovar access token si expira
api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config

        // Si es 401 y no es ya un retry
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            const tokens = getTokens()
            if (tokens && tokens.refresh) {
                try {
                    const response = await axios.post('http://localhost:8000/api/login/token/refresh/', {
                        refresh: tokens.refresh
                    })

                    // Guardar nuevo access token en localStorage
                    const newTokens = {
                        access: response.data.access,
                        refresh: tokens.refresh // refresco sigue igual
                    }
                    localStorage.setItem('auth_tokens', JSON.stringify(newTokens))

                    // Actualizar header del request original y reintentar
                    originalRequest.headers['Authorization'] = `Bearer ${newTokens.access}`
                    return api(originalRequest)
                } catch (err) {
                    // Refresh token expiró o inválido
                    localStorage.removeItem('auth_tokens')
                    window.location.href = '/login' // redirigir al login
                    return Promise.reject(err)
                }
            } else {
                // No hay refresh token, redirigir al login
                window.location.href = '/login'
            }
        }

        return Promise.reject(error)
    }
)

export default api
