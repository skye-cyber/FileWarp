/**
 * Redux Store Configuration
 *
 * Centralized state management for RStudio using Redux Toolkit
 */

import { configureStore } from '@reduxjs/toolkit';
import warpReducer from './warpSlice';
import { loadState, saveState } from '../utils/localStorage';

/**
 * Configure and create the Redux store
 */
export const store = configureStore({
    reducer: {
        warp: warpReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                // Ignore specific action types that might have non-serializable data
                //ignoredActions: ['warp/setWarpdata', 'warp/updateWarpData'],
                // Ignore specific paths in the state
                //ignoredPaths: ['warp.data.metadata.created', 'warp.data.metadata.lastUpdated'],
            },
        }),
    devTools: import.meta.env.DEV || process.env.NODE_ENV !== 'production',
    preloadedState: loadState(),
});

// Save store state to localStorage whenever it changes
store.subscribe(() => {
    saveState(store.getState());
});

// Export the store for use in the application
export default store;
