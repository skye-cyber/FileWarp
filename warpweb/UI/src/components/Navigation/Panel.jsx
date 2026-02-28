import { useDispatch, useSelector } from 'react-redux';
import { Images, Moon, PdfDocument, Stack, Sun, Video, Audio, Dashboard, FileWithLines, Hambuger } from "../svg/core";


export const CollapsiblePanel = ({ onNavigate, onclose, panelref }) => {
    const { ui } = useSelector((state) => state.warp);

    return (
        <div ref={panelref} className={`absolute top-16 left-0 z-[20] border border-blue-100 dark:border-accent-400/50 shadow-lg shadow-gray-300 dark:shadow-cyber-700 h-fit max-h-[70vh] min-w-32 w-fit overflow-h-auto scrollbar-custom max-w-64 bg-white dark:bg-cyber-900 p-2 hidden -translate-x-full transition-tanslate duration-500 ease-in-out rounded-b-md`}>
            <div className="block gao-1">
                <button onClick={() => onNavigate('/dashboard')} className={`nav-link dark:hover:bg-accent-400/20 hover:border-b-2 border-blend-50 w-full ${ui.activeTab === 'dashboard' ? "active" : ""}`}>
                    <Dashboard className={`nav-svg ${ui.activeTab === 'dashboard' ? "active" : ""}`} />
                    Dashboard
                </button>
                <button onClick={() => onNavigate('/documents')} className={`nav-link dark:hover:bg-accent-400/20 hover:border-b-2 border-blend-50 w-full ${ui.activeTab === 'documents' ? "active" : ""}`}>
                    <PdfDocument className={`nav-svg ${ui.activeTab === 'document' ? "active" : ""}`} />Documents
                </button>
                <button onClick={() => onNavigate('/audios')} className={`nav-link dark:hover:bg-accent-400/20 hover:border-b-2 border-blend-50 w-full ${ui.activeTab === 'audios' ? "active" : ""}`}>
                    <Audio className={`nav-svg ${ui.activeTab === 'audio' ? "active" : ""}`} />Audio
                </button>
                <button onClick={() => onNavigate('/videos')} className={`nav-link dark:hover:bg-accent-400/20 hover:border-b-2 border-blend-50 w-full ${ui.activeTab === 'videos' ? "active" : ""}`}>
                    <Video className={`nav-svg ${ui.activeTab === 'video' ? "active" : ""}`} /> Video
                </button>
                <button onClick={() => onNavigate('/images')} className={`nav-link dark:hover:bg-accent-400/20 hover:border-b-2 border-blend-50 w-full ${ui.activeTab === 'images' ? "active" : ""}`}>
                    <Images className={`nav-svg ${ui.activeTab === 'image' ? "active" : ""}`} />Images
                </button>
            </div>
        </div>
    )
}
