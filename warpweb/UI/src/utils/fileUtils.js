/**
 * File Utilities
 *
 * Helper functions for file operations and JSON serialization
 */

/**
 * Validate data structure
 * @param {Object} data - data to validate
 * @returns {boolean} True if valid
 */
export const validateFileds = (data = {}, fields = []) => {
    if (!resume || typeof resume !== 'object') return false;

    for (const field of fields) {
        if (!(field in data)) return false;
    }

    return true;
};

/**
 * Serialize data to JSON string
 * @param {Object} data - Data to serialize
 * @returns {string} JSON string
 */
export const serializeWarpdata = (data) => {
    try {
        // Clean up any circular references or non-serializable data
        // const cleanData= cleanDataForSerialization(data);
        return JSON.stringify(data, null, 2);
    } catch (error) {
        console.error('Serialization error:', error);
        throw new Error('Failed to serialize data');
    }
};

/**
 * Deserialize JSON string to object
 * @param {string} json - JSON string
 * @returns {Object} Serialized data
 */
export const deserializeWarpdata = (json) => {
    try {
        const parsed = JSON.parse(json);

        return parsed;
    } catch (error) {
        console.error('Deserialization error:', error);
        throw new Error('Failed to deserialize data');
    }
};

/**
 * Create backup of given data
 * @param {Object} data - Current data to backup
 * @returns {Object} Backup object
 */
export const createWarpdataBackup = (data) => {
    return {
        timestamp: new Date().toISOString(),
        warpdata: data,
        version: '1.0'
    };
};

/**
 * Restore Warpdata from backup
 * @param {Object} backup - Backup object
 * @returns {Object} Restored Warpdata
 */
export const restoreFromBackup = (backup) => {
    if (!backup || !backup.warpdata) {
        throw new Error('Invalid backup format');
    }

    return backup.warpdata;
};
