/**
 * Warp Slice
 *
 * Redux slice for managing warpdata data and application state
 */

import { createSlice } from '@reduxjs/toolkit';

/**
 * Initial state for the warpdata slice
 */
const initialState = {
    warpdata: {},
    loading: false,
    error: null,
    successMessage: null,
    activeTool: {category: 'dashboard', id: 1, name: 'Dashboard'},
    ui: {
        activeTab: 'dashboard',
        panelWidth: 350,
        isDragging: false,
        zoomLevel: 100,
    }
};

/**
 * Create the warp slice
 */
export const warpSlice = createSlice({
    name: 'warp',
    initialState,
    reducers: {
        /**
         * Set the current warpdata
         * @param {WarpState} state - Current state
         * @param {Object} action - Redux action
         * @param {Object} action.payload - warpdata to set
         */
        setWarpdata: (state, action) => {
            state.warpdata = action.payload;
            state.error = null;
        },

        /**
         * Update Warpdata partially
         * @param {WarpState} state - Current state
         * @param {Object} action - Redux action
         * @param {Object} action.payload - Partial Warpdata to update
         */
        updateWarpdata: (state, action) => {
            state.warpdata = { ...state.warpdata, ...action.payload };
        },

        /**
         * Reset to empty Warpdata
         * @param {WarpState} state - Current state
         */
        resetWarpdata: (state) => {
            state.warpdata = {};
            state.error = null;
            state.successMessage = 'FileWarp initialized';
        },

        // UI State management
        setActiveTab: (state, action) => {
            state.ui.activeTab = action.payload;
        },

        setActiveTool: (state, action) => {
            state.activeTool = action.payload;
        },

        setPanelWidth: (state, action) => {
            state.ui.panelWidth = action.payload;
        },

        setIsDragging: (state, action) => {
            state.ui.isDragging = action.payload;
        },

        setZoomLevel: (state, action) => {
            state.ui.zoomLevel = action.payload;
        },

        /**
         * Set loading state
         * @param {WarpState} state - Current state
         * @param {Object} action - Redux action
         * @param {boolean} action.payload - Loading state to set
         */
        setLoading: (state, action) => {
            state.loading = action.payload;
        },

        /**
         * Set error message
         * @param {WarpState} state - Current state
         * @param {Object} action - Redux action
         * @param {string|null} action.payload - Error message to set
         */
        setError: (state, action) => {
            state.error = action.payload;
            state.loading = false;
        },
        /**
         * Clear error message
         * @param {WarpState} state - Current state
         */
        clearError: (state) => {
            state.error = null;
        },
        /**
         * Set success message
         * @param {WarpState} state - Current state
         * @param {Object} action - Redux action
         * @param {string|null} action.payload - Success message to set
         */
        setSuccess: (state, action) => {
            state.successMessage = action.payload;
            state.loading = false;
        },

        /**
         * Clear success message
         * @param {WarpState} state - Current state
         */
        clearSuccess: (state) => {
            state.successMessage = null;
        }
    },
});

// Export actions
export const {
    setWarp,
    updateWarp,
    setLoading,
    setError,
    clearError,
    setSuccess,
    clearSuccess,
    resetWarp,
    setActiveTab,
    setActiveTool,
    setPanelWidth,
    setIsDragging,
    setZoomLevel
} = warpSlice.actions;

const warpReducer = warpSlice.reducer;
export default warpReducer
