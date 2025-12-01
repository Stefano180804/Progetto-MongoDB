import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
export class LoginComponent {
    email = '';
    password = '';
    error = '';

    constructor(private router: Router) { }

    login() {
        if (this.email === 'admin@its.it' && this.password === 'admin') {
            this.router.navigate(['/dashboard']);
        } else {
            this.error = 'Credenziali non valide';
        }
    }
}
