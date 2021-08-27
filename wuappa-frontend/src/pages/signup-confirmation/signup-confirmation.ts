import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { SignupService } from '../../providers/signup-service';
import { LoginPage } from '../../pages/login/login';
import { TranslateService } from '@ngx-translate/core';
/**
 * Generated class for the SignupConfirmationPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-signup-confirmation',
  templateUrl: 'signup-confirmation.html',
})
export class SignupConfirmationPage extends UIComponent{
  validRegister: boolean;
  public title: any;
  public registerMode: any;
  constructor(
    public navCtrl: NavController, 
    public navParams: NavParams,
    private signupService: SignupService,
    private translateService: TranslateService) {
    super();
    this.registerMode = true;
    this.translateService.get(['Sign up']).subscribe(results =>{
      this.title = results['Sign up'];
    })
    this.validRegister = this.signupService.getValidRegister();
    if(this.validRegister){
      this.setUIIdeal();
    }else{
      this.setUIError();
    }
  }

  goToLoginPage(){
    this.navCtrl.push(LoginPage);
  }

  backToDetails(){
    this.navCtrl.popTo(this.navCtrl.getByIndex(this.navCtrl.length() - 4));
  }

  

}
