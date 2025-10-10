# Imagen base
FROM node:22

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias primero
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código
COPY . .

# Exponer puerto de Vite (5173 por defecto)
EXPOSE 5173

# Ejecutar Vite en modo desarrollo
CMD ["npm", "run", "dev", "--", "--host"]
