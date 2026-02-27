/**
* WarpWeb Main Entry Point
    *
* This is the main entry point for the Vite - powered React application.
* It sets up the React app, Redux store, and global providers.
*/

import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { BrowserRouter as Router } from 'react-router-dom';
import App from './App';
import store from './store';
import './styles/global.css';
// import './styles/normalize.css';

/**
 * Main Application Component with all providers
 */
const Root = () => {
    const theme = createTheme({
        palette: {
            mode: 'light',
            primary: {
                main: '#1976d2',
                light: '#42a5f5',
                dark: '#1565c0',
                contrastText: '#ffffff',
                range: {
                    50: "#eff6ff",
                    100: "#dbeafe",
                    200: "#bfdbfe",
                    300: "#93c5fd",
                    400: "#60a5fa",
                    500: "#3b82f6",
                    600: "#2563eb",
                    700: "#1d4ed8",
                    800: "#1e40af",
                    900: "#1e3a8a",
                },
            },
            secondary: {
                main: '#9c27b0',
                light: '#ba68c8',
                dark: '#7b1fa2',
                contrastText: '#ffffff',
            },
            background: {
                default: '#f5f5f5',
                    paper: '#ffffff',
            },
            error: {
                main: '#d32f2f',
            },
            warning: {
                main: '#ed6c02',
            },
            info: {
                main: '#0288d1',
            },
            success: {
                main: '#2e7d32',
            },
            text: {
                primary: '#212121',
                secondary: '#757575',
                disabled: '#bdbdbd',
            },
        },
        typography: {
            fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
            h1: {
                fontSize: '2.5rem',
                fontWeight: 500,
                lineHeight: 1.2,
            },
            h2: {
                fontSize: '2rem',
                fontWeight: 500,
                lineHeight: 1.3,
            },
            h3: {
                fontSize: '1.75rem',
                fontWeight: 500,
                lineHeight: 1.3,
            },
            h4: {
                fontSize: '1.5rem',
                fontWeight: 500,
                lineHeight: 1.3,
            },
            h5: {
                fontSize: '1.25rem',
                fontWeight: 500,
                lineHeight: 1.3,
            },
            h6: {
                fontSize: '1.1rem',
                fontWeight: 500,
                lineHeight: 1.3,
            },
            body1: {
                fontSize: '1rem',
                lineHeight: 1.5,
            },
            body2: {
                fontSize: '0.875rem',
                lineHeight: 1.43,
            },
            button: {
                textTransform: 'none',
                fontWeight: 500,
            },
        },
        components: {
            MuiButton: {
                styleOverrides: {
                    root: {
                        borderRadius: 8,
                        padding: '8px 16px',
                        textTransform: 'none',
                    },
                },
            },
            MuiCard: {
                styleOverrides: {
                    root: {
                        borderRadius: 12,
                        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
                    },
                },
            },
            MuiPaper: {
                styleOverrides: {
                    root: {
                        borderRadius: 8,
                    },
                },
            },
            MuiTextField: {
                styleOverrides: {
                    root: {
                        '& .MuiOutlinedInput-root': {
                            borderRadius: 6,
                        },
                    },
                },
            },
        },
        shape: {
            borderRadius: 8,
        },
        transitions: {
            duration: {
                shortest: 150,
                shorter: 200,
                short: 250,
                standard: 300,
                complex: 375,
                enteringScreen: 225,
                leavingScreen: 195,
            },
        },
    });


    return (
        <React.StrictMode>
            <Provider store={store}>
                <ThemeProvider theme={theme}>
                    <CssBaseline />
                    <Router>
                        <App />
                    </Router>
                </ThemeProvider>
            </Provider>
        </React.StrictMode>
    );
};

// Create root and render the application
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Root />);

// Expose global variables for debugging in development
if (import.meta.env.DEV) {
    window.store = store;
    console.log('Warp Vite project initialized in development mode');
} else {
    console.log('Warp Vite project initialized in production mode');
}

export default Root;
