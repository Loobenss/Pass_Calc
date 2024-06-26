[app]
title = Pass_Calc
package.name = Cal
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3==3.11.6,kivy==2.3.0,Kivy-Garden,requests,toml,urllib3,pillow
icon.filename = icocal.png
orientation = portrait
fullscreen = 0
osx.python_version = 3.11.6
osx.kivy_version = 2.3.0

android.build_options = --with-build-python

android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

p4a.branch = release-2022.12.20

[buildozer]
log_level = 2
warn_on_root = 1
