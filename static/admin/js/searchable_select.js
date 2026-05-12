// Rendre les select recherchables
document.addEventListener('DOMContentLoaded', function() {
    var selects = document.querySelectorAll('.searchable-select');
    
    selects.forEach(function(select) {
        // Créer une barre de recherche
        var searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Rechercher une faculte...';
        searchInput.style.cssText = 'width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px;';
        searchInput.onkeyup = function() {
            var filter = this.value.toLowerCase();
            for (var i = 0; i < select.options.length; i++) {
                var text = select.options[i].text.toLowerCase();
                select.options[i].style.display = text.includes(filter) ? '' : 'none';
            }
        };
        
        // Insérer la recherche avant le select
        select.parentNode.insertBefore(searchInput, select);
    });
});