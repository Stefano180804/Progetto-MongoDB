import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Modulo {
    id: string;
    nome: string;
    codice: string;
    ore: number;
    descrizione: string;
}

interface Studente {
    id: string;
    nome: string;
    cognome: string;
    email: string;
}

interface Esame {
    id: string;
    studente: string;
    modulo: string;
    voto: number;
    data: string;
}

@Component({
    selector: 'app-dashboard',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
    currentView: 'dashboard' | 'moduli' | 'studenti' = 'dashboard';
    showModuloForm: boolean = false;
    showStudenteForm: boolean = false;

    // New module form data
    nuovoModulo: Modulo = {
        id: '',
        nome: '',
        codice: '',
        ore: 0,
        descrizione: ''
    };

    // New student form data
    nuovoStudente: Studente = {
        id: '',
        nome: '',
        cognome: '',
        email: ''
    };

    // Mock Data
    moduli: Modulo[] = [
        { id: '1', nome: 'Sviluppo Web Avanzato', codice: 'WEB01', ore: 80, descrizione: 'Corso completo su Angular e React' },
        { id: '2', nome: 'Database NoSQL', codice: 'DB02', ore: 60, descrizione: 'Approfondimento su MongoDB e Redis' },
        { id: '3', nome: 'Cloud Computing', codice: 'CLD03', ore: 40, descrizione: 'AWS e Azure fundamentals' }
    ];

    studenti: Studente[] = [
        { id: '1', nome: 'Mario', cognome: 'Rossi', email: 'mario.rossi@example.com' },
        { id: '2', nome: 'Luca', cognome: 'Bianchi', email: 'luca.bianchi@example.com' },
        { id: '3', nome: 'Giulia', cognome: 'Verdi', email: 'giulia.verdi@example.com' },
        { id: '4', nome: 'Elena', cognome: 'Neri', email: 'elena.neri@example.com' }
    ];

    esami: Esame[] = [
        { id: '1', studente: 'Mario Rossi', modulo: 'Sviluppo Web Avanzato', voto: 28, data: '2023-10-15' },
        { id: '2', studente: 'Luca Bianchi', modulo: 'Database NoSQL', voto: 24, data: '2023-10-20' },
        { id: '3', studente: 'Giulia Verdi', modulo: 'Sviluppo Web Avanzato', voto: 30, data: '2023-10-22' }
    ];

    setView(view: 'dashboard' | 'moduli' | 'studenti') {
        this.currentView = view;
    }

    get mediaVoti(): number {
        const total = this.esami.reduce((acc, curr) => acc + curr.voto, 0);
        return this.esami.length ? Math.round((total / this.esami.length) * 10) / 10 : 0;
    }

    // Open the new module form
    openModuloForm() {
        this.showModuloForm = true;
        this.resetModuloForm();
    }

    // Close the form
    closeModuloForm() {
        this.showModuloForm = false;
        this.resetModuloForm();
    }

    // Reset form data
    resetModuloForm() {
        this.nuovoModulo = {
            id: '',
            nome: '',
            codice: '',
            ore: 0,
            descrizione: ''
        };
    }

    // Save new module
    salvaModulo() {
        if (this.nuovoModulo.nome && this.nuovoModulo.codice && this.nuovoModulo.ore > 0) {
            // Generate a new ID
            const newId = (this.moduli.length + 1).toString();
            const moduloToAdd = { ...this.nuovoModulo, id: newId };

            // Add to the list
            this.moduli.push(moduloToAdd);

            // Close the form
            this.closeModuloForm();
        }
    }

    // Open the new student form
    openStudenteForm() {
        this.showStudenteForm = true;
        this.resetStudenteForm();
    }

    // Close the student form
    closeStudenteForm() {
        this.showStudenteForm = false;
        this.resetStudenteForm();
    }

    // Reset student form data
    resetStudenteForm() {
        this.nuovoStudente = {
            id: '',
            nome: '',
            cognome: '',
            email: ''
        };
    }

    // Save new student
    salvaStudente() {
        if (this.nuovoStudente.nome && this.nuovoStudente.cognome && this.nuovoStudente.email) {
            if (this.nuovoStudente.id) {
                // Update existing student
                const index = this.studenti.findIndex(s => s.id === this.nuovoStudente.id);
                if (index !== -1) {
                    this.studenti[index] = { ...this.nuovoStudente };
                }
            } else {
                // Generate a new ID
                const newId = (this.studenti.length + 1).toString();
                const studenteToAdd = { ...this.nuovoStudente, id: newId };

                // Add to the list
                this.studenti.push(studenteToAdd);
            }

            // Close the form
            this.closeStudenteForm();
        }
    }

    // Edit student
    modificaStudente(studente: Studente) {
        this.nuovoStudente = { ...studente };
        this.showStudenteForm = true;
    }

    // Delete student
    eliminaStudente(id: string) {
        if (confirm('Sei sicuro di voler eliminare questo studente?')) {
            this.studenti = this.studenti.filter(s => s.id !== id);
        }
    }
}
