// Script pour gérer l'interaction entre les champs personnel et enseignant
document.addEventListener('DOMContentLoaded', function() {
    // Gestion pour le formulaire de congés
    const personnelConge = document.getElementById('id_personnel');
    const enseignantConge = document.getElementById('id_enseignant');

    if (personnelConge && enseignantConge) {
        function updateCongeFields() {
            if (personnelConge.value) {
                enseignantConge.disabled = true;
                enseignantConge.value = '';
            } else if (enseignantConge.value) {
                personnelConge.disabled = true;
                personnelConge.value = '';
            } else {
                personnelConge.disabled = false;
                enseignantConge.disabled = false;
            }
        }

        personnelConge.addEventListener('change', updateCongeFields);
        enseignantConge.addEventListener('change', updateCongeFields);

        // Initialiser l'état
        updateCongeFields();
    }

    // Gestion pour le formulaire de participation
    const enseignantParticipation = document.getElementById('id_enseignant_participation');
    const personnelParticipation = document.getElementById('id_personnel_participation');

    if (enseignantParticipation && personnelParticipation) {
        function updateParticipationFields() {
            if (enseignantParticipation.value) {
                personnelParticipation.disabled = true;
                personnelParticipation.value = '';
            } else if (personnelParticipation.value) {
                enseignantParticipation.disabled = true;
                enseignantParticipation.value = '';
            } else {
                enseignantParticipation.disabled = false;
                personnelParticipation.disabled = false;
            }
        }

        enseignantParticipation.addEventListener('change', updateParticipationFields);
        personnelParticipation.addEventListener('change', updateParticipationFields);

        // Initialiser l'état
        updateParticipationFields();
    }
});
