const editButtons = document.querySelectorAll(".edit-button");

        editButtons.forEach(function (button) {
            button.addEventListener("click", function (e) {
                e.preventDefault();
                const target = this.getAttribute("data-target");
                const editForm = document.getElementById(target);

                if (editForm.style.display === "none") {
                    editForm.style.display = "block";
                } else {
                    editForm.style.display = "none";
                }
            });
        });
        function toggleEditForm(bookId) {
            var editForm = document.getElementById('edit-content-' + bookId);
            editForm.style.display = editForm.style.display === 'none' ? 'block' : 'none';
        }