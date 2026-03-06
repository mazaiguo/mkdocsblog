/**
 * 代码块隐藏/显示功能
 * Code Block Toggle Functionality for MkDocs
 * 
 * 功能特性:
 * - 点击标题栏切换代码块显示/隐藏
 * - 平滑的折叠动画效果
 * - 记住折叠状态（localStorage）
 * - 支持批量操作
 * - 可视化指示器
 */

document.addEventListener('DOMContentLoaded', function() {
    initCodeBlockToggle();
});

/**
 * 初始化代码块切换功能
 */
function initCodeBlockToggle() {
    // 查找所有代码块
    const highlights = document.querySelectorAll('.highlight');
    
    highlights.forEach(function(highlight, index) {
        setupToggleForCodeBlock(highlight, index);
    });
    
    // 添加全局控制按钮
    addGlobalToggleControls();
    
    // 恢复折叠状态
    restoreToggleStates();
}

/**
 * 为单个代码块设置切换功能
 * @param {Element} highlight 代码块容器
 * @param {number} index 代码块索引
 */
function setupToggleForCodeBlock(highlight, index) {
    // 添加唯一ID
    if (!highlight.id) {
        highlight.id = `code-block-${index}`;
    }
    
    // 创建切换按钮
    const toggleButton = createToggleButton();
    
    // 获取或创建标题栏点击区域
    let clickArea = highlight.querySelector('.code-header-click-area');
    if (!clickArea) {
        clickArea = createHeaderClickArea();
        highlight.appendChild(clickArea);
    }
    
    // 添加切换按钮到标题栏
    clickArea.appendChild(toggleButton);
    
    // 查找并移动复制按钮到标题栏内
    moveCopyButtonToHeader(highlight, clickArea);
    
    // 获取代码内容区域
    const codeContent = getCodeContent(highlight);
    if (!codeContent) return;
    
    // 添加切换状态类
    highlight.classList.add('toggleable');
    
    // 检查是否有Markdown标记要求初始折叠状态
    const shouldCollapse = checkMarkdownCollapseMarkers(highlight);
    if (shouldCollapse) {
        // 标记为需要初始折叠
        highlight.setAttribute('data-initial-collapse', 'true');
    }
    
    // 绑定点击事件
    clickArea.addEventListener('click', function(e) {
        // 避免影响复制按钮
        if (e.target.closest('.md-clipboard')) {
            return;
        }
        
        toggleCodeBlock(highlight, codeContent, toggleButton);
    });
    
    // 添加键盘支持
    clickArea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggleCodeBlock(highlight, codeContent, toggleButton);
        }
    });
    
    // 设置可访问性属性
    clickArea.setAttribute('role', 'button');
    clickArea.setAttribute('tabindex', '0');
    clickArea.setAttribute('aria-expanded', 'true');
    clickArea.setAttribute('aria-controls', highlight.id + '-content');
    
    // 为代码内容添加ID
    codeContent.id = highlight.id + '-content';
}

/**
 * 移动复制按钮到标题栏内
 * @param {Element} highlight 代码块容器
 * @param {Element} clickArea 标题栏点击区域
 */
function moveCopyButtonToHeader(highlight, clickArea) {
    // 尝试多次查找复制按钮，因为它可能是延迟加载的
    let attempts = 0;
    const maxAttempts = 10;
    
    const moveButton = () => {
        const copyButton = highlight.querySelector('.md-clipboard');
        
        if (copyButton) {
            // 找到了复制按钮，将它移动到标题栏区域
            if (!clickArea.contains(copyButton)) {
                // 从原来的位置移除并添加到标题栏
                clickArea.appendChild(copyButton);
                
                // 显式设置样式确保对齐
                copyButton.style.position = 'relative';
                copyButton.style.display = 'flex';
                copyButton.style.alignItems = 'center';
                copyButton.style.justifyContent = 'center';
                copyButton.style.height = '24px';
                copyButton.style.lineHeight = '24px';
                copyButton.style.margin = '0';
                copyButton.style.verticalAlign = 'middle';
                
                // 确保复制按钮内部元素也正确对齐
                const copyButtonChildren = copyButton.querySelectorAll('*');
                copyButtonChildren.forEach(child => {
                    child.style.verticalAlign = 'middle';
                    child.style.display = 'inline-flex';
                    child.style.alignItems = 'center';
                    if (child.tagName.toLowerCase() === 'svg') {
                        child.style.margin = '0';
                    }
                });
                
                console.log('复制按钮已移动到标题栏内并设置对齐样式');
            }
        } else if (attempts < maxAttempts) {
            // 如果还没找到，继续尝试
            attempts++;
            setTimeout(moveButton, 100);
        }
    };
    
    // 立即尝试一次
    moveButton();
}

/**
 * 创建切换按钮
 * @returns {Element} 切换按钮元素
 */
function createToggleButton() {
    const button = document.createElement('div');
    button.className = 'code-toggle-btn';
    
    // 显式设置对齐样式
    button.style.display = 'flex';
    button.style.alignItems = 'center';
    button.style.justifyContent = 'center';
    button.style.height = '24px';
    button.style.lineHeight = '24px';
    button.style.verticalAlign = 'middle';
    
    button.innerHTML = `
        <svg class="toggle-icon collapse-icon" viewBox="0 0 24 24" width="16" height="16" style="display: block; vertical-align: middle;">
            <path d="M7 14l5-5 5 5z" fill="currentColor"/>
        </svg>
        <svg class="toggle-icon expand-icon" viewBox="0 0 24 24" width="16" height="16" style="display: none; vertical-align: middle;">
            <path d="M7 10l5 5 5-5z" fill="currentColor"/>
        </svg>
    `;
    return button;
}

/**
 * 创建标题栏点击区域
 * @returns {Element} 点击区域元素
 */
function createHeaderClickArea() {
    const area = document.createElement('div');
    area.className = 'code-header-click-area';
    
    // 显式设置flexbox布局确保按钮正确对齐
    area.style.display = 'flex';
    area.style.alignItems = 'center';
    area.style.justifyContent = 'flex-end';
    area.style.gap = '6px';
    
    return area;
}

/**
 * 获取代码内容区域
 * @param {Element} highlight 代码块容器
 * @returns {Element|null} 代码内容元素
 */
function getCodeContent(highlight) {
    // 优先查找 .highlighttable（带行号的代码块）
    let content = highlight.querySelector('.highlighttable');
    if (content) return content;
    
    // 其次查找 pre 元素
    content = highlight.querySelector('pre');
    if (content) return content;
    
    return null;
}

/**
 * 切换代码块显示/隐藏
 * @param {Element} highlight 代码块容器
 * @param {Element} codeContent 代码内容元素
 * @param {Element} toggleButton 切换按钮
 */
function toggleCodeBlock(highlight, codeContent, toggleButton) {
    const isCollapsed = highlight.classList.contains('collapsed');
    const clickArea = highlight.querySelector('.code-header-click-area');
    
    if (isCollapsed) {
        // 展开代码块
        expandCodeBlock(highlight, codeContent, toggleButton, clickArea);
    } else {
        // 折叠代码块
        collapseCodeBlock(highlight, codeContent, toggleButton, clickArea);
    }
    
    // 保存状态
    saveToggleState(highlight.id, !isCollapsed);
    
    // 触发自定义事件
    const event = new CustomEvent('codeBlockToggled', {
        detail: {
            id: highlight.id,
            collapsed: !isCollapsed,
            element: highlight
        }
    });
    document.dispatchEvent(event);
}

/**
 * 展开代码块
 */
function expandCodeBlock(highlight, codeContent, toggleButton, clickArea) {
    highlight.classList.remove('collapsed');
    
    // 更新按钮图标
    const collapseIcon = toggleButton.querySelector('.collapse-icon');
    const expandIcon = toggleButton.querySelector('.expand-icon');
    collapseIcon.style.display = 'block';
    expandIcon.style.display = 'none';
    
    // 更新可访问性属性
    clickArea.setAttribute('aria-expanded', 'true');
    
    // 获取内容高度并设置动画
    const height = codeContent.scrollHeight;
    codeContent.style.height = height + 'px';
    
    // 动画完成后移除固定高度
    setTimeout(() => {
        codeContent.style.height = 'auto';
    }, 300);
}

/**
 * 折叠代码块
 */
function collapseCodeBlock(highlight, codeContent, toggleButton, clickArea) {
    // 先设置当前高度
    const height = codeContent.scrollHeight;
    codeContent.style.height = height + 'px';
    
    // 强制重绘
    codeContent.offsetHeight;
    
    // 开始折叠动画
    codeContent.style.height = '0px';
    highlight.classList.add('collapsed');
    
    // 更新按钮图标
    const collapseIcon = toggleButton.querySelector('.collapse-icon');
    const expandIcon = toggleButton.querySelector('.expand-icon');
    collapseIcon.style.display = 'none';
    expandIcon.style.display = 'block';
    
    // 更新可访问性属性
    clickArea.setAttribute('aria-expanded', 'false');
}

/**
 * 添加全局控制按钮
 */
function addGlobalToggleControls() {
    // 检查是否已存在控制面板
    if (document.querySelector('.code-toggle-controls')) {
        return;
    }
    
    const controls = document.createElement('div');
    controls.className = 'code-toggle-controls';
    controls.innerHTML = `
        <div class="toggle-controls-inner">
            <span class="controls-label">代码块控制:</span>
            <button class="toggle-btn expand-all" title="展开所有代码块">
                <svg viewBox="0 0 24 24" width="16" height="16">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z" fill="currentColor"/>
                </svg>
                展开全部
            </button>
            <button class="toggle-btn collapse-all" title="折叠所有代码块">
                <svg viewBox="0 0 24 24" width="16" height="16">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11H7v-2h10v2z" fill="currentColor"/>
                </svg>
                折叠全部
            </button>
        </div>
    `;
    
    // 添加到页面顶部
    const content = document.querySelector('.md-content__inner');
    if (content) {
        content.insertBefore(controls, content.firstChild);
        
        // 绑定全局控制事件
        controls.querySelector('.expand-all').addEventListener('click', expandAllCodeBlocks);
        controls.querySelector('.collapse-all').addEventListener('click', collapseAllCodeBlocks);
    }
}

/**
 * 展开所有代码块
 */
function expandAllCodeBlocks() {
    const highlights = document.querySelectorAll('.highlight.toggleable');
    highlights.forEach(highlight => {
        if (highlight.classList.contains('collapsed')) {
            const clickArea = highlight.querySelector('.code-header-click-area');
            if (clickArea) {
                clickArea.click();
            }
        }
    });
}

/**
 * 折叠所有代码块
 */
function collapseAllCodeBlocks() {
    const highlights = document.querySelectorAll('.highlight.toggleable');
    highlights.forEach(highlight => {
        if (!highlight.classList.contains('collapsed')) {
            const clickArea = highlight.querySelector('.code-header-click-area');
            if (clickArea) {
                clickArea.click();
            }
        }
    });
}

/**
 * 保存折叠状态到本地存储
 * @param {string} id 代码块ID
 * @param {boolean} collapsed 是否折叠
 */
function saveToggleState(id, collapsed) {
    try {
        const states = JSON.parse(localStorage.getItem('codeBlockStates') || '{}');
        states[id] = collapsed;
        localStorage.setItem('codeBlockStates', JSON.stringify(states));
    } catch (e) {
        console.warn('无法保存代码块状态:', e);
    }
}

/**
 * 检查Markdown中的折叠标记
 * @param {Element} highlight 代码块容器
 * @returns {boolean} 是否应该初始折叠
 */
function checkMarkdownCollapseMarkers(highlight) {
    // 方法1: 检查文件名中的标记 (title="file.py collapsed")
    const filenameElement = highlight.querySelector('span.filename');
    if (filenameElement) {
        const filename = filenameElement.textContent || '';
        if (filename.includes('collapsed') || filename.includes('hidden') || 
            filename.includes('fold') || filename.includes('minimize')) {
            return true;
        }
    }
    
    // 方法2: 检查代码块的类名
    const classList = Array.from(highlight.classList);
    if (classList.some(cls => ['collapsed', 'hidden', 'fold', 'minimize'].includes(cls))) {
        return true;
    }
    
    // 方法3: 检查data属性
    if (highlight.hasAttribute('data-collapsed') || 
        highlight.hasAttribute('data-hidden') ||
        highlight.hasAttribute('data-fold')) {
        return true;
    }
    
    // 方法4: 检查注释标记（在代码内容中查找特殊注释）
    const codeElement = highlight.querySelector('code');
    if (codeElement) {
        const codeText = codeElement.textContent || '';
        const firstLine = codeText.split('\n')[0];
        if (firstLine.includes('<!-- collapsed -->') || 
            firstLine.includes('# collapsed') ||
            firstLine.includes('// collapsed') ||
            firstLine.includes('/* collapsed */')) {
            return true;
        }
    }
    
    // 方法5: 检查代码块容器的data-lang属性是否包含折叠标记
    const dataLang = highlight.getAttribute('data-lang');
    if (dataLang && (dataLang.includes('collapsed') || dataLang.includes('hidden'))) {
        return true;
    }
    
    return false;
}

/**
 * 从本地存储恢复折叠状态
 */
function restoreToggleStates() {
    try {
        const states = JSON.parse(localStorage.getItem('codeBlockStates') || '{}');
        
        // 处理所有代码块
        const highlights = document.querySelectorAll('.highlight.toggleable');
        highlights.forEach(highlight => {
            const id = highlight.id;
            const hasStoredState = states[id] !== undefined;
            const shouldCollapse = hasStoredState ? states[id] : highlight.hasAttribute('data-initial-collapse');
            
            if (shouldCollapse) {
                // 延迟执行以确保DOM完全加载
                setTimeout(() => {
                    const clickArea = highlight.querySelector('.code-header-click-area');
                    if (clickArea && !highlight.classList.contains('collapsed')) {
                        clickArea.click();
                    }
                }, 150);
            }
        });
    } catch (e) {
        console.warn('无法恢复代码块状态:', e);
    }
}

/**
 * 清除所有保存的状态
 */
function clearToggleStates() {
    try {
        localStorage.removeItem('codeBlockStates');
    } catch (e) {
        console.warn('无法清除代码块状态:', e);
    }
}

/**
 * 重新初始化（用于动态内容）
 */
function reinitCodeBlockToggle() {
    // 清除现有控制面板
    const existingControls = document.querySelector('.code-toggle-controls');
    if (existingControls) {
        existingControls.remove();
    }
    
    // 重新初始化
    initCodeBlockToggle();
}

// 导出到全局对象
window.CodeBlockToggle = {
    init: initCodeBlockToggle,
    reinit: reinitCodeBlockToggle,
    expandAll: expandAllCodeBlocks,
    collapseAll: collapseAllCodeBlocks,
    clearStates: clearToggleStates
};

// 监听页面导航（SPA支持）
document.addEventListener('DOMContentLoaded', function() {
    // 监听MkDocs Material的页面切换
    if (typeof app !== 'undefined' && app.document$) {
        app.document$.subscribe(() => {
            setTimeout(reinitCodeBlockToggle, 100);
        });
    }
});
