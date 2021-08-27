import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, AlertController, LoadingController, App } from 'ionic-angular';
import { Facebook, FacebookLoginResponse } from '@ionic-native/facebook';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core';
import { UIComponent } from '../../classes/component';
import { SessionService } from '../../providers/session-service';
import { SignupService } from '../../providers/signup-service';
import { MenuPage } from '../menu/menu';
import { RecoverPasswordPage } from '../recover-password/recover-password';
import { UserService } from '../../providers/user-service';
import * as moment from 'moment';
import { LANGUAGES } from '../../app/constants';
/**
 * Generated class for the LoginAccessPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-login-access',
  templateUrl: 'login-access.html',
})
export class LoginAccessPage extends UIComponent{

  public form: FormGroup;
  private translations: any = [];
  constructor(
    private sessionService: SessionService,
    public navCtrl: NavController,
    private loadingCtrl: LoadingController,
    private alertCtrl: AlertController,
    private fb: FormBuilder,
    private app: App,
    private signupService: SignupService,
    private facebook: Facebook,
    public navParams: NavParams,
    private translateService: TranslateService,
    private userService: UserService
  ) {
    super();
    this.form = this.fb.group({
      email: ["", Validators.required],
      password: ["", Validators.required]
    });
    this.translateService.get([
      'LOADING',
      'Welcome to Wuapa. In order to log in for the first time please check you email inbox and click in the link “Verify my email address” in order to to verify your email address and activate your account',
      'We have sent you a new verification e-mail. Please, check your inbox',
      "Resend verification e-mail", "OK"
    ]).subscribe(values => {
      this.translations = values;
    });
  }

  login(): void {
    let loader = this.loadingCtrl.create();
    loader.present();
    this.sessionService.login(this.form.value).subscribe(data => {
      loader.dismiss();
      if(data['user'].profile.language && LANGUAGES.indexOf(data['user'].profile.language) >= 0){
        this.userService.setStoredLanguage(data['user'].profile.language);
        this.translateService.use(data['user'].profile.language).subscribe(results =>{
          moment.locale(data['user'].profile.language);
          this.app.getActiveNavs("appRoot")[0].setRoot(MenuPage);
        },error =>{
            this.showErrorAlert(error);
        });
      }else{
        this.app.getActiveNavs("appRoot")[0].setRoot(MenuPage);
      }
    }, error => {
        this.setUIError();
        loader.dismiss();
        let errorString = this.signupService.errorToString(error);
        if (errorString == "E-mail is not verified.") {
          this.alertCtrl.create({
            subTitle: this.translations['Welcome to Wuapa. In order to log in for the first time please check you email inbox and click in the link “Verify my email address” in order to to verify your email address and activate your account'],
            buttons: [{
              text: this.translations['OK'],
              role: "cancel"
            }, {
              text: this.translations["Resend verification e-mail"],
              handler: () => {
                loader = this.loadingCtrl.create();
                loader.present();
                this.sessionService.resendVerificationEmail(this.form.value.email).subscribe(data => {
                  loader.dismiss();
                  this.alertCtrl.create({
                    subTitle: this.translations['We have sent you a new verification e-mail. Please, check your inbox'],
                    buttons: [this.translations['OK']]
                  }).present();
                }, error => {
                  loader.dismiss();
                  this.showErrorAlert(error);
                });
              }
            }]
          }).present();
        } else {
          this.showErrorAlert(error);
        }
      }
    )
  }

  showErrorAlert(error) {
    this.alertCtrl.create({
      subTitle: this.signupService.errorToString(error),
      buttons: [this.translations['OK']]
    }).present();
  }

  loginFb() {
    this.facebook.login(['public_profile', 'email'])
      .then((res: FacebookLoginResponse) => this.tokenFb(res.authResponse.accessToken))
      .catch(error => this.showErrorAlert(error));
  }

  tokenFb(token): void {
    this.setUILoading();
    let loader = this.loadingCtrl.create();
    loader.present();
    this.signupService.signupFacebook(token).subscribe(data => {
        this.setUIIdeal();
        loader.dismiss();
        this.app.getActiveNavs("appRoot")[0].setRoot(MenuPage);
    }, error => {
        this.setUIError();
        loader.dismiss();
        this.showErrorAlert(error)
    });

  }
  goToPrev(){
    this.navCtrl.pop();
  }
  goToRecoverPage(){
    this.navCtrl.push(RecoverPasswordPage);
  }



}
