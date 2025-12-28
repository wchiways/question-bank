// ========================================
// 工具函数
// ========================================

// 复制代码
function copyCode(button) {
    const codeBlock = button.parentElement;
    const code = codeBlock.querySelector('code');
    const text = code.textContent;

    navigator.clipboard.writeText(text).then(() => {
        button.textContent = '已复制!';
        setTimeout(() => {
            button.textContent = '复制';
        }, 2000);
    }).catch(err => {
        console.error('复制失败:', err);
        button.textContent = '复制失败';
        setTimeout(() => {
            button.textContent = '复制';
        }, 2000);
    });
}

// 格式化时间
function formatTime(ms) {
    if (ms < 1000) {
        return `${ms}ms`;
    } else {
        return `${(ms / 1000).toFixed(2)}s`;
    }
}

// ========================================
// 导航栏滚动效果
// ========================================

let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
});

// ========================================
// 平滑滚动
// ========================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ========================================
// 查询表单处理
// ========================================

const queryForm = document.getElementById('queryForm');
const resultBox = document.getElementById('result');

if (queryForm) {
    queryForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const title = document.getElementById('title').value;
        const options = document.getElementById('options').value;
        const type = document.getElementById('type').value;

        // 显示加载状态
        const submitButton = queryForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.innerHTML;
        submitButton.innerHTML = `
            <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32" class="animate-spin"/>
            </svg>
            查询中...
        `;
        submitButton.disabled = true;

        // 隐藏之前的结果
        resultBox.style.display = 'none';

        const startTime = Date.now();

        try {
            // 构建查询URL
            const params = new URLSearchParams({
                title: title,
                options: options,
                type: type
            });

            // 发送请求
            const response = await fetch(`/api/v1/query?${params.toString()}`);
            const data = await response.json();

            const latency = Date.now() - startTime;

            // 显示结果
            resultBox.style.display = 'block';
            const resultHeader = resultBox.querySelector('.result-header');
            const resultContent = resultBox.querySelector('.result-content');
            const resultLatency = resultBox.querySelector('.result-latency');

            resultLatency.textContent = `响应时间: ${formatTime(latency)}`;

            if (data.code === 1) {
                resultContent.innerHTML = `
                    <div class="text-success">
                        <strong>✓ 查询成功</strong><br>
                        <span style="font-size: 1.5rem; margin-top: 0.5rem; display: block;">${data.data}</span>
                        ${data.source ? `<span style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem; display: block;">来源: ${data.source}</span>` : ''}
                    </div>
                `;
            } else {
                resultContent.innerHTML = `
                    <div class="text-error">
                        <strong>✗ 查询失败</strong><br>
                        <span style="margin-top: 0.5rem; display: block;">${data.msg || '未知错误'}</span>
                    </div>
                `;
            }

            // 滚动到结果
            resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        } catch (error) {
            console.error('查询失败:', error);

            resultBox.style.display = 'block';
            const resultContent = resultBox.querySelector('.result-content');
            const resultLatency = resultBox.querySelector('.result-latency');

            resultLatency.textContent = '';
            resultContent.innerHTML = `
                <div class="text-error">
                    <strong>✗ 网络错误</strong><br>
                    <span style="margin-top: 0.5rem; display: block;">${error.message}</span>
                    <span style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem; display: block;">请检查服务器是否正常运行</span>
                </div>
            `;
        } finally {
            // 恢复按钮状态
            submitButton.innerHTML = originalButtonText;
            submitButton.disabled = false;
        }
    });
}

// ========================================
// 添加动画CSS
// ========================================

const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        from {
            transform: rotate(0deg);
            stroke-dashoffset: 32;
        }
        to {
            transform: rotate(360deg);
            stroke-dashoffset: 0;
        }
    }

    .spinner {
        animation: spin 1s linear infinite;
    }

    .spinner circle {
        stroke-dasharray: 32;
        stroke-dashoffset: 32;
    }
`;
document.head.appendChild(style);

// ========================================
// 添加示例数据（可选）
// ========================================

// 可以预填一些示例数据方便测试
const exampleData = {
    title: '中国的首都是哪里？',
    options: 'A.北京 B.上海 C.广州 D.深圳',
    type: 'single'
};

// 取消下面的注释来启用示例数据预填
// document.getElementById('title').value = exampleData.title;
// document.getElementById('options').value = exampleData.options;
// document.getElementById('type').value = exampleData.type;

// ========================================
// 页面加载动画
// ========================================

window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.3s ease';
        document.body.style.opacity = '1';
    }, 100);
});

// ========================================
// 控制台彩蛋
// ========================================

console.log(
    '%c🚀 OCS题库系统',
    'font-size: 24px; font-weight: bold; color: #6366f1;'
);
console.log(
    '%c版本: 1.2.1',
    'font-size: 14px; color: #9ca3af;'
);
console.log(
    '%cGitHub: https://github.com/wchiways/question-bank',
    'font-size: 12px; color: #9ca3af;'
);
console.log('%c欢迎使用OCS题库系统！', 'font-size: 14px; color: #10b981;');
