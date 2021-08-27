import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Storage } from '@ionic/storage';

import { APIService } from './api-service';
import { TokenService } from './token-service';

import 'rxjs/add/operator/do';
import { TranslateService } from '@ngx-translate/core';

@Injectable()
export class SignupService extends APIService {

    private userInfo: any;
    private documents: any = [];
    private termsAccepted: boolean;
    private userType: any;
    private url_image: string = '';
    private validRegister: boolean;
    public citySelected: any;
    public zoneSelected: any = [];
    public daysSelected: any = [];
    public hoursSelected: any = [];
    private workzones: any = []
    private services: any = []
    public account_name: any;
    public iban: any;
    public swift: any;
    private card: any = {
        name: "",
        surname: "",
        cardnumber: "",
        expiration:"",
        cvc: ""
    }
    constructor(
        protected storage: Storage,
        protected http: HttpClient,
        protected tokenService: TokenService,
        protected translateService: TranslateService
    ) { super(http); }

    setUserInfo(formData): void {
        let phoneNumber = formData.phoneNumber.replace(/^0+/,'');

        this.userInfo = {
          first_name: formData.name,
          last_name: formData.surname,
          email: formData.email,
          phone: `${formData.prefix}${phoneNumber}`,
          password1: formData.password1,
          password2: formData.password2,
        };
    }

    setProfileImage(image): void {
        this.url_image = image;
    }

    setTerms(terms): void {
        this.termsAccepted = terms;
    }

    setUserType(userType): void{
        this.userType = userType;
    }

    getUserType() {
        return this.userType;
    }

    getProfileImage() {
        return this.url_image;
    }

    setCity(citySelected): void {
        this.citySelected = citySelected;
    }

    getCity() {
        return this.citySelected;
    }

    setWorkZones(zoneSelected){
        this.zoneSelected = zoneSelected;
        this.workzones = this.zoneSelected;
    }
    setWorkDays(daysSelected){
        this.daysSelected = daysSelected;
    }
    setWorkHours(hoursSelected){
        this.hoursSelected = hoursSelected;

    }
    setSwiftAndIban(account_name, swift, iban){
        this.account_name = account_name;
        this.swift = swift;
        this.iban = iban;
    }

    setDocuments (documents){
        this.documents = documents;
    }

    setServices(services) {
        this.services = services;
    }

    registerUser(){
        let data = {
            first_name: this.userInfo.first_name,
            last_name: this.userInfo.last_name,
            email: this.userInfo.email,
            phone: this.userInfo.phone,
            password1: this.userInfo.password1,
            password2: this.userInfo.password2,
            picture: this.url_image,
            type: this.userType,
            language: this.translateService.currentLang
        }
        //Create an array with the ids of the cities
        let cityList = [];
        cityList = this.citySelected.map(city => city.id);

        if(this.userType === 'PRO') {
          data['account_name'] = this.account_name;
          data['iban_bank_account'] = this.iban;
          data['swift_bank_account'] = this.swift;
          data['documents'] = this.documents;
          data['work_zones'] = this.workzones;
          data['services'] = this.services;
          data['work_days'] = this.daysSelected;
          data['work_hours'] = this.hoursSelected;
          data['city'] = cityList;
        }


        return this.http.post(this.getApiUrl('registration'), data);
    }

    sendSMS() {
      let data = {
          phone: this.userInfo.phone,
      };
      return this.http.post(this.getApiUrl('SMSRequest'), data);
    }

    verifySMS(code){
      let data = {
          phone: this.userInfo.phone,
          code: code
      };
      return this.http.post(this.getApiUrl('SMSVerify'), data);
     }

    signupFacebook(data) {
        var facebookToken = {
            access_token: data
        }
        return this.http.post(this.getApiUrl('facebook'), facebookToken).do(response => {
          const responseToken = response as any; // STC: Stupid TypeScript Cast
            if (responseToken.token || false) {
              this.tokenService.setToken(responseToken.token);
          }
        });
    }

    setValidRegister(value){
        this.validRegister = value;
    }

    getValidRegister(): boolean{
        return this.validRegister;
    }
    setCard(value): void{
        this.card.name = value.name
        this.card.surname = value.surname
        this.card.cardnumber = value.cardnumber
        this.card.expiration = value.expiration
        this.card.cvc = value.cvc
    }

    checkEmail(email){
        return this.http.post(this.getApiUrl('check_email'),{email: email});
    }

}
