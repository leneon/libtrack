// Barre de recherche pour la faculté
document.addEventListener('DOMContentLoaded', function() {
    var faculteSelect = document.getElementById('faculte_select');
    if (!faculteSelect) return;
    
    // Créer la barre de recherche
    var searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = '🔍 Rechercher une faculté...';
    searchInput.style.cssText = 'width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px;';
    
    // Fonction de filtrage
    searchInput.onkeyup = function() {
        var filter = this.value.toLowerCase();
        for (var i = 0; i < faculteSelect.options.length; i++) {
            var text = faculteSelect.options[i].text.toLowerCase();
            faculteSelect.options[i].style.display = text.includes(filter) ? '' : 'none';
        }
    };
    
    // Insérer avant le select
    faculteSelect.parentNode.insertBefore(searchInput, faculteSelect);
});