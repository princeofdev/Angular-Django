#!/bin/bash

rm Wuappa.apk
cd .. && \
mkdir -p platforms/android/app && \
cp src/google-services.json platforms/android/app/google-services.json && \
ionic cordova build android --prod --release && \
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore android-build/sign-key.jks platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk wuappa && \
zipalign -v 4 platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk android-build/Wuappa.apk && \
apksigner verify android-build/Wuappa.apk
