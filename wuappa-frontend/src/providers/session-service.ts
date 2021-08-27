import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { APIService } from './api-service';
import { TokenService } from './token-service';

import 'rxjs/add/operator/do';


@Injectable()
export class SessionService extends APIService {

    constructor(protected http: HttpClient, protected tokenService: TokenService) { super(http); }

    login(loginData) {
        return this.http.post(this.getApiUrl('login'), { email: loginData.email, password: loginData.password }).do(response => {
            const responseToken = response as any; // STC: Stupid TypeScript Cast
            const token = responseToken.token || null;
            if (token) {
                this.tokenService.setToken(token);
            }
        });
    }

    getUser() : Promise<any> {
      return this.tokenService.getUser();
    }

    getUpdatedUser(){
      return this.http.get(this.getApiUrl('user'));
    }

    setUser(user) {
      this.tokenService.refresh();
    }

    logout() {
        return this.tokenService.setToken(null);
    }

    isLogged() {
      return new Promise((resolve, reject) => {
        this.tokenService.getToken().then(value => {
          resolve((value != null));
        }).catch(error => {
          resolve(error);
        });
      })
    }

    recover(email) {
      return this.http.post(this.getApiUrl('resetPassword'), {email});
    }

    resetPassword(uid, token, new_password1, new_password2) {
      return this.http.post(this.getApiUrl('resetPasswordConfirm'), {
        uid, token, new_password1, new_password2
      });
    }

    changePassword(oldPassword, newPassword1, newPassword2) {
      return this.http.put(this.getApiUrl('changePassword'), {
        old_password: oldPassword,
        new_password1: newPassword1,
        new_password2: newPassword2
      });
    }

    resendVerificationEmail(email) {
      return this.http.post(this.getApiUrl('verifyEmail'), { email });
    }



}
