from admin_tools.dashboard import modules, Dashboard

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for DRC_TRANSACTIONS.
    """
    def init_with_context(self, context):
        self.children.append(modules.ModelList(
            title='Applications',
            models=('transactions.models.*',)
        ))

        self.children.append(modules.RecentActions(
            title='Recent Actions',
            limit=10
        ))

# Utiliser le tableau de bord personnalisé dans le settings.py
ADMIN_TOOLS_INDEX_DASHBOARD = 'DRC_TRANSACTIONS.admin_tools.dashboard.CustomIndexDashboard'
