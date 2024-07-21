// index.js
import { Alpine } from 'alpinejs';

document.addEventListener('DOMContentLoaded', function() {
    Alpine.data('clientList', () => ({
        clients: [],

        async fetchClients() {
            try {
                let response = await fetch('http://127.0.0.1:8000/api/clients/');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                this.clients = await response.json();
            } catch (error) {
                console.error('Error fetching clients:', error);
            }
        },

        getClientName(client) {
            if (client.category === 'enterprise') {
                return client.company_name || 'No company name';
            } else {
                return client.name || 'No name';
            }
        },

        init() {
            this.fetchClients();
        }
    }));
});
