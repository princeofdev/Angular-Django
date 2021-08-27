import { Component, ViewChild } from '@angular/core';
import { IonicPage, NavController, NavParams,Nav, App, AlertController, Events, Platform, LoadingController, MenuController } from 'ionic-angular';
import { Push } from '@ionic-native/push';

import { LoginPage } from '../login/login';
import { SessionService } from '../../providers/session-service';

import { SettingsPage } from '../settings/settings';
import { MapsPage } from '../maps/maps';
import { AppointmentsPage } from '../appointments/appointments';
import { PaymentMethodPage } from '../payment-method/payment-method';
import { WorkCalendarPage } from '../work-calendar/work-calendar';
import { ServicesPage } from '../services-page/services-page';
import { WorkDaysPage } from '../work-days/work-days';
import { AccountPage } from '../account-page/account-page';
import { TranslateService } from '@ngx-translate/core';
import { WorkZoneDistrictPage } from '../work-zone-district/work-zone-district';
import { UserService } from '../../providers/user-service';
import { AppointmentDetailPage } from '../appointment-detail/appointment-detail';
import { TermsConditionsMenuPage } from '../terms-conditions-menu/terms-conditions-menu';
import { HelpPage } from '../help/help';
import { JWTService } from '../../providers/jwt-service';
import { Subscription } from 'rxjs';
import { SocialSharing } from '@ionic-native/social-sharing';

@IonicPage()
@Component({
  selector: 'page-menu',
  templateUrl: 'menu.html',
})
export class MenuPage {
  @ViewChild(Nav) nav: Nav;

  rootPage:any = null;
  pages = {
    "Home": MapsPage ,
    "Settings": SettingsPage ,
    "My appointments": AppointmentsPage,
    "Payment methods": PaymentMethodPage,
    "Bank account": AccountPage ,
    "Workdays": WorkDaysPage,
    "Holidays": WorkCalendarPage ,
    "WORKZONE": WorkZoneDistrictPage ,
    "Services": ServicesPage,
    "TERMS-CONDITIONS": TermsConditionsMenuPage ,
    "Help & Support": HelpPage
  };

  private onResumeSubscription: Subscription;
  private user: any = null;
  public translations: any = [];
  public loading = false;
  public device:string = '';
  constructor(
    private socialSharing: SocialSharing,
    public navCtrl: NavController,
    public navParams: NavParams,
    private sessionService: SessionService,
    private app: App,
    public translateService: TranslateService,
    public push: Push,
    public userService: UserService,
    public alertCtrl: AlertController,
    public events: Events,
    public platform: Platform,
    private loadingCtrl: LoadingController,
    private jwtService: JWTService,
    private menuCtrl: MenuController,
  ) {
    this.translateService.get(["Home", "Invite your friends to download WUAPPA on", "Settings", "My appointments", "Payment methods", "Bank account", "Workdays", "WORKZONE",
      "Services", "Work calendar", "About us", "Support", "Services", "Holidays", "See detail", "TERMS-CONDITIONS", "Help & Support",
      "See services", "OK", "Try that amazing app, download it at:", "App successfully shared",
      "Friends! I just had a beauty treatment at home! Download the WUAPPA app and book your own beauty professional anytime anywhere. Beautify yourself!"]).subscribe(
      result => {
        this.translations = result;
      }
    );
    this.translateService.onLangChange.subscribe(language => {
      this.translateService.get(["Home", "Invite your friends to download WUAPPA on", "Settings", "My appointments", "Payment methods", "Bank account", "Workdays", "WORKZONE",
        "Services", "Work calendar", "About us", "Support", "Services", "Holidays", "See detail", "TERMS-CONDITIONS", "Help & Support",
        "See services", "OK", "Try that amazing app, download it at:", "App successfully shared",
        "Friends! I just had a beauty treatment at home! Download the WUAPPA app and book your own beauty professional anytime anywhere. Beautify yourself!"]).subscribe(
          result => {
            this.translations = result;
          }
        );
    })

    this.onResumeSubscription = this.platform.resume.subscribe(() => {
      this.checkLogin();
    });


  }

  ionViewDidEnter() {
    this.checkLogin();
  }

  logout() {
    this.sessionService.logout();
    this.menuCtrl.enable(false);
    this.rootPage = LoginPage;
  }

  isFinalUser() {
    return this.user && this.user.type == "FIN";
  }

  isProfessionalUser() {
    return this.user && this.user.type == "PRO";
  }

  setUser(user){
    this.user = user;
    if (user.type == "FIN") {
      this.rootPage = MapsPage;
    } else {
      this.rootPage = AppointmentsPage;
    }
    this.menuCtrl.enable(true);
  }

  openPage(page) {
    this.app.getActiveNavs("menuRoot")[0].setRoot(this.pages[page]);
  }

  initPushNotificacions() {
    const options: any = {
      android: { icon: 'notification', iconColor: "black" },
      ios: { alert: 'true', sound: 'true' }
    };
    const pushObject = this.push.init(options);
    pushObject.on('notification').subscribe((notification: any) => {
      if (notification.additionalData.type == "service.update") {
        this.events.publish("service.update", notification);
        this.alertCtrl.create({
          title: notification.title,
          message: notification.message,
          buttons: [{
            text: this.translations["OK"], role: "cancel"
          }, {
            text: this.translations["See detail"],
            handler: () => {
              this.navCtrl.push(AppointmentDetailPage, { appointmentId: notification.additionalData.id });
            }
          }]
        }).present();
      } else if (notification.additionalData.type == "service.pending") {
        this.events.publish("service.pending", notification);
        this.alertCtrl.create({
          title: notification.title,
          message: notification.message,
          buttons: [{
            text: this.translations["OK"], role: "cancel"
          }, {
            text: this.translations["See services"],
            handler: () => {
              this.navCtrl.push(AppointmentsPage, { activeItem: 'pending' });
            }
          }]
        }).present();
      } else {
        this.alertCtrl.create({
          title: notification.title,
          message: notification.message,
          buttons: [this.translations["OK"]]
        }).present();
      }
    });
    pushObject.on('registration').subscribe((registration: any) => {
      this.userService.registerDevice(registration.registrationId, registration.registrationType).subscribe(data => {}, error => {
        console.error("Error while registering device", JSON.stringify(error));
      });
    });
  }


  checkLogin(){
    if (this.loading) {
      return;
    } else {
      this.loading = true;
    }
    let loader = this.loadingCtrl.create();
    loader.present();
    this.sessionService.isLogged().then(isLogged => {
      this.loading = false;
      loader.dismiss();
      if (isLogged) {
        this.jwtService.checkToken();
        this.initPushNotificacions();
        this.sessionService.getUser().then(data => this.setUser(data));
      } else {
        this.rootPage = LoginPage;
        this.menuCtrl.enable(false);
      }
    }).catch(error => {
      this.loading = false;
      loader.dismiss();
      this.rootPage = LoginPage;
      this.alertCtrl.create({
        message: error,
        buttons: [this.translations["OK"]]
      }).present();
    });
  }

  choosePlatform(){
    let alert = this.alertCtrl.create({
      message: this.translations['Invite your friends to download WUAPPA on'],
      buttons: [
        {
          text: 'Google Play',
          handler: () => {
            this.shareApp('android')
          }
        },
        {
          text: 'App Store',
          handler: () => {
            this.shareApp('ios')
          }
        }
      ]
    })
    alert.present();
  }

  shareApp(platform = null){
    let urlIos = 'http://bit.do/wuappa-ios';
    let urlAndroid = 'http://bit.do/wuappa-android';
    let message = `
    ${this.translations['Friends! I just had a beauty treatment at home! Download the WUAPPA app and book your own beauty professional anytime anywhere. Beautify yourself!']}
Google Play: ${urlAndroid}
AppStore: ${urlIos}`;
    this.socialSharing.share(message, 'WUAPPA', null, null).then(() => {
    }, error => {
      console.error(error);
    })
  }

}
