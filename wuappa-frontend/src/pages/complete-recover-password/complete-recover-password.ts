import { Component } from '@angular/core';
import { IonicPage, NavParams, LoadingController, AlertController, App } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { SessionService } from '../../providers/session-service';
import { LoginPage } from '../login/login';


@IonicPage()
@Component({
  selector: 'page-complete-recover-password',
  templateUrl: 'complete-recover-password.html',
})
export class CompleteRecoverPasswordPage extends UIComponent{
  public form: FormGroup;

  constructor(
    private app: App,
    private navParams: NavParams,
    private fb: FormBuilder,
    private sessionService: SessionService,
    private loadingCtrl: LoadingController,
    private alertCtrl: AlertController
  ) {
    super();
    this.form = fb.group({
      new_password1: ["", Validators.required],
      new_password2: ["", Validators.required],
    });
    this.setUIPartial();
  }

  recoverPassword(): void {
    let loader = this.loadingCtrl.create();
    loader.present();
    this.sessionService.resetPassword(
      this.navParams.get("uid"),
      this.navParams.get("token"),
      this.form.value.new_password1,
      this.form.value.new_password2
    ).subscribe(data => {
      this.setUIIdeal();
      loader.dismiss();
    }, error =>{
      loader.dismiss();
      this.setUIPartial();
      this.alertCtrl.create({
        message: this.sessionService.errorToString(error),
        buttons: ["OK"]
      }).present();
    }
    )

  }

  backToLogin() {
    this.app.getActiveNavs("menuRoot")[0].setRoot(LoginPage);
  }

}
