import React from "react";

export const Footer = ({ }) => {
    return (
        <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-12">
            <div className="max-w-7xl mx-auto py-6 px-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div>
                        <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Filemac</h3>
                        <p className="text-gray-600 dark:text-gray-400">
                            Comprehensive file management suite with conversion, analysis, and processing tools.
                        </p>
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Tools</h3>
                        <div className="grid grid-cols-2 gap-2 text-sm">
                            <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400">Document Converter</a>
                            <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400">Audio Effects</a>
                            <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400">Video Analysis</a>
                            <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400">Image Processing</a>
                        </div>
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Support</h3>
                        <div className="space-y-2 text-sm">
                            <p className="text-gray-600 dark:text-gray-400">Help & Documentation</p>
                            <p className="text-gray-600 dark:text-gray-400">Contact Support</p>
                        </div>
                    </div>
                </div>
                <div className="border-t border-gray-200 dark:border-gray-600 mt-6 pt-6 text-center">
                    <p className="text-gray-500 dark:text-gray-400">
                        &copy; 2025 Warp. All rights reserved. Version 1.1.7
                    </p>
                </div>
            </div>
        </footer>
    )
}
