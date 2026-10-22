[app]

# (str) Title of your application
title = Control PLC Schneider

# (str) Package name
package.name = controlplc

# (str) Package domain (needed for android packaging)
package.domain = org.industrial

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let it include python files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy,fastapi,uvicorn,pydantic,starlette,pyModbusTCP,idna,anyio,click,h11,certifi

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# (list) Android SDK build-tools version (Opcional pero asegura que descargue build-tools y aidl)
android.sdk_build_tools_version = 34.0.0

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 34

# (list) Android SDK build-tools version
android.sdk_build_tools_version = 34.0.0