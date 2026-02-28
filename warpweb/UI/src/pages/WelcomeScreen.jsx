/**
 * Welcome Screen Component
 *
 * This component provides the initial welcome screen for new users
 * with options to create a new resume or open an existing one.
 *
 * @module WelcomeScreen
 */

import React from 'react';
import { Box, Typography, Button, Paper, Grid } from '@mui/material';
import { AddCircleOutline } from '@mui/icons-material';
import { useTheme } from '@emotion/react';
/**
 * Welcome Screen Component
 * @param {Object} props - Component props
 * @param {Function} props.onGetStarted - Callback for get started action
 * @param {Function} props.onOpenResume - Callback for open resume action
 */
const WelcomeScreen = ({ onGetStarted }) => {
    const theme = useTheme();
    return (
        <Box
            sx={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                minHeight: '100vh',
                background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
                p: 4
            }}
        >
            <Paper
                elevation={6}
                sx={{
                    p: 6,
                    maxWidth: 800,
                    width: '100%',
                    textAlign: 'center',
                    borderRadius: 3
                }}
            >
                <Box mb={4}>
                    <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
                        Welcome to FileWarp
                    </Typography>
                    <Typography variant="h5" color="text.secondary" paragraph>
                        State of the art file Toolkit
                    </Typography>
                </Box>

                <Box mb={6}>
                    <Typography variant="body1" paragraph>
                        FileWarp gives you complete control over file operations, be it conversion, manipulation etc.
                    </Typography>
                    <Typography variant="body1" paragraph>
                        Handle file operations with ease.
                    </Typography>
                </Box>

                <Grid container spacing={3} justifyContent="center">
                    <Grid item>
                        <Button
                            variant="contained"
                            color="primary"
                            size="large"
                            startIcon={<AddCircleOutline />}
                            onClick={onGetStarted}
                            sx={{ minWidth: 200, py: 1.5 }}
                        >
                            Get Started
                        </Button>
                    </Grid>
                </Grid>

                <Box mt={4} pt={2} borderTop="1px solid #eee">
                    <Typography variant="body2" color="text.secondary">
                        Need help? Check out our <a href="#" className='hover:underline' style={{ color: theme.palette.primary.main }}>documentation</a>
                    </Typography>
                </Box>
            </Paper>
        </Box>
    );
};

export default WelcomeScreen;
