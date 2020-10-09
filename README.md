## caserver
支持OAUTH2和CAS的统一认证服务

### requirement
Django==2.2.16</br>
django-cas-ng==4.1.1</br>
django-cors-middleware==1.5.0</br>
django-mama-cas==2.4.0</br>
django-oauth-toolkit==1.3.2</br>
djangorestframework==3.12.1</br>
django-crowd-auth==0.8.0</br>


### 说明
因工作需要，为打通公司内部多平台的单点登录认证，实现一套账户登录多个系统，特搞了一个简单的支持oauth2和cas认证，并且以crowd为用户目录的服务。</br>
此工具简单易用，几乎只需要简单的配置即可使用。</br>
适用于使用jira、confluence、crowd全家桶的公司，并且希望crowd可以当做其他平台诸如grafana、jumpserver、jenkins等的身份认证中心。

### 配置
python3安装Django步骤就省略了，相关的依赖按照requirement来就可以。</br>
下面重点讲讲配置</br>
#### settings.py
```python
# 这里添加需导入的应用
INSTALLED_APPS = [
    ...
    'mama_cas',
    'oauth2_provider',
    'corsheaders',
    'rest_framework',
    ...
]

# 中间件
# 加入crowd认证模块，还有多语言支持
MIDDLEWARE = [
	...
	'django_crowd_auth.middlewares.sso',
	'django.middleware.locale.LocaleMiddleware',
	...
]

# 允许跨域
CORS_ORIGIN_ALLOW_ALL = True

# 认证后端
# 这个配置参数是存在的，只是默认不在配置文件中，需要新添加一个crowd模块
AUTHENTICATION_BACKENDS = [ 
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
    'django_crowd_auth.backends.Backend',
]

# 下面是cas相关配置
MAMA_CAS_SERVICES = [ 
    {   
        # 必填项，此项为**Client** IP:Port，相当于白名单
        'SERVICE': 'https://xxx.xxx.com',
        # 回调模式，具体参考官方文档
        'CALLBACKS': [
            'mama_cas.callbacks.user_model_attributes',
        ],  
    },  

]

# Crowd服务器地址及配置
CROWD_CLIENT = {
    'crowd_url': 'https://xxx.xxx.com/crowd/',
    'app_name': 'jumperserver',
    'app_pass': 'KhlwuFtYmM',
    #'ssl_verify': '/etc/pki/tls/certs/ca-bundle.crt',
    'ssl_verify': '/etc/ssl/cert.pem',
    'timeout': 10,
}

CROWD_USERS_ARE_STAFF = True
CROWD_SUPERUSERS_GROUP = 'confluence-administrators'

ROOT_URLCONF = 'caserver.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 多语言
LANGUAGES = (
    ('en', ('English')),
    ('zh-hans', ('中文简体')),
    ('zh-hant', ('中文繁體')),
)
# 翻译文件所在目录，需要手工创建
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.i18n",
)

STATIC_URL = '/static/'
STATIC_ROOT = '/home/ops/caserver/static/'

# Oauth2模块配置
OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}