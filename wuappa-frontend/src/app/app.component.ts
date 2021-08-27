import { ViewChild, Component } from '@angular/core';
import { Platform, Nav } from 'ionic-angular';
import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';
import { Globalization } from '@ionic-native/globalization';

import { MenuPage } from '../pages/menu/menu';
import { TranslateService } from '@ngx-translate/core';
import { Keyboard } from '@ionic-native/keyboard';
import { Storage } from '@ionic/storage';
import * as moment from 'moment';
import 'moment/locale/es';
import { LANGUAGES } from './constants';


@Component({
  templateUrl: 'app.html'
})
export class MyApp {

  rootPage: any = MenuPage;

  @ViewChild(Nav) navChild:Nav;
  private languageCode: any = '';

  constructor(
    public platform: Platform,
    public statusBar: StatusBar,
    public splashScreen: SplashScreen,
    private translate: TranslateService,
    private keyboard: Keyboard,
    private globalization: Globalization,
    private storage: Storage
  ) {

    this.initializeApp();
    // this language will be used as a fallback when a translation isn't found in the current language
    this.translate.setDefaultLang('en');
  }

  setLanguage(languageCode) {
    if (LANGUAGES.indexOf(languageCode) >= 0) {
      this.translate.use(languageCode);
      moment.locale(languageCode);
    }
  }

  initializeApp() {
    this.platform.ready().then(success => {
      // Okay, so the platform is ready and our plugins are available.
      // Here you can do any higher level native things you might need.
      this.statusBar.overlaysWebView(false);
      this.statusBar.styleDefault();
      this.splashScreen.hide();
      this.keyboard.hideKeyboardAccessoryBar(false);

      this.storage.ready().then(() =>{
        this.storage.get('language').then(results =>{
          this.languageCode = results;
          this.setLanguage(this.languageCode);
          if(typeof this.languageCode !== 'undefined' && this.languageCode){
            this.setLanguage(this.languageCode);
          }else{
            this.globalization.getPreferredLanguage().then(res => {
              const language = res.value || null;
              if (language && language.indexOf("-") >= 0) {
                this.languageCode = language.split("-")[0];
                this.setLanguage(this.languageCode);
              }
            });
          }
        });
      });
    });
  }

}
