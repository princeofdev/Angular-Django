import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { SignupService } from '../../providers/signup-service';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { SignupAddPicturePage } from '../signup-add-picture/signup-add-picture';
import { AlertController } from 'ionic-angular/components/alert/alert-controller';
import { LoadingController } from 'ionic-angular/components/loading/loading-controller';
import { TranslateService } from '@ngx-translate/core';

@IonicPage()
@Component({
  selector: 'page-mobile-confirmation',
  templateUrl: 'mobile-confirmation.html',
})
export class MobileConfirmationPage extends UIComponent {
  validRegister: boolean;
  public form: FormGroup;
  translations: {};
  public title: any;
  public registerMode: any;

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private signupService: SignupService,
    private fb: FormBuilder,
    private alertCtrl: AlertController,
    private loadingCtrl:  LoadingController,
    private translate: TranslateService
  ) {
    super();
    this.form = this.fb.group({
      code: ["", Validators.required],
    });
    this.translate.get(["Loading",  "OK","Sign up"]).subscribe(results => {
      this.translations = results;
      this.title = results['Sign up'];
    });
    this.registerMode = true;
  }

  verifySMS() {
    const loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
    loader.present();
    this.signupService.verifySMS(this.form.value.code.toUpperCase()).subscribe(data => {
      loader.dismiss();
      this.navCtrl.push(SignupAddPicturePage);
    }, error => {
      loader.dismiss();
      this.alertCtrl.create({
        message: this.signupService.errorToString(error),
        buttons: [this.translations["OK"]]
      }).present();
    })
  }

}
