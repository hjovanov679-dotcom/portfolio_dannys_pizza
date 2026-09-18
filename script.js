function showPage(pageid) {
    var pages = document.querySelectorAll('.page');
    pages.forEach(page => {
        page.classList.remove('active');
    });

    document.getElementById(pageid).classList.add('active');
}

const hero = document.querySelector('.fire-section');
const fireVideo = document.getElementById('fire-video');

document.addEventListener('DOMContentLoaded', () => {
    const element = document.querySelector('.about-content2 p');
    const text = element.textContent;
    element.textContent = '';
    // Reserve the complete text layout before revealing individual letters.
    const characters = Array.from(text, character => {
        const span = document.createElement('span');
        span.textContent = character;
        span.style.opacity = '0';
        element.appendChild(span);
        return span;
    });
    let index = 0;
    
    function type() {
        if (index < characters.length) {
            characters[index].style.opacity = '1';
            index++;
            setTimeout(type, 10);
        }
    }
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                type();
                observer.unobserve(entry.target);
            }
        });
    });
    const goal = document.querySelector('.about-content2 p');
    observer.observe(goal);
});

async function reserveTable() {

    const namee = document.getElementById('name')
    const email = document.getElementById('email')
    const guests = document.getElementById('guests')
    const date = document.getElementById('date')
    const notes = document.getElementById('special-notes')

    const inputName = namee.value
    const inputEmail = email.value
    const inputGuests = guests.value
    const inputDate = date.value
    const inputNotes = notes.value

    const frontendData = {
        name: inputName,
        email: inputEmail,
        guests: inputGuests,
        date: inputDate,
        notes: inputNotes
    }
    
    try {
        const response = await fetch('/api/send-confirmation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(frontendData)
        })

        if (!response.ok) {
            throw new Error(`Server fout: ${response.status}`);
        }
        const result = await response.json()
        console.log('Succesvol ontvangen!')
    }
    catch (error) {
        console.error('Er ging iets mis:', error);
    }
}



