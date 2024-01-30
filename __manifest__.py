{
    'name': 'CRM-FOR-LABORATORY',
    'version': '1.0',
    'category': 'CRM',
    'summary': 'Track leads and close opportunities',
    'depends': [
        'base_setup',
        'sales_team',
        'mail',
        'calendar',
        'resource',
        'utm',
        'web_tour',
        'web_kanban_gauge',
        'contacts',
        'digest',
        'phone_validation',
        'base',
        'web',
        'crm',
    ],
    'data': [
        'security/security.xml',
        'views/crm_leads_view.xml',
        'views/teeth_color_view.xml',
        'views/filter_views.xml',
        'views/crm_kanban_view.xml',
        'views/crm_tree_view.xml',
        'views/worker_views.xml',
        'views/porselenci_view.xml',
        'views/crm_product_status.xml',
        'views/ir_ui_view.xml',
        'views/ir_actions_report.xml',
        # 'views/res_partener_view.xml'

    ],
    'installable': True,
    'application': True,
}