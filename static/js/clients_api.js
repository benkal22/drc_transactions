// DRC_TRANSACTIONS/static/js/clients_api.js
document.addEventListener('alpine:init', () => {
    Alpine.data('formHandle', () => ({
        clients: [],
        countries: [],
        provinces: [],
        products: [],
        unique_sectors: [],
        client: {
            id_client: null,
            sector_label: [],
            product: [],
            country: null,
            selectedCountry: null,
            province: null,
            category: 'enterprise',
            company_name: '',
            manager_name: '',
            tax_code: '',
            nrc: '',
            nat_id: '',
            name: '',
            photo: null,
            address: '',
            email: '',
            phone_number: '',
            selectedProducts: [],
        },
        errors: [],
        showAdditionalInfo: false,
        status: false,
        isError: false,
        modalHeaderText: '',
        modalBodyText: '',

        async fetchClients() {
            try {
                const response = await fetch('/api/clients/');
                if (!response.ok) {
                    throw new Error('Erreur réseau lors de la récupération des clients.');
                }
                this.clients = await response.json();
            } catch (error) {
                console.error('Erreur fetching clients:', error);
            }
        },
        async fetchCountries() {
            try {
                const response = await fetch('/api/countries/');
                if (!response.ok) {
                    throw new Error('Erreur réseau lors de la récupération des pays.');
                }
                this.countries = await response.json();
            } catch (error) {
                console.error('Erreur fetching countries:', error);
            }
        },
        async fetchProvinces() {
            try {
                const response = await fetch('/api/provinces/');
                if (!response.ok) {
                    throw new Error('Erreur réseau lors de la récupération des provinces.');
                }
                this.provinces = await response.json();
            } catch (error) {
                console.error('Erreur fetching provinces:', error);
            }
        },
        async fetchProducts() {
            try {
                const response = await fetch('/api/products/');
                if (!response.ok) {
                    throw new Error('Erreur réseau lors de la récupération des produits.');
                }
                this.products = await response.json();
            } catch (error) {
                console.error('Erreur fetching products:', error);
            }
        },
        async fetchUniqueSectors() {
            try {
                const response = await fetch('/api/unique-sectors/');
                if (!response.ok) {
                    throw new Error('Erreur réseau lors de la récupération des secteurs uniques.');
                }
                this.unique_sectors = await response.json();
            } catch (error) {
                console.error('Erreur fetching unique sectors:', error);
            }
        },
        async addClient() {
            let formData = new FormData();
            formData.append('category', this.client.category);
            formData.append('company_name', this.client.company_name);
            formData.append('manager_name', this.client.manager_name);
            formData.append('tax_code', this.client.tax_code);
            formData.append('nrc', this.client.nrc);
            formData.append('nat_id', this.client.nat_id);
            formData.append('name', this.client.name);
            formData.append('photo', this.client.photo);
            formData.append('address', this.client.address);
            formData.append('email', this.client.email);
            formData.append('phone_number', this.client.phone_number);
            formData.append('sector_label', JSON.stringify(this.client.sector_label.map(item => item.id)));
            formData.append('country', this.client.selectedCountry.id);
            formData.append('province', this.client.province.id);
            formData.append('products', JSON.stringify(this.client.selectedProducts.map(item => item.id)));

            try {
                const response = await fetch('/api/clients/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                });
                if (!response.ok) {
                    throw new Error('Erreur réseau lors de la création du client.');
                }
                const newClient = await response.json();
                this.clients.push(newClient);
                this.resetClient();
                this.showModal('Succès', 'Client ajouté avec succès.', false);
            } catch (error) {
                console.error('Erreur lors de l\'ajout du client:', error);
                this.showModal('Erreur', 'Erreur lors de l\'ajout du client.', true);
            }
        },
        async deleteClient(id) {
            try {
                const response = await fetch(`/api/clients/${id}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                });
                if (!response.ok) {
                    throw new Error('Erreur réseau lors de la suppression du client.');
                }
                this.clients = this.clients.filter(client => client.id_client !== id);
                this.showModal('Succès', 'Client supprimé avec succès.', false);
            } catch (error) {
                console.error('Erreur lors de la suppression du client:', error);
                this.showModal('Erreur', 'Erreur lors de la suppression du client.', true);
            }
        },
        async updateClient() {
            let formData = new FormData();
            formData.append('id_client', this.client.id_client);
            formData.append('category', this.client.category);
            formData.append('company_name', this.client.company_name);
            formData.append('manager_name', this.client.manager_name);
            formData.append('tax_code', this.client.tax_code);
            formData.append('nrc', this.client.nrc);
            formData.append('nat_id', this.client.nat_id);
            formData.append('name', this.client.name);
            formData.append('photo', this.client.photo);
            formData.append('address', this.client.address);
            formData.append('email', this.client.email);
            formData.append('phone_number', this.client.phone_number);
            formData.append('sector_label', JSON.stringify(this.client.sector_label.map(item => item.id)));
            formData.append('country', this.client.selectedCountry.id);
            formData.append('province', this.client.province.id);
            formData.append('products', JSON.stringify(this.client.products.map(item => item.id)));

            try {
                const response = await fetch(`/api/clients/${this.client.id_client}/`, {
                    method: 'PUT',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                });
                if (!response.ok) {
                    throw new Error('Erreur réseau lors de la mise à jour du client.');
                }
                const updatedClient = await response.json();
                this.clients = this.clients.map(client => {
                    if (client.id_client === updatedClient.id_client) {
                        return updatedClient;
                    }
                    return client;
                });
                this.resetClient();
                this.showModal('Succès', 'Client mis à jour avec succès.', false);
            } catch (error) {
                console.error('Erreur lors de la mise à jour du client:', error);
                this.showModal('Erreur', 'Erreur lors de la mise à jour du client.', true);
            }
        },
        resetClient() {
            this.client = {
                id_client: null,
                sector_label: [],
                product: [],
                country: null,
                selectedCountry: null,
                province: null,
                category: 'enterprise',
                company_name: '',
                manager_name: '',
                tax_code: '',
                nrc: '',
                nat_id: '',
                name: '',
                photo: null,
                address: '',
                email: '',
                phone_number: '',
                selectedProducts: [],
            };
        },
        get filteredProducts() {
            if (!this.client.sector_label) return this.products;
            return this.products.filter(product => product.sector_label === this.client.sector_label);
        },
        init() {
            this.fetchClients();
            this.fetchCountries();
            this.fetchProvinces();
            this.fetchProducts();
            this.fetchUniqueSectors();
        },
        validateAndSubmitForm() {
            this.errors = [];

            if (this.client.category === 'enterprise' && !this.client.company_name) {
                this.errors.push('company_name');
            }
            if (this.client.category === 'individual' && !this.client.name) {
                this.errors.push('name');
            }
            if (!this.client.address) {
                this.errors.push('address');
            }
            if (!this.client.email) {
                this.errors.push('email');
            }
            if (!this.client.phone_number) {
                this.errors.push('phone_number');
            }
            if (!this.client.selectedCountry) {
                this.errors.push('country');
            }
            if (this.client.selectedCountry && this.client.selectedCountry.id === 112 && !this.client.province) {
                this.errors.push('province');
            }

            if (this.errors.length === 0) {
                if (this.client.id_client) {
                    this.updateClient();
                } else {
                    this.addClient();
                }
            } else {
                this.showModal('Erreur de validation', 'Veuillez remplir tous les champs obligatoires.', true);
            }
        },
        showModal(headerText, bodyText, isError) {
            this.modalHeaderText = headerText;
            this.modalBodyText = bodyText;
            this.isError = isError;
            this.status = true;
        },
        hideModal() {
            this.status = false;
            this.modalHeaderText = '';
            this.modalBodyText = '';
            this.isError = false;
        },
    }));
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
