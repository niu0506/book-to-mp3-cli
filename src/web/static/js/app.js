// 应用状态管理
const state = {
    currentFile: null,
    batchFiles: [],
    currentTaskId: null,
    ws: null
};

// 工具函数
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');

    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
}

// 面板切换
function switchPanel(panelName) {
    document.querySelectorAll('.panel').forEach(panel => {
        panel.classList.remove('active');
    });

    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    document.getElementById(`${panelName}-panel`).classList.add('active');
    document.querySelector(`[data-panel="${panelName}"]`).classList.add('active');

    if (panelName === 'history') {
        loadHistory();
    }
}

// 单文件上传处理
function handleSingleFileUpload(file) {
    state.currentFile = file;

    document.getElementById('single-file-name').textContent = file.name;
    document.getElementById('single-file-size').textContent = formatFileSize(file.size);
    document.getElementById('single-file-info').classList.remove('hidden');
    document.getElementById('single-upload-zone').classList.add('hidden');

    showToast(`已选择文件: ${file.name}`, 'success');
}

// 批量文件上传处理
function handleBatchFilesUpload(files) {
    Array.from(files).forEach(file => {
        state.batchFiles.push(file);
    });

    updateBatchFileList();
    showToast(`已添加 ${files.length} 个文件`, 'success');
}

// 更新批量文件列表
function updateBatchFileList() {
    const container = document.getElementById('batch-file-list');
    container.innerHTML = '';

    state.batchFiles.forEach((file, index) => {
        const item = document.createElement('div');
        item.className = 'file-list-item';
        item.innerHTML = `
            <span>${file.name} (${formatFileSize(file.size)})</span>
            <button class="remove-btn" onclick="removeBatchFile(${index})">删除</button>
        `;
        container.appendChild(item);
    });
}

// 删除批量文件
function removeBatchFile(index) {
    state.batchFiles.splice(index, 1);
    updateBatchFileList();
}

// 上传文件到服务器
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error('上传失败');
    }

    return await response.json();
}

// 批量上传文件
async function uploadBatchFiles(files) {
    const formData = new FormData();
    files.forEach(file => {
        formData.append('files', file);
    });

    const response = await fetch('/api/upload-batch', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error('批量上传失败');
    }

    return await response.json();
}

// 开始单文件转换
async function startSingleConversion() {
    if (!state.currentFile) {
        showToast('请先选择文件', 'error');
        return;
    }

    try {
        // 上传文件
        const uploadResult = await uploadFile(state.currentFile);

        // 开始转换
        const fileNameWithoutExt = uploadResult.file_name ? uploadResult.file_name.replace(/\.[^/.]+$/, '') : state.currentFile.name.replace(/\.[^/.]+$/, '');
        console.log('Upload result:', uploadResult);
        console.log('Original name:', fileNameWithoutExt);
        
        const convertResponse = await fetch('/api/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_id: uploadResult.file_id,
                original_name: fileNameWithoutExt,
                voice: document.getElementById('voice-select').value,
                bitrate: document.getElementById('bitrate-select').value,
                segment_length: parseInt(document.getElementById('segment-length').value),
                output_name: document.getElementById('output-name').value || null
            })
        });

        if (!convertResponse.ok) {
            throw new Error('转换失败');
        }

        const convertResult = await convertResponse.json();
        state.currentTaskId = convertResult.task_id;

        // 显示进度面板
        document.getElementById('single-progress-panel').classList.remove('hidden');
        document.getElementById('single-convert-btn').disabled = true;

        // 连接WebSocket
        connectWebSocket(state.currentTaskId);

        showToast('转换已开始', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// 开始批量转换
async function startBatchConversion() {
    if (state.batchFiles.length === 0) {
        showToast('请先选择文件', 'error');
        return;
    }

    try {
        // 上传所有文件
        const uploadResult = await uploadBatchFiles(state.batchFiles);

        // 开始批量转换
        const convertResponse = await fetch('/api/convert-batch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_ids: uploadResult.files.map(f => f.file_id),
                voice: document.getElementById('batch-voice-select').value,
                bitrate: document.getElementById('batch-bitrate-select').value,
                segment_length: parseInt(document.getElementById('batch-segment-length').value)
            })
        });

        if (!convertResponse.ok) {
            throw new Error('批量转换失败');
        }

        const convertResult = await convertResponse.json();
        state.batchTaskIds = convertResult.task_ids;

        // 显示任务队列面板
        document.getElementById('batch-tasks-panel').classList.remove('hidden');
        document.getElementById('batch-convert-btn').disabled = true;

        // 为每个任务创建UI并连接WebSocket
        updateBatchTasksPanel();

        showToast('批量转换已开始', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// 更新批量任务面板
function updateBatchTasksPanel() {
    const container = document.getElementById('batch-tasks-list');
    container.innerHTML = '';

    state.batchFiles.forEach((file, index) => {
        if (state.batchTaskIds && state.batchTaskIds[index]) {
            const taskId = state.batchTaskIds[index];
            const card = document.createElement('div');
            card.className = 'task-card';
            card.id = `task-${taskId}`;
            card.innerHTML = `
                <h4>${file.name}</h4>
                <div class="progress-bar" style="margin-top: 10px;">
                    <div class="progress-fill" style="width: 0%;"></div>
                </div>
                <p style="margin-top: 5px;">进度: 0%</p>
            `;
            container.appendChild(card);

            // 连接WebSocket
            connectWebSocket(taskId);
        }
    });
}

// 连接WebSocket
function connectWebSocket(taskId) {
    const ws = new WebSocket(`ws://${window.location.host}/ws/progress/${taskId}`);

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === 'progress') {
            updateProgress(taskId, data);
        } else if (data.type === 'complete') {
            handleComplete(taskId, data);
        } else if (data.type === 'error') {
            handleError(taskId, data);
        }
    };

    ws.onerror = () => {
        showToast('WebSocket连接错误', 'error');
    };
}

// 更新进度
function updateProgress(taskId, data) {
    if (taskId === state.currentTaskId) {
        // 单文件转换进度
        document.getElementById('progress-fill').style.width = `${data.progress}%`;
        document.getElementById('progress-percent').textContent = data.progress;
        document.getElementById('current-segment').textContent = data.current_segment;
        document.getElementById('total-segments').textContent = data.total_segments;
        document.getElementById('current-text').textContent = data.current_text_preview || '--';
    } else {
        // 批量转换进度
        const card = document.getElementById(`task-${taskId}`);
        if (card) {
            const progressFill = card.querySelector('.progress-fill');
            const progressText = card.querySelector('p');
            progressFill.style.width = `${data.progress}%`;
            progressText.textContent = `进度: ${data.progress}%`;
        }
    }
}

// 处理完成
function handleComplete(taskId, data) {
    if (taskId === state.currentTaskId) {
        // 单文件转换完成
        document.getElementById('single-progress-panel').classList.add('hidden');
        document.getElementById('single-download-panel').classList.remove('hidden');
        document.getElementById('single-download-btn').onclick = () => {
            window.location.href = `/api/download/${taskId}`;
        };
        document.getElementById('download-file-name').textContent = data.output_file;
        document.getElementById('single-convert-btn').disabled = false;

        showToast('转换完成！', 'success');
    } else {
        // 批量转换中的某个任务完成
        const card = document.getElementById(`task-${taskId}`);
        if (card) {
            card.innerHTML += `<p><strong>✓ 转换完成</strong></p>`;
            card.style.borderLeftColor = '#28a745';
        }

        // 检查是否所有任务都完成了
        const allCompleted = state.batchTaskIds.every(id => {
            const card = document.getElementById(`task-${id}`);
            return card && card.innerHTML.includes('转换完成');
        });

        if (allCompleted) {
            document.getElementById('batch-convert-btn').disabled = false;
            showToast('批量转换完成！', 'success');
        }
    }
}

// 处理错误
function handleError(taskId, data) {
    showToast(`转换失败: ${data.error}`, 'error');

    if (taskId === state.currentTaskId) {
        document.getElementById('single-progress-panel').classList.add('hidden');
        document.getElementById('single-convert-btn').disabled = false;
    } else {
        const card = document.getElementById(`task-${taskId}`);
        if (card) {
            card.innerHTML += `<p style="color: #dc3545;"><strong>✗ 转换失败: ${data.error}</strong></p>`;
            card.style.borderLeftColor = '#dc3545';
        }
    }
}

// 加载历史记录
async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();

        const tbody = document.querySelector('#history-table tbody');
        tbody.innerHTML = '';

        data.tasks.forEach(task => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${task.file_name}</td>
                <td>${formatDateTime(task.created_at)}</td>
                <td><span class="status-badge status-${task.status}">${task.status}</span></td>
                <td>
                    ${task.status === 'completed' ? `<button class="action-btn download-action-btn" onclick="downloadFile('${task.task_id}')">下载</button>` : ''}
                    <button class="action-btn delete-action-btn" onclick="deleteHistory('${task.task_id}')">删除</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        showToast('加载历史记录失败', 'error');
    }
}

// 下载文件
function downloadFile(taskId) {
    window.location.href = `/api/download/${taskId}`;
}

// 删除历史记录
async function deleteHistory(taskId) {
    if (!confirm('确定要删除这条记录吗？')) {
        return;
    }

    try {
        const response = await fetch(`/api/history/${taskId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('删除失败');
        }

        showToast('删除成功', 'success');
        loadHistory();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// 清空历史记录
async function clearHistory() {
    if (!confirm('确定要清空所有历史记录吗？')) {
        return;
    }

    try {
        const response = await fetch('/api/history');
        const data = await response.json();

        for (const task of data.tasks) {
            await fetch(`/api/history/${task.task_id}`, {
                method: 'DELETE'
            });
        }

        showToast('历史记录已清空', 'success');
        loadHistory();
    } catch (error) {
        showToast('清空历史记录失败', 'error');
    }
}

// 事件监听
document.addEventListener('DOMContentLoaded', () => {
    // 导航按钮
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            switchPanel(btn.dataset.panel);
        });
    });

    // 单文件上传区域
    const singleUploadZone = document.getElementById('single-upload-zone');
    const singleFileInput = document.getElementById('single-file-input');

    singleUploadZone.addEventListener('click', () => {
        singleFileInput.click();
    });

    singleUploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        singleUploadZone.style.borderColor = '#667eea';
    });

    singleUploadZone.addEventListener('dragleave', () => {
        singleUploadZone.style.borderColor = '#ddd';
    });

    singleUploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        singleUploadZone.style.borderColor = '#ddd';

        if (e.dataTransfer.files.length > 0) {
            handleSingleFileUpload(e.dataTransfer.files[0]);
        }
    });

    singleFileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleSingleFileUpload(e.target.files[0]);
        }
    });

    // 删除单文件
    document.getElementById('single-remove-btn').addEventListener('click', () => {
        state.currentFile = null;
        document.getElementById('single-file-info').classList.add('hidden');
        document.getElementById('single-upload-zone').classList.remove('hidden');
        document.getElementById('single-file-input').value = '';
    });

    // 批量上传区域
    const batchUploadZone = document.getElementById('batch-upload-zone');
    const batchFileInput = document.getElementById('batch-file-input');

    batchUploadZone.addEventListener('click', () => {
        batchFileInput.click();
    });

    batchUploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        batchUploadZone.style.borderColor = '#667eea';
    });

    batchUploadZone.addEventListener('dragleave', () => {
        batchUploadZone.style.borderColor = '#ddd';
    });

    batchUploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        batchUploadZone.style.borderColor = '#ddd';

        if (e.dataTransfer.files.length > 0) {
            handleBatchFilesUpload(e.dataTransfer.files);
        }
    });

    batchFileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleBatchFilesUpload(e.target.files);
        }
    });

    // 分段长度滑块
    document.getElementById('segment-length').addEventListener('input', (e) => {
        document.getElementById('segment-length-value').textContent = e.target.value;
    });

    document.getElementById('batch-segment-length').addEventListener('input', (e) => {
        document.getElementById('batch-segment-length-value').textContent = e.target.value;
    });

    // 转换按钮
    document.getElementById('single-convert-btn').addEventListener('click', startSingleConversion);
    document.getElementById('batch-convert-btn').addEventListener('click', startBatchConversion);

    // 历史记录按钮
    document.getElementById('refresh-history-btn').addEventListener('click', loadHistory);
    document.getElementById('clear-history-btn').addEventListener('click', clearHistory);
});