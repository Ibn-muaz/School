// UI utilities and components
class UI {
    static showToast(message, type = 'info', duration = 5000) {
        const toastContainer = document.getElementById('toast-container');

        const toast = document.createElement('div');
        toast.className = `toast toast-${type} fade-in`;

        const toastContent = document.createElement('div');
        toastContent.className = 'toast-content';

        const title = document.createElement('div');
        title.className = 'toast-title';
        title.textContent = this.getToastTitle(type);

        const messageEl = document.createElement('div');
        messageEl.className = 'toast-message';
        messageEl.textContent = message;

        toastContent.appendChild(title);
        toastContent.appendChild(messageEl);
        toast.appendChild(toastContent);

        toastContainer.appendChild(toast);

        // Auto remove after duration
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-in-out';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, duration);

        // Click to dismiss
        toast.addEventListener('click', () => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        });
    }

    static getToastTitle(type) {
        const titles = {
            success: 'Success',
            error: 'Error',
            warning: 'Warning',
            info: 'Information'
        };
        return titles[type] || 'Notification';
    }

    static showModal(title, content, footer = null) {
        const modal = document.getElementById('modal-overlay');
        const modalContent = document.getElementById('modal-content');

        modalContent.innerHTML = '';

        // Header
        const header = document.createElement('div');
        header.className = 'modal-header';

        const titleEl = document.createElement('h3');
        titleEl.className = 'modal-title';
        titleEl.textContent = title;

        const closeBtn = document.createElement('button');
        closeBtn.className = 'text-gray-400 hover:text-gray-600';
        closeBtn.innerHTML = '<i data-lucide="x" class="w-6 h-6"></i>';
        closeBtn.onclick = () => this.hideModal();

        header.appendChild(titleEl);
        header.appendChild(closeBtn);

        // Body
        const body = document.createElement('div');
        body.className = 'modal-body';
        body.innerHTML = content;

        // Footer
        let footerEl = null;
        if (footer) {
            footerEl = document.createElement('div');
            footerEl.className = 'modal-footer';
            footerEl.innerHTML = footer;
        }

        modalContent.appendChild(header);
        modalContent.appendChild(body);
        if (footerEl) {
            modalContent.appendChild(footerEl);
        }

        modal.classList.remove('hidden');

        // Re-initialize Lucide icons
        lucide.createIcons();
    }

    static hideModal() {
        const modal = document.getElementById('modal-overlay');
        modal.classList.add('hidden');
    }

    static showLoading(buttonId, text = 'Loading...') {
        const button = document.getElementById(buttonId);
        if (!button) return;

        const originalText = button.innerHTML;
        button.disabled = true;
        button.innerHTML = `
            <div class="flex items-center">
                <div class="spinner mr-2"></div>
                ${text}
            </div>
        `;

        return () => {
            button.disabled = false;
            button.innerHTML = originalText;
        };
    }

    static createTable(headers, data, actions = null) {
        const table = document.createElement('div');
        table.className = 'overflow-x-auto';

        const tableEl = document.createElement('table');
        tableEl.className = 'table';

        // Header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');

        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });

        if (actions) {
            const th = document.createElement('th');
            th.textContent = 'Actions';
            headerRow.appendChild(th);
        }

        thead.appendChild(headerRow);
        tableEl.appendChild(thead);

        // Body
        const tbody = document.createElement('tbody');

        data.forEach((row, index) => {
            const tr = document.createElement('tr');

            headers.forEach(header => {
                const td = document.createElement('td');
                const key = header.toLowerCase().replace(/\s+/g, '_');
                td.textContent = row[key] || '';
                tr.appendChild(td);
            });

            if (actions) {
                const td = document.createElement('td');
                td.innerHTML = actions(row, index);
                tr.appendChild(td);
            }

            tbody.appendChild(tr);
        });

        tableEl.appendChild(tbody);
        table.appendChild(tableEl);

        return table;
    }

    static createForm(fields, onSubmit, submitText = 'Submit') {
        const form = document.createElement('form');
        form.className = 'space-y-4';

        fields.forEach(field => {
            const formGroup = document.createElement('div');
            formGroup.className = 'form-group';

            const label = document.createElement('label');
            label.className = 'form-label';
            label.textContent = field.label;
            label.setAttribute('for', field.name);

            let input;
            if (field.type === 'textarea') {
                input = document.createElement('textarea');
                input.className = 'form-textarea';
                if (field.rows) input.rows = field.rows;
            } else if (field.type === 'select') {
                input = document.createElement('select');
                input.className = 'form-select';
                if (field.options) {
                    field.options.forEach(option => {
                        const optionEl = document.createElement('option');
                        optionEl.value = option.value;
                        optionEl.textContent = option.label;
                        input.appendChild(optionEl);
                    });
                }
            } else {
                input = document.createElement('input');
                input.className = 'form-input';
                input.type = field.type || 'text';
                if (field.placeholder) input.placeholder = field.placeholder;
            }

            input.id = field.name;
            input.name = field.name;
            if (field.required) input.required = true;
            if (field.value) input.value = field.value;

            formGroup.appendChild(label);
            formGroup.appendChild(input);
            form.appendChild(formGroup);
        });

        // Submit button
        const submitBtn = document.createElement('button');
        submitBtn.type = 'submit';
        submitBtn.className = 'btn btn-primary';
        submitBtn.textContent = submitText;

        form.appendChild(submitBtn);

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            onSubmit(data);
        });

        return form;
    }

    static createCard(title, content, className = '') {
        const card = document.createElement('div');
        card.className = `card ${className}`;

        if (title) {
            const header = document.createElement('div');
            header.className = 'card-header';

            const titleEl = document.createElement('h3');
            titleEl.className = 'card-title';
            titleEl.textContent = title;

            header.appendChild(titleEl);
            card.appendChild(header);
        }

        const contentEl = document.createElement('div');
        contentEl.className = 'card-content';
        if (typeof content === 'string') {
            contentEl.innerHTML = content;
        } else {
            contentEl.appendChild(content);
        }

        card.appendChild(contentEl);

        return card;
    }

    static createStatCard(value, label, change = null, changeType = 'positive') {
        const card = document.createElement('div');
        card.className = 'stat-card';

        const valueEl = document.createElement('div');
        valueEl.className = 'stat-value';
        valueEl.textContent = value;

        const labelEl = document.createElement('div');
        labelEl.className = 'stat-label';
        labelEl.textContent = label;

        card.appendChild(valueEl);
        card.appendChild(labelEl);

        if (change) {
            const changeEl = document.createElement('div');
            changeEl.className = `stat-change ${changeType}`;
            changeEl.textContent = change;
            card.appendChild(changeEl);
        }

        return card;
    }

    static formatCurrency(amount) {
        return new Intl.NumberFormat('en-NG', {
            style: 'currency',
            currency: 'NGN',
        }).format(amount);
    }

    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        });
    }

    static formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    }

    static createBadge(text, type = 'secondary') {
        const badge = document.createElement('span');
        badge.className = `badge badge-${type}`;
        badge.textContent = text;
        return badge;
    }

    static createButton(text, onClick, className = 'btn-primary', icon = null) {
        const button = document.createElement('button');
        button.className = `btn ${className}`;

        if (icon) {
            const iconEl = document.createElement('i');
            iconEl.setAttribute('data-lucide', icon);
            iconEl.className = 'w-4 h-4 mr-2';
            button.appendChild(iconEl);
        }

        const textEl = document.createElement('span');
        textEl.textContent = text;
        button.appendChild(textEl);

        button.addEventListener('click', onClick);

        return button;
    }
}