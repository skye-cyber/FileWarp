export function toCamelCase(str) {
    if (!str) return ''
    const words = str.split(' ');
    return words[0].toLowerCase() +
        words.slice(1).map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join('');
}

export function toTitleCase(str) {
    if (!str) return ''
        const firstLetter = str[0];
    return firstLetter.toUpperCase() + str.slice(1)
}
