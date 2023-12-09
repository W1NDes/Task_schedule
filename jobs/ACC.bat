cd C:\AzurLaneAutoScript\toolkit\Lib\site-packages\adbutils\binaries
adb connect 127.0.0.1:16416
adb -s 127.0.0.1:16416 shell input tap 427 536
ping 127.0.0.1 -n 5
adb -s 127.0.0.1:16416 shell input tap 676 106