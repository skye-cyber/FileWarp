/**
 * Main Layout Component
 *
 * This component provides the main application layout with:
 * - Top toolbar
 * - Split-screen editor and preview
 * - Status bar
 *
 * @module MainLayout
 */

import React from 'react';
import { useSelector } from 'react-redux';
import { Box, Drawer, Divider, useTheme, Typography, Button, Chip, Grid } from '@mui/material';
import { Save, Add, PictureAsPdf, Description, Code, ContentCopy, Refresh, Palette } from '@mui/icons-material';
import TopToolbar from '../toolbars/TopToolbar';
import EditorPanel from '../editor/EditorPanel';
import PreviewPanel from '../preview/PreviewPanel';
import StatusBar from '../toolbars/status/StatusBar';
import { ResumeDraftItem } from '../Draft/ResumeDraft';
import { TemplatePreview } from '../preview/TemplatePreview';
import { TEMPLATES } from '../../../schema/resume.schema';
import { StateManager } from '../syscore/StatesManager';

/**
 * Main Layout Component
 */
const MainLayout = () => {
    const theme = useTheme();
    const { resume } = useSelector((state) => state.resume);
    const [LeftDrawerOpen, setLeftDrawerOpen] = React.useState(false);
    const [RightDrawerOpen, setRightDrawerOpen] = React.useState(false);

    const [EditorPanelWidth, setEditorPanelWidth] = React.useState(400);
    const [RightPanelWidth, setRightPanelWidth] = React.useState(200);

    const [isDraggingEditor, setIsDraggingEditor] = React.useState(false);
    const [isDraggingRight, setIsDraggingRight] = React.useState(false);

    const containerRef = React.useRef(null);
    const EditorDragHandleRef = React.useRef(null);
    const RightDragHandleRef = React.useRef(null);

    const [resumeDrafts, setResumeDrafts] = React.useState([])

    /**
     * Handle mouse down for panel resizing
     */
    const handleEditorMouseDown = (e) => {
        setIsDraggingEditor(true);
        e.preventDefault();
    };

    /**
     * Handle mouse down for panel resizing
     */
    const handleRightMouseDown = (e) => {
        setIsDraggingRight(true);
        e.preventDefault();
    };

    /**
     * Handle mouse move for panel resizing
     */
    const handleMouseMove = (e) => {
        if (isDraggingEditor) {
            const containerRect = containerRef.current.getBoundingClientRect();
            const newWidth = e.clientX - containerRect.left;

            // Constrain width between 300px and 600px
            if (newWidth >= 270 && newWidth <= 350) {
                setEditorPanelWidth(newWidth);
            }
        } else if (isDraggingRight) {
            const containerRect = containerRef.current.getBoundingClientRect();
            const newWidth = containerRect.right - e.clientX;
            //             console.log("New width:", newWidth)

            // Constrain width between 300px and 600px
            if (newWidth >= 240 && newWidth <= 250) {
                setRightPanelWidth(newWidth);
            }
        }
    };

    /**
     * Handle mouse up for panel resizing
     */
    const handleMouseUp = () => {
        setIsDraggingEditor(false);
        setIsDraggingRight(false);
    };

    /**
     * Set up event listeners for dragging
     */
    React.useEffect(() => {
        if (isDraggingEditor || isDraggingRight) {
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
            document.body.style.cursor = 'col-resize';
        } else {
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
            document.body.style.cursor = '';
        }

        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
            document.body.style.cursor = '';
        };
    }, [isDraggingEditor, isDraggingRight]);

    return (
        <Box
            ref={containerRef}
            sx={{
                display: 'flex',
                flexDirection: 'column',
                height: '100vh',
                overflow: 'hidden',
                backgroundColor: theme.palette.background.default
            }}
        >
            {/* Top Toolbar */}
            <TopToolbar
                onMenuClick={() => setLeftDrawerOpen(true)}
                onRightSettingsToggle={() => setRightDrawerOpen(true)}
                resumeTitle='Untitled Resume'
            />

            {/* Main Content Area */}
            <Box sx={{
                display: 'flex',
                flex: 1,
                overflow: 'hidden',
                position: 'relative'
            }}>
                {/* Editor Panel (Left) */}
                <Box
                    sx={{
                        width: `${EditorPanelWidth}px`,
                        minWidth: 270,
                        maxWidth: 350,
                        height: '100%',
                        overflow: 'auto',
                        borderRight: `1px solid ${theme.palette.divider}`,
                        transition: 'width 0.2s ease'
                    }}
                >
                    <EditorPanel />
                </Box>

                {/* Left Resize Handle */}
                <Box
                    ref={EditorDragHandleRef}
                    onMouseDown={handleEditorMouseDown}
                    sx={{
                        width: '8px',
                        height: '100%',
                        cursor: 'col-resize',
                        backgroundColor: isDraggingEditor ? theme.palette.primary.main : 'transparent',
                        '&:hover': {
                            backgroundColor: theme.palette.action.hover,
                        },
                        transition: 'background-color 0.2s ease',
                        zIndex: 2
                    }}
                />

                {/* Preview Panel (Right) */}
                <Box
                    sx={{
                        flex: 1,
                        height: '100%',
                        overflow: 'auto',
                        backgroundColor: theme.palette.background.paper
                    }}
                >
                    <PreviewPanel />
                </Box>

                {/* Right Resize Handle */}
                <Box
                    ref={RightDragHandleRef}
                    onMouseDown={handleRightMouseDown}
                    sx={{
                        display:  {sm: 'none', lg: 'block'},
                        width: '8px',
                        height: '100%',
                        cursor: 'col-resize',
                        backgroundColor: isDraggingRight ? theme.palette.primary.main : 'transparent',
                        '&:hover': {
                            backgroundColor: theme.palette.action.hover,
                        },
                        transition: 'background-color 0.2s ease',
                        zIndex: 2
                    }}
                />

                {/* Right Template Panel */}
                <Box
                    sx={{
                        overflowX: 'hidden',
                        display:  {sm: 'none', lg: 'block'},
                        justifyContent:'center',
                        borderColor: '#737373',
                        width: `${RightPanelWidth}px`,
                        minWidth: 240,
                        maxWidth: 250,
                        height: '100%',
                        borderLeft: `2px solid ${theme.palette.divider}`,
                        transition: 'width 0.2s ease'
                    }}
                >
                    {
                        TEMPLATES.map((Template, index) => <TemplatePreview key={index} templateId={Template.id} />)
                    }
                </Box>
            </Box>

            {/* Status Bar */}
            <StatusBar />

            {/* Settings Drawer: Left - Template Drafts */}
            <Drawer
                anchor="left"
                open={LeftDrawerOpen}
                onClose={() => setLeftDrawerOpen(false)}
                sx={{
                    '& .MuiDrawer-paper': {
                        width: 340,
                    }
                }}
            >
                <Box sx={{ p: 2, width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Typography variant="h6">Template Drafts</Typography>
                        <Chip
                            label={`0 drafts`}
                            size="small"
                            color="primary"
                        />
                    </Box>

                    <Divider sx={{ my: 1 }} />

                    {/* Drafts list */}
                    <Box sx={{ flex: 1, overflow: 'auto', mb: 2 }}>
                        {resumeDrafts?.rslist?.length > 0 ? (
                            resumeDrafts.rslist.map((item, index) => (
                                <ResumeDraftItem key={item.id || index} data={item} />
                            ))
                        ) : (
                            <Box sx={{
                                textAlign: 'center',
                                py: 4
                                ,
                                color: 'text.secondary'
                            }}>
                                <Typography variant="body2">
                                    No template drafts found
                                </Typography>
                                <Typography variant="caption">
                                    Create your first resume to see drafts here
                                </Typography>
                            </Box>
                        )}
                    </Box>

                    <Divider sx={{ my: 1 }} />

                    {/* Draft actions */}
                    <Box sx={{ display: 'flex', gap: 0 }}>
                        <Button
                            className="mr-2"
                            variant="outlined"
                            fullWidth
                            startIcon={<Save />}
                            onClick={() => {}}
                        >
                            Save Current
                        </Button>
                        <Button
                            className="p-0"
                            variant="contained"
                            fullWidth
                            startIcon={<Add />}
                            onClick={() => {}}
                        >
                            New Draft
                        </Button>
                    </Box>
                </Box>
            </Drawer>

            {/* Right Drawer - Quick Tools */}
            <Drawer
                anchor="right"
                open={RightDrawerOpen}
                onClose={() => setRightDrawerOpen(false)}
                sx={{
                    '& .MuiDrawer-paper': {
                        width: 320,
                    }
                }}
            >
                <Box sx={{ p: 2, width: 320, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <Typography variant="h6" sx={{ mb: 2 }}>
                        Quick Tools & Actions
                    </Typography>

                    <Divider sx={{ my: 1 }} />

                    {/* Quick Export Section */}
                    <Box sx={{ mb: 3 }}>
                        <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'medium' }}>
                            Quick Export
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                            <Button
                                variant="outlined"
                                size="small"
                                startIcon={<PictureAsPdf />}
                                onClick={() => {
                                    // Trigger PDF export
                                    const exportData = StateManager.get('exportData');
                                    if (exportData) {
                                        StateManager.get('handleExport')('pdf');
                                    }
                                }}
                                disabled={!resume.personalInfo.firstName}
                            >
                                PDF
                            </Button>
                            <Button
                                variant="outlined"
                                size="small"
                                startIcon={<Description />}
                                onClick={() => {
                                    // Trigger DOCX export
                                    const exportData = StateManager.get('exportData');
                                    if (exportData) {
                                        StateManager.get('handleExport')('docx');
                                    }
                                }}
                                disabled={!resume.personalInfo.firstName}
                            >
                                DOCX
                            </Button>
                            <Button
                                variant="outlined"
                                size="small"
                                startIcon={<Code />}
                                onClick={() => {
                                    // Trigger JSON export
                                    const exportData = StateManager.get('exportData');
                                    if (exportData) {
                                        StateManager.get('handleExport')('json');
                                    }
                                }}
                                disabled={!resume.personalInfo.firstName}
                            >
                                JSON
                            </Button>
                        </Box>
                    </Box>

                    <Divider sx={{ my: 2 }} />

                    {/* Template Quick Select */}
                    <Box sx={{ mb: 3 }}>
                        <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'medium' }}>
                            Quick Template Switch
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                            {TEMPLATES.slice(0, 4).map((template) => (
                                <Chip
                                    key={template.id}
                                    label={template.name}
                                    onClick={(e) => {
                                        const event = { target: { value: template.id } };
                                        document.dispatchEvent(new CustomEvent('templateChange', { detail: { event: event } }));
                                        setRightDrawerOpen(false);
                                    }}
                                    color="primary"
                                    variant="outlined"
                                    size="small"
                                />
                            ))}
                        </Box>
                    </Box>

                    <Divider sx={{ my: 2 }} />

                    {/* Quick Actions */}
                    <Box sx={{ mb: 3 }}>
                        <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'medium' }}>
                            Quick Actions
                        </Typography>
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                            <Button
                                variant="text"
                                size="small"
                                startIcon={<ContentCopy />}
                                onClick={() => {
                                    // Copy resume to clipboard
                                    if (window.rstudio) {
                                        window.rstudio.api.copy_resume(resume);
                                    }
                                }}
                                disabled={!resume.personalInfo.firstName}
                            >
                                Copy Resume Data
                            </Button>
                            <Button
                                variant="text"
                                size="small"
                                startIcon={<Refresh />}
                                onClick={() => {
                                    // Reset resume
                                    if (window.confirm('Are you sure you want to reset this resume?')) {
                                        if (window.rstudio) {
                                            window.rstudio.api.reset_resume();
                                        }
                                    }
                                }}
                            >
                                Reset Resume
                            </Button>
                            <Button
                                variant="text"
                                size="small"
                                startIcon={<Palette />}
                                onClick={() => {
                                    // Toggle ATS mode
                                    const currentSettings = StateManager.get('exportSettings') || {};
                                    document.dispatchEvent(new CustomEvent('toggleATSMode', {
                                        detail: { atsMode: !currentSettings.atsMode }
                                    }));
                                }}
                            >
                                Toggle ATS Mode
                            </Button>
                        </Box>
                    </Box>

                    <Divider sx={{ my: 2 }} />

                    {/* Resume Stats */}
                    <Box sx={{ mb: 3 }}>
                        <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'medium' }}>
                            Resume Statistics
                        </Typography>
                        <Grid container spacing={1}>
                            <Grid item xs={6}>
                                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                                    <strong>Experience:</strong> {resume.experience?.length || 0}
                                </Typography>
                            </Grid>
                            <Grid item xs={6}>
                                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                                    <strong>Skills:</strong> {resume.skills?.length || 0}
                                </Typography>
                            </Grid>
                            <Grid item xs={6}>
                                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                                    <strong>Projects:</strong> {resume.projects?.length || 0}
                                </Typography>
                            </Grid>
                            <Grid item xs={6}>
                                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                                    <strong>Certifications:</strong> {resume.certifications?.length || 0}
                                </Typography>
                            </Grid>
                        </Grid>
                    </Box>

                    <Divider sx={{ my: 2 }} />

                    {/* Template Info */}
                    <Box sx={{ flex: 1, overflow: 'auto' }}>
                        <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'medium' }}>
                            Current Template Info
                        </Typography>
                        <Box sx={{ p: 1, backgroundColor: 'action.hover', borderRadius: 1 }}>
                            <Typography variant="body2" sx={{ fontWeight: 'medium', mb: 1 }}>
                                {TEMPLATES.find(t => t.id === (StateManager.get('template') || 'modern'))?.name || 'Modern'}
                            </Typography>
                            <Typography variant="caption" sx={{ color: 'text.secondary', lineHeight: 1.4 }}>
                                {TEMPLATES.find(t => t.id === (StateManager.get('template') || 'modern'))?.description || 'Clean, contemporary design'}
                            </Typography>
                        </Box>
                    </Box>
                </Box>
            </Drawer>
        </Box>
    );
};

export default MainLayout;
