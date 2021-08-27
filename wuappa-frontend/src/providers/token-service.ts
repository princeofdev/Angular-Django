import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Storage } from '@ionic/storage';
import { APIService } from './api-service';

import * as jwtDecode from 'jwt-decode';

export const TOKEN = "token";

@Injectable()
export class TokenService extends APIService {

    public token = null;

    constructor(http: HttpClient, protected storage: Storage) {
      super(http);
      this.storage.ready().then(() => {
        this.getToken().then().catch();
      })
    }

    public getToken() : Promise<string> {
      return new Promise((resolve, reject) => {
        if (this.token) {
          resolve(this.token);
        } else {
          this.storage.ready().then(() => {
            this.storage.get(TOKEN).then(token => {
              this.token = token || null;
              resolve(this.token);
            }).catch(error => {
              reject(error);
            })
          }).catch(error => {
            reject(error);
          })
        }
      });
    }

    public setToken(token) {
      this.token = token;
      return this.storage.set(TOKEN, token);
    }

    getUser() : Promise<any> {
      return new Promise((resolve, reject) => {
        this.getToken().then(token => {
          let user: any = jwtDecode(token);
          if (typeof user.pk == "undefined") {
            user.pk = user.user_id || null;
          }
          resolve(user);
        }).catch(error => {
          reject(error); 
        });
      });
    }

    refresh() {
      return new Promise((resolve, reject) => {
        this.getToken().then(token => {
          this.http.post(this.getApiUrl('refreshToken'), { token }).subscribe(response => {
              if (response["token"]) {
                
                  this.setToken(response["token"]);
                  resolve(response);
              } else {
                reject(response);
                this.setToken(null);
              }
          }, error => {
            reject(error);
            this.setToken(null);
          });
        }).catch(error => {
          reject(error);
        });
      });
    }

}
