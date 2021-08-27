import { Component } from '@angular/core';
import { IonicPage, NavController, LoadingController, AlertController } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { SessionService } from '../../providers/session-service';
import { TranslateService } from '@ngx-translate/core';
import { LoginPage } from '../login/login';

@IonicPage()
@Component({
  selector: 'page-recover-password',
  templateUrl: 'recover-password.html',
})
export class RecoverPasswordPage extends UIComponent{
  public form: FormGroup;
  public translations: any;
  public title: string;
  public registerMode: any;

  constructor(
    public navCtrl: NavController,
    private fb: FormBuilder,
    private sessionService: SessionService,
    private loadingCtrl: LoadingController,
    private alertCtrl: AlertController,
    private translateService: TranslateService
  ) {
    super();
    this.registerMode = true;
    this.form = this.fb.group({
      email: ["", Validators.required],
    });
    this.translateService.get([
    "OK",
    "We have sent you an e-mail to recover your password",
    "RECOVER_PASSWORD" ]).subscribe(values => {
      this.translations = values;
      this.title = values['RECOVER_PASSWORD'];
    });
   
  }

  recoverPassword(): void {
    let loader = this.loadingCtrl.create();
    loader.present();
    this.sessionService.recover(this.form.value.email).subscribe(data => {
      loader.dismiss();
      this.alertCtrl.create({
        message: this.translations["We have sent you an e-mail to recover your password"],
        buttons: [{
          text: this.translations["OK"],
          handler:() => { this.navCtrl.popTo(LoginPage); }
        }]
      }).present();
    }, error =>{
      loader.dismiss();
      this.alertCtrl.create({
        message: this.sessionService.errorToString(error),
        buttons: [this.translations["OK"]]
      }).present();
    });
  }

}
