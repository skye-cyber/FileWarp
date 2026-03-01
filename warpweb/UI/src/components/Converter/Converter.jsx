import React, { useRef } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { AvailableTools, getToolsByCategory } from "../Tools/schema";
import { setActiveTab, setActiveTool } from "../../store/warpSlice";
import { toTitleCase } from "../../utils/extendJS";
import { useNavigate } from "react-router-dom";
import { ChevronRight, MargicTool } from "../svg/core";
import { AppBlocking, ChevronLeft, DensityLarge, DensityMedium, ListAlt, MenuBook, MenuOpen, MenuOpenOutlined, MoreHoriz, MoreVert, MoreVertOutlined, Reorder } from "@mui/icons-material";
import { AppBar } from "@mui/material";

export const Converter = ({ category = 'documents' }) => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const { activeTool, ui } = useSelector((state) => state.warp);
    const [Tools, setTools] = React.useState(null)
    const availableToolRef = useRef()

    React.useEffect(() => {
        if (ui.activeTab === 'dashboard') return navigate('/dashboard');

        const tools = getToolsByCategory(ui.activeTab);
        setTools(tools);
    }, [ui.activeTab, navigate, getToolsByCategory]);

    const ToolSwitch = React.useCallback((tool) => {
        console.log("Switch tool:", tool)
        dispatch(setActiveTab(tool.category))
        dispatch(setActiveTool(tool))

        // TODO Update active tool item in the nav
        // Active tool className: 'bg-blue-50 dark:bg-blue-900 border-blue-500 border-r-4'
        // Inactive Tool className: ''
    })

    const DropZoneInit = () => {
        //setupFileDropZone('doc-drop-zone', 'doc-file-input');
        // setupFileDropZone('doc-drop-zone', 'audio-file-input');
        // ...
    }

    const openTools = () => {
        availableToolRef.current.classList.remove('hidden')
    }

    const closeTools = () => {
        availableToolRef.current.classList.add('hidden')
    }

    const toggleTools = () => {
        if (availableToolRef.current.classList.contains('hidden')) {
            openTools()
        } else {
            closeTools()
        }
    }

    const ToolButton = ({ tool }) => {
        if (!tool) return
        return (
            <button
                onClick={() => ToolSwitch(tool.id)}
                className={`tool-nav w-full text-left p-1 sm:p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-blend-900 transition-colors tool-${tool.id} hover:border-x-2 border-blue-400 dark:border-secondary-100 trasition-transform transition-all duration-500`}
            >
                <div className="flex items-center justify-between">
                    <span className="font-medium text-gray-700 dark:text-gray-300"
                    >{toTitleCase(tool.name)}</span
                    >
                    <ChevronRight className="hidden sm:block w-5 h-5 fill-gray-400" />
                </div>
                <p className="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mt-0 sm:mt-1">
                    {tool.description}
                </p>
            </button>
        )
    }

    return (
        <div className="w-full max-w-screen h-screen py-0">
            {/* Category Header */}
            <div className="hidden mb-8" data-aos="fade-up">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                    {toTitleCase(activeTool.category)} Tools
                </h1>
                <p className="text-gray-600 dark:text-gray-400">Select a tool to get started</p>
            </div>

            {/* Tools Grid */}
            <div className="relative block sm:grid grid-cols-1 lg:grid-cols-3 gap-0 h-full">
                {/* Tools Navigation */}
                <div ref={availableToolRef}
                    className="block sm:sticky top-0 left-0 z-[5] bg-white dark:bg-cyber-950 rounded-none shadow-md p-2 sm:p-6 mb-0.5 sm:mb-14 w-fit max-w-full sm:max-w-[30vw] sm:h-[90%] overflow-auto scrollbar-custom"
                >
                    <div className="sticky -top-6 left-0 z-[5] text-lg bg-inherit w-full">
                        <h3 className=" font-semibold mb-4 text-gray-900 dark:text-white">
                            Available Tools
                        </h3>
                    </div>
                    <div className="flex flex-wrap sm:block space-y-0 sm:space-y-2 mt-2">
                        {Tools &&
                            Object.keys(Tools).map((toolkey, key) => {
                                // console.log(toolkey, AvailableTools[toolkey])
                                return <ToolButton key={key} tool={AvailableTools[toolkey]} />
                            })}
                    </div>
                </div>

                {/* Tool Interface */}
                <div className="w-full lg:col-span-2 mt-1 bg-orange-300" data-aos="fade-left">
                    <div
                        id="tool-interface"
                        className="bg-white dark:bg-cyber-950 rounded-none sm:rounded-xl shadow-md p-2 sm:p-6"
                    >
                        {activeTool && activeTool.component ?
                            <activeTool.component />
                            :
                            <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                                <span className="flex justify-center mb-4">
                                    <MargicTool className="w-12 h-12 fill-sky-500 dark:fill-gray-300" />
                                </span>
                                <h3 className="text-lg sm:text-xl font-semibold mb-2 font-normal">Select a Tool</h3>
                                <p className="text-sm sm:text-[16px]">
                                    Choose a tool from the left sidebar to start processing your files
                                </p>
                            </div>
                        }

                    </div>
                </div>
            </div>
        </div >
    )
}
