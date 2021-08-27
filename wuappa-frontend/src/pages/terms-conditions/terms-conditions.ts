import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, LoadingController, AlertController } from 'ionic-angular';
import { LoginPage } from '../login/login';
import { SignupConfirmationPage } from '../signup-confirmation/signup-confirmation';
import { UIComponent } from '../../classes/component';
import { SignupService } from '../../providers/signup-service';
import { TranslateService } from '@ngx-translate/core';
import { MobileConfirmationPage } from '../mobile-confirmation/mobile-confirmation';


@IonicPage()
@Component({
  selector: 'page-terms-conditions',
  templateUrl: 'terms-conditions.html',
})
export class TermsConditionsPage extends UIComponent {
  private termsAccepted: boolean;
  private loading: any;
  public userType: any;
  public title: any;
  public registerMode: any;
  public translations = {};

  constructor(
    public navCtrl: NavController,
     public navParams: NavParams,
     private signupService: SignupService,
     private loadingCtrl: LoadingController,
     private translateService: TranslateService,
     private alertCtrl: AlertController) {
    super();
    this.translateService.get(['Sign up', 'OK']).subscribe(value =>{
      this.title = value['Sign up'];
      this.translations = value;
    })
    this.userType = this.signupService.getUserType();
    this.registerMode = true;
  }

  goToLoginPage(){
    this.navCtrl.push(LoginPage);
  }

  refuseTerms(){
    this.termsAccepted = false;
    this.navCtrl.pop();
  }

  showErrorAlert(error) {
    this.alertCtrl.create({
      message: this.signupService.errorToString(error),
      buttons: [this.translations["OK"]]
    }).present();
  }

  acceptTerms() {
    this.termsAccepted = true;
    this.translateService.get('LOADING').subscribe(value => { this.loading = value; });
    if (this.userType == 'FIN') {
      let loader = this.loadingCtrl.create({ content: this.loading });
      loader.present();
      this.signupService.registerUser().subscribe(results => {
        loader.dismiss();
        this.signupService.setValidRegister(true);
        this.navCtrl.push(SignupConfirmationPage);
      }, err => {
        loader.dismiss();
        this.showErrorAlert(err);
        this.signupService.setValidRegister(false);
        this.navCtrl.push(SignupConfirmationPage);
      });
    } else {
      this.navCtrl.push(MobileConfirmationPage);
    }
  }

}
