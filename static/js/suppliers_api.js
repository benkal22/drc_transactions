document.addEventListener('Alpine:init', async () => {
    Alpine.store('supplierStore',
        {
            suppliers:[],
            supplier: {
                id_supplier: () => Math.random().toString(36).substr(2,9),
                sector_label: '',
                product: '',
                country: '',
                province: '',
                category: '',
                company_name: '',
                manager_name: '',
                tax_code: '',
                nrc: '',
                nat_id: '',
                name: '',
                photo: '',
                address: '',
                email: '',
                phone_number: ''
            }
        }

    )

}
)