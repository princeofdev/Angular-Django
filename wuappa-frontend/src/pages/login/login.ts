import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { SignupPage } from '../signup/signup';
import { SignupService } from '../../providers/signup-service';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core'
import { UIComponent } from '../../classes/component';
import { LoginAccessPage } from '../login-access/login-access';


@IonicPage({
  'name': 'login-page'
})
@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
})
export class LoginPage extends UIComponent{

  itemActive: any;
  public form: FormGroup;
  private translations;

  constructor(public navCtrl: NavController,
    public navParams: NavParams,
     private translateService: TranslateService,
     private fb: FormBuilder,
     private signupService: SignupService) {
      super();
      this.itemActive = 'all';
      this.form = this.fb.group({
        email: ["", Validators.required],
        password: ["", Validators.required]
      });
      this.translateService.get(['LOADING']).subscribe(values => {
        this.translations = values;
      });
  }

  setLogin() {
    this.navCtrl.push(LoginAccessPage);
  }

  setRegister() {
    this.itemActive = 'register';
  }

  goToPrev(){
    this.itemActive = 'all';
  }

  goToSignUp(userType){
    this.signupService.setUserType(userType);
    this.navCtrl.push(SignupPage);
  }

}
