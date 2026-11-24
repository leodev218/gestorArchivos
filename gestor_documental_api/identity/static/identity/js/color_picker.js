
document.addEventListener("DOMContentLoaded", function () {

    const containers = document.querySelectorAll(
        ".color-picker-container"
    );

    containers.forEach(function (container) {

        const colorPicker = container.querySelector(
            ".color-picker-input"
        );

        const hexInput = container.querySelector(
            ".color-hex-input"
        );

        if (!colorPicker || !hexInput) return;

        // Cuando se selecciona un color en la paleta.
        colorPicker.addEventListener("input", function () {
            hexInput.value = colorPicker.value.toUpperCase();
        });

        // Cuando se escribe un código hexadecimal.
        hexInput.addEventListener("input", function () {

            const value = hexInput.value.trim();

            const validHex = /^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/;

            if (validHex.test(value)) {
                colorPicker.value = value;
            }

        });

        // Sincronizar el valor inicial.
        const initialValue = hexInput.value.trim();

        if (/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/.test(initialValue)) {
            colorPicker.value = initialValue;
        }

    });

});
