# Development environment

The app has been built using Ionic Framework.

1) Install Ionic

`npm install -g ionic``

2) Install all dependencies

`npm i`

3) Start development server

`ionic serve`

# Build native app

Is highly recommended to follow this guide: [https://ionicframework.com/docs/intro/deploying/](https://ionicframework.com/docs/intro/deploying/)

## Build iOS app

Just execute: `ionic cordova build ios --prod`

## Build Android app

Just execute the script `build-and-sign.sh` from the `android-build` folder.