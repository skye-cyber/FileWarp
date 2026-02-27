/**
 * Error Boundary Component
 *
 * This component catches JavaScript errors anywhere in the component tree,
 * logs those errors, and displays a fallback UI.
 *
 * @module ErrorBoundary
 */

import React, { Component } from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import { Warning, Refresh } from '@mui/icons-material';

/**
 * Error Boundary Component
 */
class ErrorBoundary extends Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
    }

    static getDerivedStateFromError(error) {
        // Update state so the next render will show the fallback UI
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        // Log the error to an error reporting service
        console.error('ErrorBoundary caught an error:', error, errorInfo);
        this.setState({ error, errorInfo });
    }

    handleReload = () => {
        window.location.reload();
    };

    render() {
        if (this.state.hasError) {
            // Fallback UI when an error occurs
            return (
                <Box
                    sx={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        minHeight: '100vh',
                        backgroundColor: 'background.default',
                        p: 4
                    }}
                >
                    <Paper
                        elevation={3}
                        sx={{
                            p: 4,
                            maxWidth: 600,
                            width: '100%',
                            textAlign: 'center'
                        }}
                    >
                        <Box mb={2} color="error.main">
                            <Warning sx={{ fontSize: 60 }} />
                        </Box>

                        <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
                            Oops! Something went wrong
                        </Typography>

                        <Typography variant="body1" paragraph sx={{ mt: 2, mb: 3 }}>
                            We encountered an unexpected error while running FileWarp.
                            Don't worry, your data is safe.
                        </Typography>

                        <Box mb={3} textAlign="left" sx={{ backgroundColor: 'action.hover', p: 2, borderRadius: 1 }}>
                            <Typography variant="caption" color="text.secondary" paragraph>
                                <strong>Error:</strong> {this.state.error?.message || 'Unknown error'}
                            </Typography>
                            {this.state.errorInfo?.componentStack && (
                                <Typography variant="caption" color="text.secondary">
                                    <strong>Component:</strong> {this.state.errorInfo.componentStack.split('\n')[1]}
                                </Typography>
                            )}
                        </Box>

                        <Button
                            variant="contained"
                            color="primary"
                            startIcon={<Refresh />}
                            onClick={this.handleReload}
                            sx={{ mr: 2 }}
                        >
                            Reload Application
                        </Button>

                        <Button
                            variant="outlined"
                            onClick={() => {
                                if (window.rstudio) {
                                    window.rstudio.window.close();
                                }
                            }}
                        >
                            Close Application
                        </Button>
                    </Paper>
                </Box>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
