/**
 * Local Storage Utilities
 *
 * Helper functions for managing localStorage with error handling
 */

/**
 * Save state to localStorage
 * @param {Object} state - The state to save
 */
export const saveState = (state) => {
    try {
        const serializedState = JSON.stringify(state);
        localStorage.setItem('warpstate', serializedState);

        // Also save just the resume data separately for easy access
        if (state.warp) {
            const serializedWarpdata = JSON.stringify(state.warp);
            localStorage.setItem('warpstate', serializedWarpdata);
        }
    } catch (err) {
        console.error('Could not save state to localStorage:', err);
    }
};

/**
 * Load state from localStorage
 * @returns {Object|null} The loaded state or null if failed
 */
export const loadState = () => {
    try {
        const serializedState = localStorage.getItem('warpstate');
        if (serializedState === null) {
            return undefined;
        }
        return JSON.parse(serializedState);
    } catch (err) {
        console.error('Could not load state from localStorage:', err);
        return undefined;
    }
};

/**
 * Clear state from localStorage
 */
export const clearState = () => {
    try {
        localStorage.removeItem('warpstate');
        localStorage.removeItem('warpstate');
    } catch (err) {
        console.error('Could not clear state from localStorage:', err);
    }
};

/**
 * Save warpdata to localStorage
 * @param {Object} resume - The resume data to save
 */
export const saveWarpdata = (warpdata) => {
    try {
        const serializedWarpdata = JSON.stringify(warpdata);
        localStorage.setItem('warpdata', serializedWarpdata);
        localStorage.setItem('warpdata-last-save', new Date().toISOString());
    } catch (err) {
        console.error('Could not save warpdata to localStorage:', err);
    }
};

/**
 * Load warpdata from localStorage
 * @returns {Object|null} The loaded resume or null if failed
 */
export const loadWarpdata = () => {
    try {
        const serializedWarpdata = localStorage.getItem('warpdata');
        if (serializedWarpdata === null) {
            return null;
        }
        return JSON.parse(serializedWarpdata);
    } catch (err) {
        console.error('Could not load warpdata from localStorage:', err);
        return null;
    }
};

/**
 * Get last save timestamp
 * @returns {string|null} ISO timestamp or null
 */
export const getLastSaveTime = () => {
    try {
        return localStorage.getItem('warpdata-last-save');
    } catch (err) {
        console.error('Could not get last save time:', err);
        return null;
    }
};
