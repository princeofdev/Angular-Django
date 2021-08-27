import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, AlertController, LoadingController } from 'ionic-angular';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';

import { UIComponent } from '../../classes/component';
import { SignupService } from '../../providers/signup-service';
import { DocumentationPage } from '../documentation-page/documentation-page';
import { ValidateService } from '../../providers/validate-service';
import { SessionService } from '../../providers/session-service';
import { UserService } from '../../providers/user-service';
import { TranslateService } from '@ngx-translate/core'


@IonicPage()
@Component({
  selector: 'page-account-page',
  templateUrl: 'account-page.html',
})
export class AccountPage extends UIComponent {
  private accountForm: FormGroup;
  public showIcon: string;
  public edit = true;
  public user: any;
  public savedSuccesfully: string;
  public title: any;
  private registerMode: any;
  translations = {};

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private fb: FormBuilder,
    private signupService: SignupService,
    public validateService: ValidateService,
    public alertCtrl: AlertController,
    private sessionService: SessionService,
    public loadingCtrl: LoadingController,
    private userService: UserService,
    public translateService: TranslateService
  ) {
    super();
    if (this.navParams.get("edit") === false) {
      this.edit = this.navParams.get("edit");
      this.registerMode = true;
    }

    this.translateService.get(['Saved Successfully','Bank account', 'OK']).subscribe(value => {
      this.savedSuccesfully = value['Saved Successfully'];
      this.title = value['Bank account'];
      this.translations = value;
    });
    
    this.accountForm = this.fb.group({
      account_name: ["", Validators.required],
      swift_bank_account: ["", Validators.required],
      iban_bank_account: ["", Validators.required]
    });
  }
  ngOnInit() {
    if (this.edit) {
      
      this.sessionService.getUpdatedUser().subscribe(results =>{
        this.setUser(results,true);
        }
      );
    }
  }
  setUser(user, edited = false) {
    this.user = user;
    if(edited){
      // this.accountForm = this.fb.group({
      //   account_name: [this.user.profile.account_name, Validators.required],
      //   swift_bank_account: [this.user.profile.swift_bank_account, Validators.required],
      //   iban_bank_account: [this.user.profile.iban_bank_account, Validators.required]
      // });
      this.accountForm.controls['account_name'].setValue(user.profile.account_name);
      this.accountForm.controls['swift_bank_account'].setValue(user.profile.swift_bank_account);
      this.accountForm.controls['iban_bank_account'].setValue(user.profile.iban_bank_account);
    }else{
      this.accountForm = this.fb.group({
        account_name: [this.user.account_name, Validators.required],
        swift_bank_account: [this.user.swift_bank_account, Validators.required],
        iban_bank_account: [this.user.iban_bank_account, Validators.required]
      });
    }
  }

  goToDocumentationPage() {
    let swift_bank_account = this.accountForm.value.swift_bank_account.toUpperCase();
    let iban_bank_account = this.accountForm.value.iban_bank_account.toUpperCase();
    let account_name = this.accountForm.value.account_name.toUpperCase();
    var self = this;
    let loader = this.loadingCtrl.create();
    loader.present();
    if (!this.edit) {
      this.validateService.validateBankAccount(
        swift_bank_account,
        iban_bank_account
      ).subscribe(success => {
        loader.dismiss();
        this.signupService.setSwiftAndIban(
          account_name,
          swift_bank_account,
          iban_bank_account
        );
        this.navCtrl.push(DocumentationPage);
      }, error => {
        loader.dismiss();
        this.alertCtrl.create({
          message: this.validateService.errorToString(error),
          buttons: [this.translations['OK']]
        }).present();
      });
    }else{
      this.userService.updateBankAccount(this.accountForm.value)
      .subscribe(data => {
        loader.dismiss();
        self.setUser(data, true);
        self.alertCtrl.create({
          message:  this.savedSuccesfully,
          buttons: [{ text: this.translations['OK'] }]
      }).present();
    }, error => {
        loader.dismiss();
        self.alertCtrl.create({
            message: this.userService.errorToString(error),
            buttons: [this.translations['OK']]
        }).present();
    });
    }
  }
  public onKey(event){
    this.accountForm.controls['swift_bank_account'].setValue(this.accountForm.value.swift_bank_account.toUpperCase());
    this.accountForm.controls['iban_bank_account'].setValue(this.accountForm.value.iban_bank_account.toUpperCase());
  }


}
