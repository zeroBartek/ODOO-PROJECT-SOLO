{
    'name': "Open Academy",

    'summary': "Does something",

    'description': """
Description for the open academy module
    """,

    'author': "Hubert Twarowski",
    'website': "https://www.youtube.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    
    "data": [
        "security/ir.model.access.csv",
        "views/contact.xml",
        "views/course.xml",
        "views/session.xml",
        "views/openacademy_views.xml",
    ],


    
    
}

