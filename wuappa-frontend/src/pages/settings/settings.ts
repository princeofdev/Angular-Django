import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, AlertController, LoadingController, ToastController, App } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { UserService } from '../../providers/user-service';
import { TranslateService } from '@ngx-translate/core'
import { ChangePasswordPage } from '../../pages/change-password/change-password';
import { SessionService } from '../../providers/session-service';
import { LoginPage } from '../login/login';

@IonicPage()
@Component({
  selector: 'page-settings',
  templateUrl: 'settings.html',
})
export class SettingsPage extends UIComponent {
  editView: boolean;
  public form: FormGroup;
  public showIcon : string;
  private error: any;
  public user: any = null;
  public translations: any;
  private title: any;
  private english: any = '';
  private french: any = '';
  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private fb: FormBuilder,
    private userService: UserService,
    private translateService: TranslateService,
    private loadingCtrl: LoadingController,
    private alertCtrl: AlertController,
    private toastCtrl: ToastController,
    private sessionService: SessionService,
    private app: App
    ) {
    super();
    this.editView = false;
    this.form = this.fb.group({
      first_name: ["", Validators.required],
      last_name: ["", Validators.required],
      email: ["", Validators.required],
      phone: ["", Validators.required],
      language: [""]
    });

    this.translateService.get(['LOADING', 'Your changes has been changed', 'Settings', 'OK', 'Cancel', 'Sign out','To update the app with the new language, you need to sign out.','English','French']).subscribe(values => {
      this.translations = values;
      this.title = values['Settings'];
      this.english = values['English'];
      this.french = values['French'];
      this.getUser();

    });
  }

  getUser(){
    let loader = this.loadingCtrl.create({content: this.translations['LOADING']});
    loader.present();
    this.userService.getUser().subscribe(user => {
      console.log('user',user);

      this.user = user;
      if(typeof user['profile'].language !== 'undefined'){
         this.form.controls['language'].setValue(user['profile'].language);
      }
      loader.dismiss();
    }, error => {
      this.setUIError();
      loader.dismiss();
      this.alertCtrl.create({
        message: this.userService.errorToString(error),
        buttons: [this.translations['OK']]
      }).present();
    });
  }

  clearInput(event){
    this.user.first_name = "";
  }

  inputCliked(input){
    this.showIcon = input;
  }

  saveProfile(){
    this.editView = false;
    let loader = this.loadingCtrl.create({content: this.translations["LOADING"]});
    loader.present();
    let old_language = this.user.profile.language;
    this.userService.updateUser(this.form.value).subscribe(data => {
        loader.dismiss();
        this.user = data;
        if(typeof old_language !== 'undefined' && old_language !== this.form.value.language){
          this.userService.setStoredLanguage(this.form.value.language);
          this.alertCtrl.create({
            title: this.translations['Sign out'],
            subTitle: this.translations['To update the app with the new language, you need to sign out.'],
            buttons: [{
              text: this.translations['OK'],
              role: 'OK',
              handler: () => {
                this.translateService.use(this.form.value.language).subscribe(results => {
                  this.sessionService.logout();
                  this.app.getActiveNavs("menuRoot")[0].setRoot(LoginPage);
                }, error => {
                  this.app.getActiveNavs("menuRoot")[0].setRoot(LoginPage);
                });
              }
            }]
          }).present();
        }

        this.showToast(this.translations['Your changes has been changed']);
        this.getBackgroundProfile();
    }, error =>{
        this.setUIError();
        loader.dismiss();
        this.alertCtrl.create({
          message: this.error,
          buttons: [this.translations["OK"]]
        }).present();
    });
  }

  goToChangePasswordPage(){
    this.saveProfile();
    this.navCtrl.push(ChangePasswordPage);
  }

  showToast(text){
    let toast = this.toastCtrl.create({
      message: text,
      duration: 3000,
      position: 'bottom'
    });
    toast.present();
  }

  getBackgroundProfile(){
    let userHasImage = this.user && this.user.profile && (this.user.profile.picture != '' && this.user.profile.picture != null);
    let myStyles = {
      'background-image': userHasImage ? 'url('+this.user.profile.picture+')' : 'url("assets/imgs/profile-default-image.png")'
    };
    return myStyles;
  }

  setBackgroundProfile(url){
    if (this.user && this.user.profile) {
      this.user.profile.picture = url;
      this.userService.setProfileImage(url);
    }
  }

  changeImage(url) {
    this.setBackgroundProfile(url);
    this.getBackgroundProfile();
  }

}
