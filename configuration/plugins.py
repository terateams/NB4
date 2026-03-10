# Add your plugins and plugin settings here.
# Of course uncomment this file out.

# To learn how to build images with your required plugins
# See https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

from os import environ

from netbox_branching.utilities import DynamicSchemaDict

PLUGINS = [
    "netbox_contract",
    "netbox_branching",
]

# PLUGINS_CONFIG = {
#   "netbox_bgp": {
#     ADD YOUR SETTINGS HERE
#   }
# }

DATABASES = DynamicSchemaDict({
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get("DB_NAME", "netbox"),         # Database name
        'USER': environ.get("DB_USER", ""),               # PostgreSQL username
        'PASSWORD': environ.get("DB_PASSWORD", ""),       # PostgreSQL password
        'HOST': environ.get("DB_HOST", "postgres"),       # Database server
        'PORT': '',                                       # Database port (leave blank for default)
        'CONN_MAX_AGE': 300,                              # Max database connection age
    }
})

DATABASE_ROUTERS = [
    "netbox_branching.database.BranchAwareRouter",
]