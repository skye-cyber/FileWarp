import React, { useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from 'react-redux';
import { setActiveTab, setActiveTool } from "../../store/warpSlice";
import { getFirstToolByCategory } from "../Tools/schema";
import { useTheme } from "../Themes/useThemeHeadless";
import { Images, Moon, PdfDocument, Stack, Sun, Video, Audio, Dashboard, FileWithLines, Hambuger } from "../svg/core";
import { CollapsiblePanel } from "./Panel";

export const NavbarTop = ({ }) => {
    const { isDark, toggleTheme, setTheme, theme } = useTheme()
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const { ui } = useSelector((state) => state.warp);
    const PanelRef = useRef(null)

    const handleNavigate = (path) => {
        try {
            const normalized_path = path.replace('/', '')
            navigate(path)
            dispatch(setActiveTab(normalized_path))
            const firstTool = getFirstToolByCategory(normalized_path)
            dispatch(setActiveTool(firstTool[Object.keys(firstTool)]))
        } catch {
            //
        }
    }

    React.useEffect(() => {
        //
    })

    const OpnenavPanel = () => {
        PanelRef.current.classList.remove('hidden')
        setTimeout(() => {
            PanelRef.current.classList.remove('-translate-x-full')
            PanelRef.current.classList.add('translate-x-0')
        }, 100)
    }

    const ClosenavPanel = () => {
        PanelRef.current.classList.remove('translate-x-0')
        PanelRef.current.classList.add('-translate-x-full')
        setTimeout(() => {
            PanelRef.current.classList.add('hidden')
        }, 700)
    }

    const TogglePanel = () => {
        if (PanelRef.current.classList.contains('hidden')) {
            OpnenavPanel()
        } else {
            ClosenavPanel()
        }
    }

    return (
        <nav className="sticky top-0 left-0 w-full z-[10] bg-white dark:bg-gray-900 shadow-lg border-b dark:border-gray-700 sticky top-0 z-50 shadow-balanced-xl">
            <CollapsiblePanel onNavigate={handleNavigate} panelref={PanelRef} onclose={ClosenavPanel} />
            <div className="relative max-w-7xl mx-auto px-4">
                <Hambuger onclick={() => TogglePanel()} className="block md:hidden absolute top-6 left-1 z-5 cursor-pointer" />
                <div className="flex justify-between h-16 ml-6 md:ml-0">
                    <div className="flex items-center">
                        <div className="flex-shrink-0 flex items-center">
                            <FileWithLines className="hidden w-8 h-8 fill-blue-600" />
                            <span className="text-xl font-bold text-gray-900 dark:text-white font-handwriting">FileWarp</span>
                        </div>
                        <div className="hidden md:ml-6 md:flex md:space-x-8">
                            <button onClick={() => handleNavigate('/dashboard')} className={`nav-link ${ui.activeTab === 'dashboard' ? "active" : ""}`}>
                                <Dashboard className={`nav-svg ${ui.activeTab === 'dashboard' ? "active" : ""}`} />
                                Dashboard
                            </button>
                            <button onClick={() => handleNavigate('/documents')} className={`nav-link ${ui.activeTab === 'documents' ? "active" : ""}`}>
                                <PdfDocument className={`nav-svg ${ui.activeTab === 'document' ? "active" : ""}`} />Documents
                            </button>
                            <button onClick={() => handleNavigate('/audios')} className={`nav-link ${ui.activeTab === 'audios' ? "active" : ""}`}>
                                <Audio className={`nav-svg ${ui.activeTab === 'audio' ? "active" : ""}`} />Audio
                            </button>
                            <button onClick={() => handleNavigate('/videos')} className={`nav-link ${ui.activeTab === 'videos' ? "active" : ""}`}>
                                <Video className={`nav-svg ${ui.activeTab === 'video' ? "active" : ""}`} /> Video
                            </button>
                            <button onClick={() => handleNavigate('/images')} className={`nav-link ${ui.activeTab === 'images' ? "active" : ""}`}>
                                <Images className={`nav-svg ${ui.activeTab === 'image' ? "active" : ""}`} />Images
                            </button>
                        </div>
                    </div>
                    <div className="flex items-center space-x-4">
                        <button onClick={() => handleNavigate('/batch')} className={`nav-link ${ui.activeTab === 'batch' ? "active" : ""}`}>
                            <Stack className={`nav-svg ${ui.activeTab === 'batch' ? "active" : ""}`} />Batch <span className="hidden lg:flex ml-0">Tools</span>
                        </button>
                        <ThemeSwitch toggleTheme={toggleTheme} isDark={isDark} />
                    </div>
                </div>
            </div>
        </nav>
    )
}

export const ThemeSwitch = ({ toggleTheme, isDark }) => {
    return (
        <button onClick={() => toggleTheme()} className="flex items-center justify-center h-10 w-10 rounded-full bg-gray-50 dark:bg-accent-300 hover:bg-primary-100 dark:hover:bg-accent-100/50 text-slate-700 dark:text-slate-300 transition-colors duration-300">
            <Moon className="hidden dark:block h-5 w-5 fill-white" />
            <Sun className="dark:hidden h-5 w-5 fill-slate-800 dark:fill-white" />
        </button>
    )
}

export const TabButton = ({ clickCallback, path, TextDisplay = '' }) => (
    <button onClick={() => clickCallback(path)} className={`nav-link ${ui.activeTab === 'batch' ? "active" : ""}`}>
        <Stack className={`nav-svg ${ui.activeTab === 'batch' ? "active" : ""}`} />{TextDisplay}
    </button>
)
