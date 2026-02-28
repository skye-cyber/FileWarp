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
import { NavbarTop } from '../Navigation/NavbarTop';

/**
 * Main Layout Component
 */
const MainLayout = ({ children }) => {
    const theme = useTheme();
//     const { warpdata } = useSelector((state) => state.warp);
    const [LeftDrawerOpen, setLeftDrawerOpen] = React.useState(false);

    const [EditorPanelWidth, setEditorPanelWidth] = React.useState(400);
    const [RightPanelWidth, setRightPanelWidth] = React.useState(200);

    const [isDraggingEditor, setIsDraggingEditor] = React.useState(false);
    const [isDraggingRight, setIsDraggingRight] = React.useState(false);

    const containerRef = React.useRef(null);
    const EditorDragHandleRef = React.useRef(null);
    const RightDragHandleRef = React.useRef(null);

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
        <div ref={containerRef} className='block w-screen h-screen bg-white dark:bg-blend-900 transition-color duration-500'>
            {/* Top NavBar */}
            <NavbarTop />

            {/* Main Content Area */}
            <div className='w-full h-full overflow-auto'>
                {children}
            </div>

            {/* Status Bar <StatusBar />*/}
        </div>
    );
};

export default MainLayout;
