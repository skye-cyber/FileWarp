export const AvailableTools = {
    // Document Tools
    convert_doc: {
        category: 'documents',
        id: 'convert_doc',
        name: "convert",
        description: "convert documents"
    },
    pdf_join: {
        category: 'documents',
        id: 'pdf_join',
        name: 'join pdf',
        description: "join pdf document"
    },
    scan_pdf: {
        category: 'documents',
        id: 'scan_pdf',
        name: 'scan pdf',
        description: "scan pdf document"
    },
    doc_long_image: {
        category: 'documents',
        id: 'doc_long_image',
        name: "document to longimage",
        description: "convert to long image"
    },
    extract_pages: {
        category: 'documents',
        id: 'extract_pages',
        name: 'extract pages',
        description: "extract pages from document"
    },
    doc2image: {
        category: 'documents',
        id: 'doc2image',
        name: 'doc to image',
        description: "convert document to image"
    },

    // Image Tools
    convert_image: {
        category: 'images',
        id: 'convert_image',
        name: "convert image",
        description: "convert image"
    },
    resize_image: {
        category: 'images',
        id: 'resize_image',
        name: "resize image",
        description: "resize"
    },
    image2pdf: {
        category: 'images',
        id: 'image2pdf',
        name: "image to pdf",
        description: "convert image to pdf"
    },
    image2word: {
        category: 'images',
        id: 'image2word',
        name: "image to word",
        description: "convert image to word"
    },
    image2gray: {
        category: 'images',
        id: 'image2gray',
        name: "image to gray",
        description: "convert image to grayscale"
    },
    ocr: {
        category: 'images',
        id: 'ocr',
        name: "ocr",
        description: "perform text extraction on image"
    },

    // Audio Tools
    convert_audio: {
        category: 'audios',
        id: 'convert_audio',
        name: "convert audio",
        description: "convert audio"
    },
    audio_join: {
        category: 'audios',
        id: 'audio_join',
        name: "join audio",
        description: "join audio files"
    },
    audio_effect: {
        category: 'audios',
        id: 'audio_effect',
        name: "create audio effects",
        description: "manipulate audio to create sound effects"
    },

    // Video Tools
    convert_video: {
        category: 'videos',
        id: 'convert_video',
        name: "convert video",
        description: "convert video"
    },
    analyze_video: {
        category: 'videos',
        id: 'analyze_video',
        name: "analyze video",
        description: "Obtain video metadata"
    },
    extract_audio: {
        category: 'videos',
        id: 'extract_audio',
        name: "extract audio",
        description: "extract audio from video"
    },

    // Batch Tools
    batch_dashboard: {
        category: 'batch',
        id: 'batch_dashboard',
        name: "dashboard batch ops",
        description: "dashboard batch ops"
    },
    batch_doc_convert: {
        category: 'batch',
        id: 'batch_doc_convert',
        name: "batch doc convert",
        description: "convert multiple documents"
    },
    folder_operations: {
        category: 'batch',
        id: 'folder_operations',
        name: "batch folder operation",
        description: "operate on folder"
    },
    bulk_ocr: {
        category: 'batch',
        id: 'bulk_ocr',
        name: "bulk ocr",
        descritpion: "bulk ocr operations"
    }
}


export function getToolsByCategory(category = "documents") {
    const keys = Object.keys(AvailableTools)
    let Tools = {}

    keys.forEach((key) => AvailableTools[key].category === category ? Tools = { ...Tools, [key]: AvailableTools[key] } : '')
    return Tools
}

export function getFirstToolByCategory(category = "documents") {
    const keys = Object.keys(AvailableTools)

    for (const key of keys) {
        if (AvailableTools[key].category === category) {
            return { [key]: AvailableTools[key] }
        }
    }
    return null
}

export function sortToolsByCategory() {
    const keys = Object.keys(AvailableTools)
    //const categories = ['documents', 'images', 'videos', 'audio', 'batch', 'misceleneous']
    let sortedTools = {}

    keys.forEach((key) => {
        const category = AvailableTools[key].category
        if (!Object.keys(sortedTools).includes(category)) {
            sortedTools = {
                ...sortedTools,
                [category]: [{ [key]: AvailableTools[key] }]
            }
        } else {
            sortedTools[category].push({ [key]: AvailableTools[key] })
        }
    })
    return sortedTools
}

export function countCategoryTools(category) {
    const tools = getToolsByCategory(category)
    return Object.keys(tools).length
}

export function getToolFromCategory(category, tool_id) {
    const categoryTools = getToolsByCategory(category)
    let tool

    Object.keys(categoryTools).forEach((key) => {
        if (categoryTools[key].id === tool_id) {
            tool = categoryTools[key]
        }
    })
    console.log(tool_id, tool)
    return tool
}
