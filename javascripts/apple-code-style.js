/**
 * Apple Style Code Blocks JavaScript
 * 为代码块添加真正的苹果风格效果
 */

document.addEventListener('DOMContentLoaded', function() {
    initAppleCodeBlocks();
});

function initAppleCodeBlocks() {
    // 查找所有代码块
    const highlights = document.querySelectorAll('.highlight');
    
    highlights.forEach(function(highlight) {
        processCodeBlock(highlight);
    });
}

function processCodeBlock(highlight) {
    // 检测语言
    const lang = detectLanguage(highlight);
    
    if (lang) {
        // 设置 data-lang 属性（备用）
        highlight.setAttribute('data-lang', lang);
        
        // 总是创建语言标识，无论是否有文件名
        createLanguageLabel(highlight, lang);
    }
}

function detectLanguage(highlight) {
    // 方法1: 从 code 元素的 class 中检测
    const codeElement = highlight.querySelector('code');
    if (codeElement) {
        const classList = Array.from(codeElement.classList);
        for (let className of classList) {
            if (className.startsWith('language-')) {
                return className.replace('language-', '');
            }
            // 也检查不带 language- 前缀的
            if (['python', 'javascript', 'csharp', 'css', 'html', 'bash', 'json', 'yaml', 'cpp', 'java', 'go', 'rust', 'php'].includes(className)) {
                return className;
            }
        }
    }
    
    // 方法2: 从 pre 元素的 class 中检测
    const preElement = highlight.querySelector('pre');
    if (preElement) {
        const classList = Array.from(preElement.classList);
        for (let className of classList) {
            if (className.startsWith('language-')) {
                return className.replace('language-', '');
            }
        }
    }
    
    // 方法3: 从 highlight 本身的 class 中检测
    const highlightClasses = Array.from(highlight.classList);
    for (let className of highlightClasses) {
        if (className.startsWith('highlight-')) {
            return className.replace('highlight-', '');
        }
        if (className.startsWith('language-')) {
            return className.replace('language-', '');
        }
    }
    
    // 方法4: 尝试从内容推断语言
    const codeText = highlight.textContent || '';
    return inferLanguageFromContent(codeText);
}

function inferLanguageFromContent(codeText) {
    // C# 语言特征检测
    if (codeText.includes('using System') || codeText.includes('namespace ') || codeText.includes('public class')) {
        return 'csharp';
    }
    
    // Python 语言特征检测
    if (codeText.includes('def ') || codeText.includes('import ') || codeText.includes('from ') || codeText.includes('#!/usr/bin/env python')) {
        return 'python';
    }
    
    // JavaScript 语言特征检测
    if (codeText.includes('function ') || codeText.includes('const ') || codeText.includes('let ') || codeText.includes('var ')) {
        return 'javascript';
    }
    
    // CSS 语言特征检测
    if (codeText.includes('{') && codeText.includes('}') && (codeText.includes(':') && codeText.includes(';'))) {
        return 'css';
    }
    
    // HTML 语言特征检测
    if (codeText.includes('<!DOCTYPE') || codeText.includes('<html') || codeText.includes('</')) {
        return 'html';
    }
    
    // Bash/Shell 脚本检测
    if (codeText.includes('#!/bin/bash') || codeText.includes('#!/bin/sh')) {
        return 'bash';
    }
    
    // JSON 检测
    if ((codeText.trim().startsWith('{') && codeText.trim().endsWith('}')) || 
        (codeText.trim().startsWith('[') && codeText.trim().endsWith(']'))) {
        try {
            JSON.parse(codeText);
            return 'json';
        } catch (e) {
            // 不是有效的JSON
        }
    }
    
    return null; // 无法检测到语言
}

function createLanguageLabel(highlight, lang) {
    // 检查是否已经有语言标签了
    const existingLabel = highlight.querySelector('.apple-lang-label');
    if (existingLabel) {
        existingLabel.textContent = formatLanguageName(lang);
        return;
    }
    
    // 如果已经有 filename，不需要创建新的标签
    const existingFilename = highlight.querySelector('span.filename');
    if (existingFilename) {
        return;
    }
    
    // 创建语言标签元素
    const langLabel = document.createElement('div');
    langLabel.className = 'apple-lang-label';
    langLabel.textContent = formatLanguageName(lang);
    
    // 插入到代码块中（不是开头，因为::before已经创建了背景）
    highlight.appendChild(langLabel);
}

function formatLanguageName(lang) {
    const languageNames = {
        'python': 'Python',
        'javascript': 'JavaScript', 
        'js': 'JavaScript',
        'csharp': 'C#',
        'cs': 'C#',
        'css': 'CSS',
        'html': 'HTML',
        'bash': 'Bash',
        'sh': 'Shell',
        'json': 'JSON',
        'yaml': 'YAML',
        'yml': 'YAML',
        'cpp': 'C++',
        'c': 'C',
        'java': 'Java',
        'go': 'Go',
        'rust': 'Rust',
        'php': 'PHP',
        'sql': 'SQL',
        'xml': 'XML'
    };
    
    return languageNames[lang] || lang.toUpperCase();
}

// 为动态加载的内容重新初始化
function reinitAppleCodeBlocks() {
    initAppleCodeBlocks();
}

// 导出函数供外部使用
window.AppleCodeStyle = {
    init: initAppleCodeBlocks,
    reinit: reinitAppleCodeBlocks
};
