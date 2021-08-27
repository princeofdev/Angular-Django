import { Component, ChangeDetectorRef } from '@angular/core';
import { IonicPage, NavController, NavParams, LoadingController, AlertController, App, LoadingOptions } from 'ionic-angular';
import { SignupAddPicturePage } from '../signup-add-picture/signup-add-picture';
import { UIComponent } from '../../classes/component';
import { TermsConditionsPage } from '../terms-conditions/terms-conditions';

import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { SignupService } from '../../providers/signup-service';
import { Facebook, FacebookLoginResponse } from '@ionic-native/facebook';
import { TranslateService } from '@ngx-translate/core';
import { ValidateService } from '../../providers/validate-service';
import {Observable} from 'rxjs/Rx';
import { MenuPage } from '../menu/menu';



@IonicPage()
@Component({
  selector: 'page-signup',
  templateUrl: 'signup.html',
})
export class SignupPage extends UIComponent {
  public title: any;
  public registerMode: any;
  public form: FormGroup;
  private loading;
  private error: any;
  public userType: any;
  public prefix: any;
  ok: 'OK';
  notEqualPassword: boolean;
  public countries = [
    ["Afghanistan", "+93"],
    ["Albania", "+355"],
    ["Algeria", "+213"],
    ["American Samoa", "+684"],
    ["Andorra", "+376"],
    ["Angola", "+244"],
    ["Anguilla", "+264"],
    ["Antarctica", "+672"],
    ["Antigua and Barbuda", "+268"],
    ["Argentina", "+54"],
    ["Armenia", "+374"],
    ["Aruba", "+297"],
    ["Australia", "+61"],
    ["Austria", "+43"],
    ["Azerbaijan", "+994"],
    ["Bahamas", "+242"],
    ["Bahrain", "+973"],
    ["Bangladesh", "+880"],
    ["Barbados", "+246"],
    ["Belarus", "+375"],
    ["Belgium", "+32"],
    ["Belize", "+501"],
    ["Benin", "+229"],
    ["Bermuda", "+441"],
    ["Bhutan", "+975"],
    ["Bolivia, Plurinational State of", "+591"],
    ["Bonaire, Sint Eustatius and Saba", "+599"],
    ["Bosnia and Herzegovina", "+387"],
    ["Botswana", "+267"],
    ["Bouvet Island", "+47"],
    ["Brazil", "+55"],
    ["British Indian Ocean Territory", "+246"],
    ["Brunei Darussalam", "+673"],
    ["Bulgaria", "+359"],
    ["Burkina Faso", "+226"],
    ["Burundi", "+257"],
    ["Cambodia", "+855"],
    ["Cameroon", "+237"],
    ["Canada", "+1"],
    ["Cape Verde", "+238"],
    ["Cayman Islands", "+345"],
    ["Central African Republic", "+236"],
    ["Chad", "+235"],
    ["Chile", "+56"],
    ["China", "+86"],
    ["Christmas Island", "+61"],
    ["Cocos (Keeling) Islands", "+891"],
    ["Colombia", "+57"],
    ["Comoros", "+269"],
    ["Congo", "+242"],
    ["Congo, the Democratic Republic of the", "+243"],
    ["Cook Islands", "+682"],
    ["Costa Rica", "+506"],
    ["Croatia", "+385"],
    ["Cuba", "+53"],
    ["Curaçao", "+599"],
    ["Cyprus", "+357"],
    ["Czech Republic", "+420"],
    ["Côte d'Ivoire", "+225"],
    ["Denmark", "+45"],
    ["Djibouti", "+253"],
    ["Dominica", "+767"],
    ["Dominican Republic", "+809"],
    ["Ecuador", "+593"],
    ["Egypt", "+20"],
    ["El Salvador", "+503"],
    ["Equatorial Guinea", "+240"],
    ["Eritrea", "+291"],
    ["Estonia", "+372"],
    ["Ethiopia", "+251"],
    ["Falkland Islands (Malvinas)", "+500"],
    ["Faroe Islands", "+298"],
    ["Fiji", "+679"],
    ["Finland", "+358"],
    ["France", "+33"],
    ["French Guiana", "+594"],
    ["French Polynesia", "+689"],
    ["French Southern Territories", "+689"],
    ["Gabon", "+241"],
    ["Gambia", "+220"],
    ["Georgia", "+995"],
    ["Germany", "+49"],
    ["Ghana", "+233"],
    ["Gibraltar", "+350"],
    ["Greece", "+30"],
    ["Greenland", "+299"],
    ["Grenada", "+473"],
    ["Guadeloupe", "+590"],
    ["Guam", "+671"],
    ["Guatemala", "+502"],
    ["Guernsey", "+1481"],
    ["Guinea", "+225"],
    ["Guinea-Bissau", "+245"],
    ["Guyana", "+592"],
    ["Haiti", "+509"],
    ["Heard Island and McDonald Islands", "+61"],
    ["Holy See (Vatican City State)", "+379"],
    ["Honduras", "+504"],
    ["Hong Kong", "+852"],
    ["Hungary", "+36"],
    ["Iceland", "+354"],
    ["India", "+91"],
    ["Indonesia", "+62"],
    ["Iran, Islamic Republic of", "+98"],
    ["Iraq", "+964"],
    ["Ireland", "+353"],
    ["Isle of Man", "+44"],
    ["Israel", "+972"],
    ["Italy", "+39"],
    ["Jamaica", "+876"],
    ["Japan", "+81"],
    ["Jersey", "+44"],
    ["Jordan", "+962"],
    ["Kazakhstan", "+7"],
    ["Kenya", "+254"],
    ["Kiribati", "+686"],
    ["Korea, Democratic People's Republic of", "+850"],
    ["Korea, Republic of", "+82"],
    ["Kuwait", "+965"],
    ["Kyrgyzstan", "+996"],
    ["Lao People's Democratic Republic", "+856"],
    ["Latvia", "+371"],
    ["Lebanon", "+961"],
    ["Lesotho", "+266"],
    ["Liberia", "+231"],
    ["Libya", "+218"],
    ["Liechtenstein", "+423"],
    ["Lithuania", "+370"],
    ["Luxembourg", "+352"],
    ["Macao", "+853"],
    ["Macedonia, The Former Yugoslav Republic of", "+389"],
    ["Madagascar", "+261"],
    ["Malawi", "+265"],
    ["Malaysia", "+60"],
    ["Maldives", "+960"],
    ["Mali", "+223"],
    ["Malta", "+356"],
    ["Marshall Islands", "+692"],
    ["Martinique", "+596"],
    ["Mauritania", "+222"],
    ["Mauritius", "+230"],
    ["Mayotte", "+262"],
    ["Mexico", "+52"],
    ["Micronesia, Federated States of", "+691"],
    ["Moldova, Republic of", "+373"],
    ["Monaco", "+355"],
    ["Mongolia", "+976"],
    ["Montenegro", "+382"],
    ["Montserrat", "+664"],
    ["Morocco", "+212"],
    ["Mozambique", "+258"],
    ["Myanmar", "+95"],
    ["Namibia", "+264"],
    ["Nauru", "+674"],
    ["Nepal", "+977"],
    ["Netherlands", "+31"],
    ["New Caledonia", "+687"],
    ["New Zealand", "+64"],
    ["Nicaragua", "+505"],
    ["Niger", "+277"],
    ["Nigeria", "+234"],
    ["Niue", "+683"],
    ["Norfolk Island", "+672"],
    ["Northern Mariana Islands", "+670"],
    ["Norway", "+47"],
    ["Oman", "+968"],
    ["Pakistan", "+92"],
    ["Palau", "+680"],
    ["Palestinian Territory, Occupied", "+970"],
    ["Panama", "+507"],
    ["Papua New Guinea", "+675"],
    ["Paraguay", "+595"],
    ["Peru", "+51"],
    ["Philippines", "+63"],
    ["Pitcairn", "+872"],
    ["Poland", "+48"],
    ["Portugal", "+351"],
    ["Puerto Rico", "+787"],
    ["Qatar", "+974"],
    ["Romania", "+40"],
    ["Russian Federation", "+7"],
    ["Rwanda", "+250"],
    ["Réunion", "+262"],
    ["Saint Barthélemy", "+590"],
    ["Saint Helena, Ascension and Tristan da Cunha", "+290"],
    ["Saint Kitts and Nevis", "+869"],
    ["Saint Lucia", "+758"],
    ["Saint Martin (French part)", "+590"],
    ["Saint Pierre and Miquelon", "+508"],
    ["Saint Vincent and the Grenadines", "+784"],
    ["Samoa", "+685"],
    ["San Marino", "+378"],
    ["Sao Tome and Principe", "+239"],
    ["Saudi Arabia", "+966"],
    ["Senegal", "+221"],
    ["Serbia", "+381"],
    ["Seychelles", "+248"],
    ["Sierra Leone", "+232"],
    ["Singapore", "+65"],
    ["Sint Maarten (Dutch part)", "+599"],
    ["Slovakia", "+421"],
    ["Slovenia", "+386"],
    ["Solomon Islands", "+677"],
    ["Somalia", "+252"],
    ["South Africa", "+27"],
    ["South Georgia and the South Sandwich Islands", "+500"],
    ["South Sudan", "+211"],
    ["Spain", "+34"],
    ["Sri Lanka", "+94"],
    ["Sudan", "+249"],
    ["Suriname", "+597"],
    ["Svalbard and Jan Mayen", "+47"],
    ["Swaziland", "+268"],
    ["Sweden", "+46"],
    ["Switzerland", "+41"],
    ["Syrian Arab Republic", "+963"],
    ["Taiwan, Province of China", "+886"],
    ["Tajikistan", "+992"],
    ["Tanzania, United Republic of", "+255"],
    ["Thailand", "+66"],
    ["Timor-Leste", "+670"],
    ["Togo", "+228"],
    ["Tokelau", "+690"],
    ["Tonga", "+676"],
    ["Trinidad and Tobago", "+868"],
    ["Tunisia", "+216"],
    ["Turkey", "+90"],
    ["Turkmenistan", "+993"],
    ["Turks and Caicos Islands", "+649"],
    ["Tuvalu", "+688"],
    ["Uganda", "+256"],
    ["Ukraine", "+380"],
    ["United Arab Emirates", "+971"],
    ["United Kingdom", "+44"],
    ["United States", "+1"],
    ["United States Minor Outlying Islands", "+1"],
    ["Uruguay", "+598"],
    ["Uzbekistan", "+998"],
    ["Vanuatu", "+678"],
    ["Venezuela, Bolivarian Republic of", "+58"],
    ["Viet Nam", "+84"],
    ["Virgin Islands, British", "+284"],
    ["Virgin Islands, U.S.", "+340"],
    ["Wallis and Futuna", "+681"],
    ["Western Sahara", "+212"],
    ["Yemen", "+967"],
    ["Zambia", "+260"],
    ["Zimbabwe", "+263"],
    ["Åland Islands", "+358"],
  ]
  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private fb: FormBuilder,
    private signupService: SignupService,
    private facebook: Facebook,
    private loadingCtrl: LoadingController,
    private translateService: TranslateService,
    private alertCtrl: AlertController,
    private app: App,
    private cd: ChangeDetectorRef,
    private validateService: ValidateService) {
    super();
    this.userType = this.signupService.getUserType();
    this.form = this.fb.group({
      name: ["", Validators.required],
      surname: ["", Validators.required],
      email: ["",
        [Validators.required, Validators.pattern("^([a-zA-Z0-9-_\.\+]+)@([a-zA-Z0-9-_\.]+)(\.{1})([a-zA-Z]+)$")]
      ],
      prefix: [this.countries[214][1], [Validators.required]],
      phoneNumber: ["", Validators.required],
      password1: ["", Validators.required],
      password2: ["", Validators.required]
    });

    this.translateService.get('LOADING').subscribe(
      value => {
        this.loading = value;
      }
    );

    this.translateService.get('ERRORLOGIN').subscribe(
      value => {
        this.error = value;
      }
    )

    this.translateService.get('Sign up').subscribe(value =>{
      this.title = value;
    });
    this.translateService.get('OK').subscribe(value =>{
      this.ok = value;
    });
    this.registerMode = true;
  }

  createLoader() {
    return this.loadingCtrl.create({ message: this.loading } as LoadingOptions);
  }

  showErrorAlert(error) {
    this.alertCtrl.create({
      message: this.signupService.errorToString(error),
      buttons: [this.ok]
    }).present();
  }

  ngAfterViewInit() {
    this.cd.detectChanges();
  }

  validateForm() {
    if (this.isFormValid()) {
      this.notEqualPassword = false;
      let loader = this.loadingCtrl.create({ message: this.loading } as LoadingOptions);
      loader.present();
      Observable.forkJoin(
        this.validateService.validateEmail(this.form.value.email),
        this.validateService.validatePhone(`${this.form.value.prefix}${this.form.value.phoneNumber}`)
      ).subscribe(data => {
        loader.dismiss();
        if (this.userType == 'FIN') {
          this.goToAddPicturePage();
        } else {
          this.goToTermsAndConditions();
        }
      }, error => {
        console.error("error", error);
        loader.dismiss();
        this.showErrorAlert(error);
      });
    } else {
      if (!this.passwordsMatch()) {
        this.notEqualPassword = true;
      }
    }
  }

  isFormValid(): boolean {
    return this.form.valid && this.passwordsMatch();
  }

  passwordsMatch(): boolean {
    let formData = this.form.value;
    return formData.password1 == "" || formData.password2 == "" || formData.password1 === formData.password2;
  }

  goToAddPicturePage() {
    this.signupService.setUserInfo(this.form.value);
    this.navCtrl.push(SignupAddPicturePage);
  }

  goToTermsAndConditions() {
    this.signupService.setUserInfo(this.form.value);
    this.setUILoading();
    let loader = this.loadingCtrl.create({ content: this.loading });
    loader.present();
    this.signupService.sendSMS().subscribe(data => {
      this.setUIIdeal();
      loader.dismiss();
      this.navCtrl.push(TermsConditionsPage);
    }, error => {
      loader.dismiss();
      this.setUIError();
      this.showErrorAlert(error);
    });
  }

  signupFb() {
    this.facebook.login(['public_profile', 'email'])
      .then((res: FacebookLoginResponse) => this.tokenFb(res.authResponse.accessToken))
      .catch(error => this.showErrorAlert(error));
  }

  tokenFb(token): void {
    this.setUILoading();
    let loader = this.loadingCtrl.create({ content: this.loading });
    loader.present();
    this.signupService.signupFacebook(token).subscribe(data => {
      this.setUIIdeal();
      loader.dismiss();
      this.app.getActiveNavs("appRoot")[0].setRoot(MenuPage);
    }, error => {
      loader.dismiss();
      this.setUIError();
      this.showErrorAlert(error);
    });

  }

  checkEmail(){
    this.setUILoading();
    let loader = this.loadingCtrl.create({ content: this.loading });
    loader.present();
    this.signupService.checkEmail(this.form.value['email']).subscribe(data =>{
      this.setUIIdeal();
      loader.dismiss();
    }, error => {
          loader.dismiss();
          this.setUIError();
          this.showErrorAlert(error);
    });
  }

}
