/**
 * RStudio Main Application Component
 *
 * This is the root component that handles:
 * - Application routing
 * - State management
 * - IPC communication with Electron
 * - Global error handling
 * - Theme and layout management
 */

import React, { useEffect, useState, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { Box, CircularProgress, Snackbar, Alert, useTheme } from '@mui/material';
import MainLayout from './components/layouts/MainLayout';
import WelcomeScreen from './pages/WelcomeScreen';
import ErrorBoundary from './components/common/ErrorBoundary';
import { setWarp, setLoading, setError, setSuccess, clearError } from './store/warpSlice';
import { Dashboard } from './components/Dashboard/Dashboard';
import { Converter } from './components/Converter/Converter';
import AOS from 'aos';
// import 'aos/dist/aos.css';
// import { useElectron } from './hooks/useElectron';
// import { useFileSystem } from './hooks/useFileSystem';
// import { useHotkeys } from './hooks/useHotkeys';

/**
 * Main Application Component
 */
const App = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const theme = useTheme();

    const { warpdata, loading, error, successMessage } = useSelector((state) => state.warp);
    const [showWelcome, setShowWelcome] = useState(false);
    const [isInitialized, setIsInitialized] = useState(false);

    /**
     * Initialize the application
     */
    useEffect(() => {
        console.log('Initializing Warp Vite project...');
        // Check if we should show welcome screen
        checkWelcomeScreen();
        setIsInitialized(true)
        AOS.init({
            once: false,
            mirror: true,
            duration: 700,
            startEvent: 'DOMContentLoaded',
        });
        setTimeout(() => {
            AOS.refresh();
        }, 300);
        return () => {
            // Cleanup on unmount
            console.log('Cleaning up Warp');
        };
    }, []);

    /**
     * Check if welcome screen should be shown
     */
    const checkWelcomeScreen = useCallback(() => {
        try {
            const hasSeenWelcome = localStorage.getItem('warp-welcome-seen');
            console.log("hasSeenWelcome", hasSeenWelcome)
            setShowWelcome(!hasSeenWelcome);
            // TODO query server for state
        } catch (err) {
            console.error('Failed to check welcome screen status:', err);
            setShowWelcome(true); // Default to showing welcome screen on error
        }
    }, []);

    /**
     * Handle welcome screen completion
     */
    const handleWelcomeComplete = useCallback(() => {
        try {
            // TODO call server to saved the state
            localStorage.setItem('warp-welcome-seen', 'true');
            setShowWelcome(false);
            navigate('/dashboard')
        } catch (err) {
            console.error('Failed to save welcome screen status:', err);
        }
    }, []);

    /**
     * Handle error dismissal
     */
    const handleCloseError = useCallback(() => {
        try {
            dispatch(clearError());
        } catch (err) {
            dispatch(setError(null))
        }
    }, [dispatch]);

    /**
     * Handle success message dismissal
     */
    const handleCloseSuccess = useCallback(() => {
        dispatch(setSuccess(null));
    }, [dispatch]);

    // Set up hotkeys
    // useHotkeys({
    //         'Ctrl+N, Meta+N': (e) => {
    //             e.preventDefault();
    //             handleNewResume();
    //         },
    //         'Ctrl+O, Meta+O': (e) => {
    //             e.preventDefault();
    //             handleOpenResume();
    //         },
    //         'Ctrl+S, Meta+S': (e) => {
    //             e.preventDefault();
    //             handleSaveResume();
    //         },
    //         'Ctrl+E, Meta+E': (e) => {
    //             e.preventDefault();
    //             handleExport('pdf');
    //         }
    //});

    /**
     * Render loading state
     */
    console.log('isInitialized:', isInitialized)
    if (!isInitialized) {
        return (
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    height: '100vh',
                    backgroundColor: theme.palette.background.default
                }}
            >
                <CircularProgress
                    size={60}
                    thickness={4}
                    sx={{ color: 'primary.main' }}
                />
            </Box >
        );
    }

    /**
     * Render the application
     */
    return (
        <ErrorBoundary>
            <MainLayout>
                <Routes>
                    <Route
                        path="/welcome"
                        element={<WelcomeScreen onGetStarted={handleWelcomeComplete} />}
                    />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/documents" element={<Converter />} category='documents' />
                    <Route path="/videos" element={<Converter category='videos' />} />
                    <Route path="/audios" element={<Converter category='audios' />} />\
                    <Route path="/images" element={<Converter />} category='images' />
                    <Route path="/batch" element={<Converter />} category='batch' />
                    <Route
                        path="/"
                        element={showWelcome ?
                            <Navigate to="/welcome" replace /> :
                            <Navigate to="/dashboard" replace />}
                    />
                </Routes>
            </MainLayout>

            {/* Loading indicator */}
            {loading && (
                <Box
                    sx={{
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        right: 0,
                        height: '4px',
                        zIndex: theme.zIndex.snackbar + 1,
                        background: `linear-gradient(90deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.light} 100%)`,
                        animation: 'progress 2s linear infinite'
                    }}
                />
            )}

            {/* Error notification */}
            <Snackbar
                open={!!error}
                autoHideDuration={6000}
                onClose={handleCloseError}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                sx={{ mt: 8 }}
            >
                <Alert
                    onClose={handleCloseError}
                    severity="error"
                    sx={{ width: '100%' }}
                >
                    {error}
                </Alert>
            </Snackbar>

            {/* Success notification */}
            <Snackbar
                open={!!successMessage}
                autoHideDuration={4000}
                onClose={handleCloseSuccess}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                sx={{ mt: 8 }}
            >
                <Alert
                    onClose={handleCloseSuccess}
                    severity="success"
                    sx={{ width: '100%' }}
                >
                    {successMessage}
                </Alert>
            </Snackbar>
        </ErrorBoundary>
    );
};

export default App;
