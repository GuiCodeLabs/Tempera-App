document.addEventListener('DOMContentLoaded', function() {
    // Gerenciamento do Logout via formulário
    const logoutBtn = document.getElementById('logout-button');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            if (!confirm('Deseja realmente sair da sua conta?')) {
                e.preventDefault();
            }
        });
    }

    // Confirmação para deletar conta
    const deleteForms = document.querySelectorAll('form[action*="deletar"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('ATENÇÃO: Esta ação é permanente e excluirá todos os seus dados. Continuar?')) {
                e.preventDefault();
            }
        });
    });
});