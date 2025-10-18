document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.btn-delete');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const docTypeId = this.getAttribute('data-doc-id');
            const docTypeName = this.getAttribute('data-doc-name');

            deleteDocumentType(docTypeId, docTypeName);
        });
    });
});