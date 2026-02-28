import React from "react";
import { useNavigate } from 'react-router-dom';
import { countCategoryTools, getToolFromCategory } from "../Tools/schema";
import { setActiveTab, setActiveTool } from "../../store/warpSlice";
import { useDispatch } from "react-redux";
import { FileWithLines, Audio, Video, Images, ArrowRight, MediaPlay, ActivityArrowCircle } from "../svg/core";
import { Folder } from "@mui/icons-material";
import { useTheme } from "@emotion/react";
export const Dashboard = ({ }) => {
    const navigate = useNavigate()
    const dispatch = useDispatch()

    const handleNavigate = (path, tool_id) => {
        try {
            const norm_path = path.replace('/', '')
            dispatch(setActiveTab(norm_path))
            dispatch(setActiveTool(getToolFromCategory(norm_path, tool_id)))
            navigate(path)
        } catch (err) {
            console.log(err)
        }
    }
    return (
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            {/* Hero Section */}
            <div className="gradient-bg rounded-2xl p-8 text-white mb-8 hidden" data-aos="fade-up">
                <div className="max-w-3xl">
                    <h1 className="text-4xl font-bold mb-4">File Management Suite</h1>
                    <p className="text-xl opacity-90 mb-6">Convert, analyze, and process your files with powerful tools</p>
                    <div className="flex flex-wrap gap-4">
                        <button onClick={() => handleNavigate('/document')} className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors flex gap-2 items-center">
                            <svg className="fill-blue-600 w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640"><path d="M128 64C92.7 64 64 92.7 64 128L64 512C64 547.3 92.7 576 128 576L208 576L208 464C208 428.7 236.7 400 272 400L448 400L448 234.5C448 217.5 441.3 201.2 429.3 189.2L322.7 82.7C310.7 70.7 294.5 64 277.5 64L128 64zM389.5 240L296 240C282.7 240 272 229.3 272 216L272 122.5L389.5 240zM272 444C261 444 252 453 252 464L252 592C252 603 261 612 272 612C283 612 292 603 292 592L292 564L304 564C337.1 564 364 537.1 364 504C364 470.9 337.1 444 304 444L272 444zM304 524L292 524L292 484L304 484C315 484 324 493 324 504C324 515 315 524 304 524zM400 444C389 444 380 453 380 464L380 592C380 603 389 612 400 612L432 612C460.7 612 484 588.7 484 560L484 496C484 467.3 460.7 444 432 444L400 444zM420 572L420 484L432 484C438.6 484 444 489.4 444 496L444 560C444 566.6 438.6 572 432 572L420 572zM508 464L508 592C508 603 517 612 528 612C539 612 548 603 548 592L548 548L576 548C587 548 596 539 596 528C596 517 587 508 576 508L548 508L548 484L576 484C587 484 596 475 596 464C596 453 587 444 576 444L528 444C517 444 508 453 508 464z" /></svg>Document Tools
                        </button>
                        <button onClick={() => handleNavigate('/audio')} className="bg-white text-green-600 px-6 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors flex gap-2 items-center">
                            <svg className="fill-green-600 w-6 h-6 mt-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640"><path d="M532 71C539.6 77.1 544 86.3 544 96L544 400C544 444.2 501 480 448 480C395 480 352 444.2 352 400C352 355.8 395 320 448 320C459.2 320 470 321.6 480 324.6L480 207.9L256 257.7L256 464C256 508.2 213 544 160 544C107 544 64 508.2 64 464C64 419.8 107 384 160 384C171.2 384 182 385.6 192 388.6L192 160C192 145 202.4 132 217.1 128.8L505.1 64.8C514.6 62.7 524.5 65 532.1 71.1z" /></svg>Audio Tools
                        </button>
                        <button onClick={() => handleNavigate('/video')} className="bg-white text-purple-600 px-6 py-3 rounded-lg font-semibold hover:bg-purple-50 transition-colors flex gap-2 items-center">
                            <svg className="fill-purple-600 w-6 h-6 mt-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640"><path d="M128 128C92.7 128 64 156.7 64 192L64 448C64 483.3 92.7 512 128 512L384 512C419.3 512 448 483.3 448 448L448 192C448 156.7 419.3 128 384 128L128 128zM496 400L569.5 458.8C573.7 462.2 578.9 464 584.3 464C597.4 464 608 453.4 608 440.3L608 199.7C608 186.6 597.4 176 584.3 176C578.9 176 573.7 177.8 569.5 181.2L496 240L496 400z" /></svg>Video Tools
                        </button>
                        <button onClick={() => handleNavigate('/Image')} className="bg-white text-red-600 px-6 py-3 rounded-lg font-semibold hover:bg-red-50 transition-colors flex gap-2 items-center">
                            <svg className="fill-red-600 w-6 h-6 mt-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640"><path d="M128 160C128 124.7 156.7 96 192 96L512 96C547.3 96 576 124.7 576 160L576 416C576 451.3 547.3 480 512 480L192 480C156.7 480 128 451.3 128 416L128 160zM56 192C69.3 192 80 202.7 80 216L80 512C80 520.8 87.2 528 96 528L456 528C469.3 528 480 538.7 480 552C480 565.3 469.3 576 456 576L96 576C60.7 576 32 547.3 32 512L32 216C32 202.7 42.7 192 56 192zM224 224C241.7 224 256 209.7 256 192C256 174.3 241.7 160 224 160C206.3 160 192 174.3 192 192C192 209.7 206.3 224 224 224zM420.5 235.5C416.1 228.4 408.4 224 400 224C391.6 224 383.9 228.4 379.5 235.5L323.2 327.6L298.7 297C294.1 291.3 287.3 288 280 288C272.7 288 265.8 291.3 261.3 297L197.3 377C191.5 384.2 190.4 394.1 194.4 402.4C198.4 410.7 206.8 416 216 416L488 416C496.7 416 504.7 411.3 508.9 403.7C513.1 396.1 513 386.9 508.4 379.4L420.4 235.4z" /></svg>Image Tools
                        </button>
                    </div>
                </div>
            </div>
            <div className="space-y-6">
                {/* Quick Stats */}
                <QuickStats />

                {/* Featured Tools */}
                <FeatureTools handleNavigate={handleNavigate} />

                {/* Recent Activity */}
                <RecentActivity />
            </div>
        </div>
    )
}

export const QuickStats = ({ }) => (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white dark:bg-secondary-950 rounded-xl p-2 sm:p-6 border border-x-[4px] border-blue-400 shadow-centered-md shadow-accent-100/20 dark:shadow-accent-800 mx-2 hover:translate-y-2 transition-translate duration-300" data-aos="fade-up" data-aos-delay="100">
            <div className="flex items-center">
                <div className="p-3 bg-blue-100 dark:bg-blue-950 rounded-lg mr-2 sm:mr-4">
                    <FileWithLines className="fill-blue-600 dark:fill-blue-400 w-4 h-4 sm:w-8 sm:h-8" />
                </div>
                <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Document Tools</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{countCategoryTools('documents')}</p>
                </div>
            </div>
        </div>

        <div className="bg-white dark:bg-secondary-950 rounded-xl p-3 sm:p-6 border border-x-[4px]  dark:border-y-green-300 border-green-400 dark:border-x-green-200 shadow-centered-md shadow-accent-100/20 dark:shadow-accent-800 mx-2 hover:translate-y-2 transition-translate duration-300" data-aos="fade-up" data-aos-delay="200">
            <div className="flex items-center">
                <div className="p-3 bg-green-100 dark:bg-green-950 rounded-lg mr-4">
                    <Audio className="fill-green-600 dark:fill-green-400 w-4 h-4 sm:w-8 sm:h-8" />
                </div>
                <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Audio Tools</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{countCategoryTools('audios')}</p>
                </div>
            </div>
        </div>

        <div className="bg-white dark:bg-secondary-950 rounded-xl p-3 sm:p-6 border border-x-[4px] border-purple-400 shadow-centered-md shadow-accent-100/20 dark:shadow-accent-800 mx-2 hover:translate-y-2 transition-translate duration-300" data-aos="fade-up" data-aos-delay="300">
            <div className="flex items-center">
                <div className="p-3 bg-purple-100 dark:bg-purple-950 rounded-lg mr-4">
                    <Video className="fill-purple-600 dark:fill-purple-400 w-4 h-4 sm:w-8 sm:h-8" />
                </div>
                <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Video Tools</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{countCategoryTools('videos')}</p>
                </div>
            </div>
        </div>

        <div className="bg-white dark:bg-secondary-950 rounded-xl p-3 sm:p-6 border border-x-[4px] border-red-300 dark:border-red-200 shadow-centered-md shadow-accent-100/20 dark:shadow-accent-800 mx-2 hover:translate-y-2 transition-translate duration-300" data-aos="fade-up" data-aos-delay="400">
            <div className="flex items-center">
                <div className="p-3 bg-red-100 dark:bg-red-950 rounded-lg mr-4">
                    <Images className="fill-red-600 dark:fill-red-400 w-4 h-4 sm:w-8 sm:h-8" />
                </div>
                <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Image Tools</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{countCategoryTools('images')}</p>
                </div>
            </div>
        </div>
    </div>
)

export const RecentActivity = ({ }) => (
    <div
        className="bg-white dark:bg-cyber-950 rounded-none sm:rounded-xl shadow-md p-1 sm:p-6"
        data-aos="fade-up"
    >
        <h2 className="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Recent Activity
        </h2>
        <div className="space-y-4">
            <div className="flex flex-col-2 items-center justify-center py-8 text-gray-500 dark:text-gray-400">
                <div className="flex flex-col items-center gap-2">
                    <ActivityArrowCircle className="fill-gray-500 dark:fill-gray-400 w-8 h-8 sm:w-12 sm:h-12" />
                    <p className="text-sm text-center text-gray-500 dark:text-gray-400">No recent activity</p>
                </div>
            </div>
        </div>
    </div>
)

export const FeatureTools = ({ handleNavigate }) => (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
        {/* Document Tools */}
        <div className="bg-white dark:bg-cyber-950 text-gray-800 dark:text-white rounded-none sm:rounded-xl shadow-md p-1 sm:p-6" data-aos="fade-right">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white flex items-center">
                <Folder className="text-blue-600 dark:text-blue-500 w-6 h-6 mr-2" />Document Tools
            </h3>
            <div className="grid grid-cols-2 gap-3">
                <button onClick={() => handleNavigate('/documents', 'convert_doc')} className="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-secondary-900 rounded-lg transition-colors">
                    <span className="text-sm sm:text-[16px] font-medium">Document Conversion</span>
                    <ArrowRight className="w-5 h-5 fill-gray-400" />
                </button>
                <button onClick={() => handleNavigate('/documents', 'pdf_join')} className="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-secondary-900 rounded-lg transition-colors">
                    <span className="text-sm sm:text-[16px] font-medium">PDF Joining</span>
                    <ArrowRight className="w-5 h-5 fill-gray-400" />
                </button>
                <button onClick={() => handleNavigate('/documents', 'scan_pdf')} className="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-secondary-900 rounded-lg transition-colors">
                    <span className="text-sm sm:text-[16px] font-medium">PDF Text Extraction</span>
                    <ArrowRight className="w-5 h-5 fill-gray-400" />
                </button>
            </div>
        </div>

        {/* Media Tools */}
        <div className="bg-white dark:bg-cyber-950 text-gray-800 dark:text-white rounded-none sm:rounded-xl shadow-md p-1 sm:p-6" data-aos="fade-left">
            <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white flex items-center">
                <MediaPlay className="fill-purple-500 w-6 h-6 mr-2" />Media Tools
            </h3>
            <div className="grid grid-cols-2 gap-3">
                <button onClick={() => handleNavigate('/audios', 'audio_join')} className="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-secondary-900 rounded-lg transition-colors">
                    <span className="text-sm sm:text-[16px] font-medium">Audio Join</span>
                    <ArrowRight className="w-5 h-5 fill-gray-400" />
                </button>
                <button onClick={() => handleNavigate('/videos', 'extract_audio')} className="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-secondary-900 rounded-lg transition-colors">
                    <span className="font-medium text-sm sm:text-[16px]">Audio Extract</span>
                    <ArrowRight className="w-5 h-5 fill-gray-400" />
                </button>
                <button onClick={() => handleNavigate('/images', 'image2pdf')} className="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-secondary-900 rounded-lg transition-colors">
                    <span className="font-medium text-sm sm:text-[16px]">Image to PDF</span>
                    <ArrowRight className="w-5 h-5 fill-gray-400" />
                </button>
                <button onClick={() => handleNavigate('/images', 'ocr')} className="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-secondary-900 rounded-lg transition-colors">
                    <span className="text-sm sm:text-[16px] font-medium">OCR</span>
                    <ArrowRight className="w-5 h-5 fill-gray-400" />
                </button>
            </div>
        </div>
    </div>
)

