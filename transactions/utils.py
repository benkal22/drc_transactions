from django.contrib.auth.decorators import login_required
from django.db.models import F, ExpressionWrapper, DecimalField, Sum, Q

from transactions.models import Producer, Client, Supplier
from transactions.filters import ProducerFilter

@login_required
def producer_statistics(request):
    if request.user.is_superuser:
        queryset = Producer.objects.all()
    else:
        queryset = Producer.objects.filter(user=request.user)
        
    producer_filter = ProducerFilter(request.GET, queryset=queryset)
    filtered_producers = producer_filter.qs

    # Récupérer tous les clients associés à ces producteurs
    filtered_clients = Client.objects.filter(producer__in=filtered_producers).distinct()
    # Calculer le total des ventes pour ces clients
    total_sales = filtered_clients.aggregate(total_sales=Sum('total_sales'))['total_sales'] or 0
    
    # Récupérer les fournisseurs associés à ces producteurs
    suppliers = Supplier.objects.filter(producer__in=filtered_producers).distinct()

    # Calculer le total des achats pour chaque fournisseur
    total_purchases = suppliers.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('transaction__price') * F('transaction__quantity'),
                output_field=DecimalField()
            ),
            filter=Q(transaction__type='purchase')
        )
    )['total'] or 0

    # Nombre total de tous les producteurs
    total_producers = filtered_producers.count()

    # Nombre total des producteurs approuvés
    total_approved_producers = filtered_producers.filter(is_approved=True).count()

    # Nombre total des producteurs non approuvés
    total_unapproved_producers = filtered_producers.filter(is_approved=False).count()

    # Retourner les résultats sous forme de dictionnaire
    return {
        'total_sales': f"💰{total_sales:.2f} CDF",
        'total_purchases': f"💰{total_purchases:.2f} CDF",
        'total_producers': total_producers,
        'total_approved_producers': total_approved_producers,
        'total_unapproved_producers': total_unapproved_producers
    }
