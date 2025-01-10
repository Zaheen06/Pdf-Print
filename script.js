const form = document.getElementById('uploadForm');
        const alertSlider = document.getElementById('alertSlider');
        const alertMessage = document.getElementById('alertMessage');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);

            try {
                const res = await fetch('upload.php', {
                    method: 'POST',
                    body: formData
                });

                const data = await res.json();
                if (data.message) {
                    alertMessage.innerHTML = data.message;
                    showAlert();
                } else {
                    alertMessage.innerHTML = data.error;
                    showAlert();
                }
            } catch (err) {
                alertMessage.innerHTML = 'An unexpected error occurred.';
                showAlert();
            }
        });

        function showAlert() {
            alertSlider.classList.add('show');
            setTimeout(closeAlert, 5000); // Close after 5 seconds
        }

        function closeAlert() {
            alertSlider.classList.remove('show');
        }