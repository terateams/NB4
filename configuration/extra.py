####
## This file contains extra configuration options that can't be configured
## directly through environment variables.
####

## Specify one or more name and email address tuples representing NetBox administrators. These people will be notified of
## application errors (assuming correct email settings are provided).
# ADMINS = [
#     # ['John Doe', 'jdoe@example.com'],
# ]


## URL schemes that are allowed within links in NetBox
# ALLOWED_URL_SCHEMES = (
#     'file', 'ftp', 'ftps', 'http', 'https', 'irc', 'mailto', 'sftp', 'ssh', 'tel', 'telnet', 'tftp', 'vnc', 'xmpp',
# )

## Enable installed plugins. Add the name of each plugin to the list.
# from netbox.configuration.configuration import PLUGINS
# PLUGINS.append('my_plugin')

## Plugins configuration settings. These settings are used by various plugins that the user may have installed.
## Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.
# from netbox.configuration.configuration import PLUGINS_CONFIG
# PLUGINS_CONFIG['my_plugin'] = {
#   'foo': 'bar',
#   'buzz': 'bazz'
# }


## Remote authentication support
# REMOTE_AUTH_DEFAULT_PERMISSIONS = {}

## Azure AD / Microsoft Entra ID Social Auth Configuration
## Read Social Auth settings from environment variables
from os import environ

# Azure AD OAuth2 settings for single-tenant authentication
if environ.get('SOCIAL_AUTH_AZUREAD_OAUTH2_KEY'):
    SOCIAL_AUTH_AZUREAD_OAUTH2_KEY = environ.get('SOCIAL_AUTH_AZUREAD_OAUTH2_KEY')

if environ.get('SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET'):
    SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET = environ.get('SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET')

# Optional: Force HTTPS redirect URI if behind a load balancer or reverse proxy
# Uncomment the line below if Azure AD complains about http:// redirect URIs
# SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# 自定义 Social Auth Pipeline，支持通过 email 关联已存在的用户
# 这样可以避免创建重复用户，而是关联到已有的相同 email 用户
SOCIAL_AUTH_PIPELINE = (
    # 获取 provider 的用户信息
    'social_core.pipeline.social_auth.social_details',
    # 获取 social auth 的 UID
    'social_core.pipeline.social_auth.social_uid',
    # 检查当前后端是否允许
    'social_core.pipeline.social_auth.auth_allowed',
    # 尝试通过 social auth 关联查找用户
    'social_core.pipeline.social_auth.social_user',
    # 尝试通过 email 查找并关联已存在的用户（关键步骤）
    'social_core.pipeline.social_auth.associate_by_email',
    # 获取用户名
    'social_core.pipeline.user.get_username',
    # 如果用户不存在则创建（只有在上面的步骤都没找到用户时才会执行）
    'social_core.pipeline.user.create_user',
    # 关联 social auth 到用户
    'social_core.pipeline.social_auth.associate_user',
    # 加载 provider 的额外数据
    'social_core.pipeline.social_auth.load_extra_data',
    # 更新用户详细信息（如名字、姓氏等）
    'social_core.pipeline.user.user_details',
)


## By default uploaded media is stored on the local filesystem. Using Django-storages is also supported. Provide the
## class path of the storage driver in STORAGE_BACKEND and any configuration options in STORAGE_CONFIG. For example:
# STORAGE_BACKEND = 'storages.backends.s3boto3.S3Boto3Storage'
# STORAGE_CONFIG = {
#     'AWS_ACCESS_KEY_ID': 'Key ID',
#     'AWS_SECRET_ACCESS_KEY': 'Secret',
#     'AWS_STORAGE_BUCKET_NAME': 'netbox',
#     'AWS_S3_REGION_NAME': 'eu-west-1',
# }


## This file can contain arbitrary Python code, e.g.:
# from datetime import datetime
# now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
# BANNER_TOP = f'<marquee width="200px">This instance started on {now}.</marquee>'
