// DocTrac - JavaScript Principal

$(document).ready(function() {
    // Configuración global de CSRF para AJAX
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    // Funciones de utilidad
    window.DocTrac = {
        // Mostrar notificaciones
        showNotification: function(message, type = 'info', duration = 5000) {
            const alertClass = this.getAlertClass(type);
            const icon = this.getIcon(type);
            
            const alert = $(`
                <div class="alert ${alertClass} alert-dismissible fade show position-fixed" 
                     role="alert" style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
                    <i class="fas ${icon} me-2"></i>${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `);
            
            $('body').append(alert);
            
            // Auto-ocultar
            setTimeout(function() {
                alert.fadeOut(function() {
                    $(this).remove();
                });
            }, duration);
            
            return alert;
        },
        
        getAlertClass: function(type) {
            const classes = {
                'success': 'alert-success',
                'error': 'alert-danger',
                'warning': 'alert-warning',
                'info': 'alert-info'
            };
            return classes[type] || 'alert-info';
        },
        
        getIcon: function(type) {
            const icons = {
                'success': 'fa-check-circle',
                'error': 'fa-exclamation-circle',
                'warning': 'fa-exclamation-triangle',
                'info': 'fa-info-circle'
            };
            return icons[type] || 'fa-info-circle';
        },
        
        // Confirmar acción
        confirmAction: function(message, callback) {
            if (confirm(message)) {
                callback();
            }
        },
        
        // Loading spinner
        showLoading: function(element) {
            const spinner = '<span class="spinner me-2"></span>';
            const $el = $(element);
            $el.data('original-html', $el.html());
            $el.html(spinner + 'Cargando...').prop('disabled', true);
        },
        
        hideLoading: function(element) {
            const $el = $(element);
            $el.html($el.data('original-html')).prop('disabled', false);
        },
        
        // Formatear fecha
        formatDate: function(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('es-MX');
        },
        
        // Formatear tamaño de archivo
        formatFileSize: function(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },
        
        // Truncar texto
        truncateText: function(text, maxLength) {
            if (text.length <= maxLength) return text;
            return text.substring(0, maxLength) + '...';
        },
        
        // Debounce function
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
    };
    
    // Mejorar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-ocultar alertas después de 5 segundos
    $('.alert:not(.alert-permanent)').each(function() {
        const alert = $(this);
        setTimeout(function() {
            alert.fadeOut();
        }, 5000);
    });
    
    // Mejorar experiencia de forms
    $('form').on('submit', function() {
        $(this).find('button[type="submit"]').each(function() {
            DocTrac.showLoading(this);
        });
    });
    
    // Validación en tiempo real para campos requeridos
    $('input[required], select[required], textarea[required]').on('blur', function() {
        const $this = $(this);
        if (!$this.val()) {
            $this.addClass('is-invalid');
        } else {
            $this.removeClass('is-invalid').addClass('is-valid');
        }
    });
    
    // Limpiar validación al escribir
    $('input, select, textarea').on('input change', function() {
        $(this).removeClass('is-invalid is-valid');
    });
    
    // Funcionalidad de búsqueda con debounce
    $('input[name="search"]').on('input', DocTrac.debounce(function() {
        const searchTerm = $(this).val();
        if (searchTerm.length > 2 || searchTerm.length === 0) {
            // Aquí se podría implementar búsqueda en tiempo real
            console.log('Buscando:', searchTerm);
        }
    }, 500));
    
    // Confirmar acciones destructivas
    $('[data-confirm]').on('click', function(e) {
        e.preventDefault();
        const message = $(this).data('confirm');
        const href = $(this).attr('href');
        
        DocTrac.confirmAction(message, function() {
            window.location.href = href;
        });
    });
    
    // Copiar texto al clipboard
    $('[data-clipboard]').on('click', function() {
        const text = $(this).data('clipboard');
        navigator.clipboard.writeText(text).then(function() {
            DocTrac.showNotification('Texto copiado al portapapeles', 'success');
        });
    });
    
    // Mejorar dropdowns dependientes
    $('.dependent-dropdown').on('change', function() {
        const dependentId = $(this).data('dependent');
        const url = $(this).data('url');
        const value = $(this).val();
        
        if (dependentId && url && value) {
            const $dependent = $('#' + dependentId);
            $dependent.prop('disabled', true).html('<option>Cargando...</option>');
            
            $.get(url, {[$(this).attr('name')]: value})
                .done(function(data) {
                    $dependent.empty();
                    if (data.options) {
                        data.options.forEach(function(option) {
                            $dependent.append(`<option value="${option.value}">${option.text}</option>`);
                        });
                    }
                    $dependent.prop('disabled', false);
                })
                .fail(function() {
                    DocTrac.showNotification('Error al cargar opciones', 'error');
                    $dependent.prop('disabled', false);
                });
        }
    });
    
    // Lazy loading para imágenes
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Keyboard shortcuts
    $(document).on('keydown', function(e) {
        // Ctrl/Cmd + S para guardar formularios
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const $form = $('form:visible').first();
            if ($form.length) {
                $form.submit();
            }
        }
        
        // Escape para cerrar modales
        if (e.key === 'Escape') {
            $('.modal.show').modal('hide');
        }
    });
    
    // Smooth scroll para enlaces internos
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        const target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 500);
        }
    });
    
    // Funcionalidad específica del dashboard
    if ($('#dashboard').length || $('.document-item').length) {
        initDashboard();
    }
    
    function initDashboard() {
        let currentDocumentId = null;
        
        // Manejar selección de documentos
        $(document).on('click', '.document-item', function() {
            const documentId = $(this).data('document-id');
            
            if (documentId === currentDocumentId) return;
            
            // Actualizar UI
            $('.document-item').removeClass('active');
            $(this).addClass('active');
            
            // Cargar documento
            loadDocument(documentId);
        });
        
        function loadDocument(documentId) {
            currentDocumentId = documentId;
            
            // Mostrar formulario de categorización
            $('#no-document-selected').hide();
            $('#categorization-form').show().addClass('fade-in');
            
            // Cargar PDF en viewer
            const pdfUrl = `/documents/${documentId}/serve/`;
            $('#pdf-viewer-container').html(`
                <iframe src="${pdfUrl}" 
                        width="100%" height="100%" 
                        style="min-height: 70vh; border: none; border-radius: 0.375rem;">
                    <p>Tu navegador no soporta la vista previa de PDF. 
                       <a href="${pdfUrl}" target="_blank">Abrir en nueva ventana</a></p>
                </iframe>
            `);
            
            // Actualizar formulario con datos del documento
            $('#current-document-id').val(documentId);
            
            // Actualizar título en header
            const title = $(`.document-item[data-document-id="${documentId}"] h6`).text();
            $('#document-title').text(title);
            
            // Mostrar botón de historial
            $('#view-history-btn').show().attr('href', `/documents/${documentId}/`);
        }
        
        // Actualizar nombre estructurado en tiempo real
        $('#category, #document-type, #person, #document-date').on('change', function() {
            updateStructuredName();
        });
        
        function updateStructuredName() {
            const date = $('#document-date').val();
            const personText = $('#person option:selected').text();
            const typeText = $('#document-type option:selected').text();
            const categoryText = $('#category option:selected').text();
            
            let parts = [];
            
            if (date) {
                parts.push(date.replace(/-/g, ''));
            }
            if (personText && personText !== 'Seleccionar...') {
                parts.push(personText.replace(/\s+/g, '_').split('(')[0].trim());
            }
            if (typeText && typeText !== 'Seleccionar tipo...') {
                parts.push(typeText.replace(/\s+/g, '_'));
            }
            if (categoryText && categoryText !== 'Seleccionar categoría...') {
                parts.push(categoryText.replace(/\s+/g, '_'));
            }
            
            const structuredName = parts.length > 0 ? parts.join('_') : 'Documento_sin_categorizar';
            $('#structured-name').text(structuredName);
        }
    }
    
    console.log('DocTrac JavaScript inicializado correctamente');
});

// Funciones globales disponibles en window
window.loadDocumentTypes = function(categoryId, targetSelect) {
    const $target = $(targetSelect);
    
    if (!categoryId) {
        $target.html('<option value="">Primero selecciona categoría...</option>').prop('disabled', true);
        return;
    }
    
    $target.html('<option value="">Cargando tipos...</option>').prop('disabled', true);
    
    $.get('/documents/api/document-types/', {category_id: categoryId})
        .done(function(data) {
            $target.html('<option value="">Seleccionar tipo...</option>');
            
            if (data.document_types && data.document_types.length > 0) {
                data.document_types.forEach(function(type) {
                    $target.append(`<option value="${type.id}">${type.name}</option>`);
                });
                $target.prop('disabled', false);
            } else {
                $target.html('<option value="">No hay tipos disponibles</option>');
            }
        })
        .fail(function() {
            DocTrac.showNotification('Error al cargar tipos de documento', 'error');
            $target.html('<option value="">Error al cargar</option>');
        });
};