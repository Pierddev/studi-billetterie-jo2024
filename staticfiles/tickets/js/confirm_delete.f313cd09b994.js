document.addEventListener('DOMContentLoaded', (event) => {
    const deleteLinks = document.querySelectorAll('.delete-ticket');

    deleteLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            if (!confirm('Voulez-vous vraiment supprimer ce ticket ?')) {
                event.preventDefault();
            }
        });
    });
});
