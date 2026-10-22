[app]
title = Control PLC Schneider
package.name = controlplc
package.domain = org.industrial
source.include_exts = py,png,jpg,kv,atlas
requirements = python3,kivy,fastapi,uvicorn,pydantic,starlette,pyModbusTCP,idna,anyio,click,h11,certifi
orientation = portrait
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

[buildozer]
log_level = 2
warn_on_root = 0