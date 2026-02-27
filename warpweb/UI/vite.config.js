import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
// import { visualizer } from 'rollup-plugin-visualizer'
// import tailwindcss from '@tailwindcss/vite'


// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        react(),
        // Uncomment for bundle analysis
        // visualizer({ open: true })
        // tailwindcss(),
    ],

    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
            '@components': path.resolve(__dirname, './src/components'),
            '@pages': path.resolve(__dirname, './src/pages'),
            '@styles': path.resolve(__dirname, './src/styles'),
            '@utils': path.resolve(__dirname, './src/utils'),
            '@hooks': path.resolve(__dirname, './src/hooks'),
            // '@contexts': path.resolve(__dirname, './src/contexts'),
            // '@templates': path.resolve(__dirname, './src/templates'),
            // '@schema': path.resolve(__dirname, './schema')
        }
    },

    base: './',

    build: {
        outDir: 'build',
        emptyOutDir: true,
        rollupOptions: {
            output: {
                manualChunks: {
                    vendor: ['react', 'react-dom', 'react-router-dom'],
                    mui: ['@mui/material', '@mui/icons-material'],
                    redux: ['@reduxjs/toolkit', 'react-redux']
                }
            }
        }
    },

    server: {
        port: 3000,
        open: false,
        proxy: {
            '/api': {
                target: 'http://localhost:8008',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '')
            }
        }
    },

    css: {
        preprocessorOptions: {
            scss: {
                additionalData: `@import "@styles/variables.scss";@import "@styles/mixins.scss";`
            }
        }
    },

    define: {
        'process.env': {}, //process.env,
        global: 'window'
    },

    optimizeDeps: {
        include: [
            '@mui/material',
            '@mui/icons-material',
            '@emotion/react',
            '@emotion/styled',
            '@reduxjs/toolkit',
            'react-redux'
        ]
    }
})
