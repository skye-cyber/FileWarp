// result_utils
import React, { useState } from "react"
import { Navigate, useNavigate } from 'react-router-dom';

export const Result = ({ results = [] }) => {
    const [aos_result_delay, set_aos_result_delay] = useState(300)
    const navigate = useNavigate();

    const PreviewFile = () => {
        console.log("Previewing file")
    }

    const CloseFilePreview = () => {
        console.log("Clsing file preview")
    }

    const ResultItem = (result) => {
        set_aos_result_delay(aos_result_delay + 100)
        return (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 overflow-hidden" data-aos="fade-up" data-aos-delay={aos_result_delay}>
                <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                    <div className="flex items-center justify-between mb-2">
                        <span className={`text-xs font-medium px-2 py-1 rounded ${result.status === 'success'
                            ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                            : "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"}`}>
                            {result.status}
                        </span>
                        <span className="text-xs text-gray-500">{result.size}</span>
                    </div>
                    <div className="flex items-center">
                        <i className="fas fa-file text-gray-400 mr-2"></i>
                        <span className="text-sm font-medium truncate">{result.original_name}</span>
                    </div>
                </div>

                <div className="p-4 bg-gray-50 dark:bg-gray-700">
                    <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-600 dark:text-gray-400">Original</span>
                        <i className="fas fa-arrow-right text-gray-400 mx-2"></i>
                        <span className="text-gray-600 dark:text-gray-400">Converted</span>
                    </div>
                    <div className="flex items-center justify-between mt-2">
                        <span className="text-xs text-gray-500">{result.original_format}</span>
                        <span className="text-xs text-green-600 font-medium">{result.target_format}</span>
                    </div>
                </div>

                <div className="p-4">
                    <div className="flex space-x-2">
                        <a href={result.download_url}
                            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-center py-2 rounded text-sm transition-colors">
                            <i className="fas fa-download mr-1"></i>Download
                        </a>
                        <button onClick={() => PreviewFile(result.preview_url)}
                            className="px-3 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded text-sm hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors">
                            <i className="fas fa-eye"></i>
                        </button>
                    </div>
                </div>
            </div>
        )
    }

    const DownloadAll = () => {
        // TODO Local so should just point to file path/location in system
        console.log("Downloading all files")
    }

    return (
        <section>
            <div className="max-w-6xl mx-auto py-6 sm:px-6 lg:px-8">
                {/* Results Header */}
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 mb-6" data-aos="fade-up">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center">
                            <div className="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mr-4">
                                <i className="fas fa-check text-2xl text-green-600 dark:text-green-400"></i>
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Processing Complete!</h1>
                                <p className="text-gray-600 dark:text-gray-400">{results.length | 0} files processed successfully</p>
                            </div>
                        </div>
                        <div className="flex space-x-3">
                            <button onClick={DownloadAll} className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg transition-colors">
                                <i className="fas fa-download mr-2"></i>Download All
                            </button>
                            <button onClick={() => navigate("/dashboard")} className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors">
                                <i className="fas fa-plus mr-2"></i>New Conversion
                            </button>
                        </div>
                    </div>
                </div>

                {/* Results Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                    {results &&
                        results.map((key, result) => {
                            return <ResultItem key={key} result={result} />
                        })
                    }
                </div>

                {/* Processing Summary */}
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6" data-aos="fade-up">
                    <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Processing Summary</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                        <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                            <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">{results.length}</p>
                            <p className="text-sm text-gray-600 dark:text-gray-400">Total Files</p>
                        </div>
                        <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                            <p className="text-2xl font-bold text-green-600 dark:text-green-400">{results.filter((r) => r.status === 'success').length}</p>
                            <p className="text-sm text-gray-600 dark:text-gray-400">Successful</p>
                        </div>
                        <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                            <p className="text-2xl font-bold text-red-600 dark:text-red-400">{results.filter((r) => r.status === 'failed').length}</p>
                            <p className="text-sm text-gray-600 dark:text-gray-400">Failed</p>
                        </div>
                        <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                            <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">{{ total_size }}</p>
                            <p className="text-sm text-gray-600 dark:text-gray-400">Total Size</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Preview Modal */}
            <div id="preview-modal" className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center hidden z-50">
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 max-w-4xl w-full mx-4 max-h-[90vh] overflow-auto">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">File Preview</h3>
                        <button onclick={CloseFilePreview} className="text-gray-500 hover:text-gray-700">
                            <i className="fas fa-times text-xl"></i>
                        </button>
                    </div>
                    <div id="preview-content" className="text-center">
                        {/* Preview content will be loaded here */}
                    </div>
                </div>
            </div>
        </section>
    )
}
