

document.addEventListener("DOMContentLoaded", function () {

    const typeField = document.getElementById("id_institution_type");

    const cyclesField = document.querySelector(
        ".form-row.field-educational_cycles"
    );

    const programsField = document.getElementById("programs-group");

    function updateAcademicFields() {

        if (!typeField) return;

        const selectedType = typeField.value;

        if (cyclesField) {
            cyclesField.style.display =
                selectedType === "CLEI" ? "" : "none";
        }

        if (programsField) {
            programsField.style.display =
                selectedType === "ETDH" ? "" : "none";
        }
    }

    if (typeField) {
        typeField.addEventListener("change", updateAcademicFields);
        updateAcademicFields();
    }

});
