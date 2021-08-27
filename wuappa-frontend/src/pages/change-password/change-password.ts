import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, ToastController,AlertController } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { UserService } from '../../providers/user-service';
import { SignupService } from '../../providers/signup-service';
import { TranslateService } from '@ngx-translate/core';



@IonicPage()
@Component({
  selector: 'page-change-password',
  templateUrl: 'change-password.html',
})
export class ChangePasswordPage extends UIComponent {
  private passwordForm: FormGroup;
  public translations: any
  public title: string;

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private userService: UserService,
    private fb: FormBuilder,
    private toastCtrl: ToastController,
    private alertCtrl: AlertController,
    private signupService: SignupService,
    private translateService: TranslateService) {
    super();
    this.passwordForm = this.fb.group({
      old_password: ["", Validators.required],
      new_password1: ["", Validators.required],
      new_password2: ["", Validators.required]
    });
    this.translateService.get(['Change password','Password changed correctly', 'OK']).subscribe(values => {
      this.translations = values;
      this.title = values['Change password'];
    });

  }

  passwordsMatch(){
    return this.passwordForm.value.new_password1 == this.passwordForm.value.new_password2;
  }

  isFormValid(){
    return this.passwordsMatch() && this.passwordForm.valid;
  }

  saveNewPassword(){
    let formData = this.passwordForm.value;
    this.userService.setNewPassword(formData)
      .subscribe(
        results => {

          this.showToast(this.translations['Password changed correctly']);

          this.navCtrl.pop();
        },
        error => {
          this.showErrorAlert(error);
        }
      )
  }

  showErrorAlert(error) {
    this.alertCtrl.create({
      message: this.signupService.errorToString(error),
      buttons: [this.translations['OK']]
    }).present();
  }


  showToast(text) {
    let toast = this.toastCtrl.create({
      message: text,
      duration: 3000,
      position: 'bottom'
    });

    toast.onDidDismiss(() => {
    });

    toast.present();
  }



}
