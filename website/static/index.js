// Delete note.
function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId}),
    }).then((_res) => {
        window,location.href = '/user-home';
    });
}

// Event listener to add or remove active styling on selected list-group-item elements.
const li_elements = document.querySelectorAll('.list-group-item');
li_elements.forEach(li_elements => {
    li_elements.addEventListener('click', () => {
        document.querySelector('.active')?.classList.remove('active');
        li_elements.classList.add('active');
    });
});

const form_element = document.getElementById('content');
const form_title = document.getElementById('title1');
const form_note_id = document.getElementById('note_id');
const form_note_date = document.getElementById('note_date');

// Send note information to user home page.
function updateContent(note_content, note_title, note_id, note_date) {
    form_element.innerHTML = note_content;
    form_title.value = note_title;
    form_note_id.value = note_id;
    form_note_date.innerHTML = 'Last saved: ' + note_date;
}

