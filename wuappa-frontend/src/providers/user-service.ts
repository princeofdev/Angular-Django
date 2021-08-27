import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { APIService } from './api-service';
import { SessionService } from './session-service';
import { Storage } from '@ionic/storage';


@Injectable()
export class UserService extends APIService {

    public user: any = null;
    public image_url: any;

    constructor(protected http: HttpClient, protected sessionService: SessionService,private storage: Storage) { super(http); }

    updateUser(userData){
        //TODO: hecho solo para prefijos con 2 numeros (ejemplo: +34)
        let prefix = userData.phone.substring(0,3);
        let number = userData.phone.substring(3);
        number = number.replace(/^0+/, '');

        console.log('prefix',prefix);
        console.log('number',number);


      var data = {
          first_name: userData.first_name,
          last_name: userData.last_name,
          email: userData.email,
          profile:{
              phone: `${prefix}${number}`,
              picture: this.image_url,
              language: userData.language
          }
      }
      return this.http.patch(this.getApiUrl('user'), data);
    }
    updateBankAccount(userData){
        var data = {
            profile: {
                iban_bank_account: userData.iban_bank_account,
                swift_bank_account: userData.swift_bank_account,
                account_name: userData.account_name
            }
        }
        return this.http.patch(this.getApiUrl('user'), data);
    }
    updateWorkDays(workdays, workhours){
        var data = {
            profile: {
                work_days: workdays,
                work_hours: workhours,
            }
        }
        return this.http.patch(this.getApiUrl('user'), data);
    }

    getUser() {
      return this.http.get(this.getApiUrl('user'));
    }

    setNewPassword(formData){
        let url = this.getApiUrl('changePassword');
        return this.http.post(url,formData);
    }

    setProfileImage(url){
        this.image_url = url;
    }

    registerDevice(deviceId, type) {
      let url = this.getApiUrl('devices');
      if (type == "APNS") {
        url += "apns/";
      } else {
        url += "gcm/";
      }
      return this.http.post(url, { registration_id: deviceId });
    }

    setStoredLanguage(language_code) {
        this.storage.set('language',language_code);
    }

}
