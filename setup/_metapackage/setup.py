import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-akretion-ak-cloud-france-oi",
    description="Meta package for akretion-ak-cloud-france-oi Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-attachment_asset_in_db>=16.0dev,<16.1dev',
        'odoo-addon-auth_oidc_akretion_data>=16.0dev,<16.1dev',
        'odoo-addon-database_age_cron>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
