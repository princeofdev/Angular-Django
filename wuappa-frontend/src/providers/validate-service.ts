import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { APIService } from './api-service';

@Injectable()
export class ValidateService extends APIService{

    public user: any;
    public image_url: any;

    constructor( protected http: HttpClient) { super(http);  }

    validateEmail(email) {
        return this.http.post(this.getApiUrl('checkemail'), {email});
    }

    validatePhone(phone) {
        return this.http.post(this.getApiUrl('checkphone'), {phone});
    }

    validateBankAccount(swift_bank_account, iban_bank_account) {
      return this.http.post(this.getApiUrl('checkbankaccount'), {swift_bank_account, iban_bank_account});
  }

}
