<div x-data="clientManager()">
    <!-- Form to create or update client -->
    <form @submit.prevent="saveClient">
        <input type="text" x-model="client.name" placeholder="Name">
        <input type="text" x-model="client.email" placeholder="Email">
        <!-- Add other fields as necessary -->
        <button type="submit">Save</button>
    </form>
    
    <!-- List of clients -->
    <ul>
        <template x-for="client in clients" :key="client.id_client">
            <li>
                <span x-text="client.name"></span>
                <button @click="editClient(client.id_client)">Edit</button>
                <button @click="deleteClient(client.id_client)">Delete</button>
            </li>
        </template>
    </ul>
</div>

<script>
function clientManager() {
    return {
        clients: [],
        client: {
            id_client: null,
            name: '',
            email: '',
            // Add other fields as necessary
        },
        
        init() {
            this.fetchClients();
        },
        
        async fetchClients() {
            try {
                let response = await fetch('http://127.0.0.1:8000/api/clients/');
                this.clients = await response.json();
            } catch (error) {
                console.error('Error fetching clients:', error);
            }
        },
        
        async saveClient() {
            try {
                let method = this.client.id_client ? 'PUT' : 'POST';
                let url = this.client.id_client ? `http://127.0.0.1:8000/api/clients/${this.client.id_client}/` : 'http://127.0.0.1:8000/api/clients/';
                
                let response = await fetch(url, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.client),
                });
                
                if (response.ok) {
                    this.fetchClients();
                    this.client = {
                        id_client: null,
                        name: '',
                        email: '',
                        // Reset other fields as necessary
                    };
                } else {
                    console.error('Error saving client:', response.statusText);
                }
            } catch (error) {
                console.error('Error saving client:', error);
            }
        },
        
        editClient(id_client) {
            let client = this.clients.find(c => c.id_client === id_client);
            this.client = {...client};
        },
        
        async deleteClient(id_client) {
            try {
                let response = await fetch(`http://127.0.0.1:8000/api/clients/${id_client}/`, {
                    method: 'DELETE',
                });
                
                if (response.ok) {
                    this.fetchClients();
                } else {
                    console.error('Error deleting client:', response.statusText);
                }
            } catch (error) {
                console.error('Error deleting client:', error);
            }
        },
    };
}
</script>
