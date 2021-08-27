import {Injectable, Injector} from '@angular/core';
import {HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse} from '@angular/common/http';
import {TranslateService} from '@ngx-translate/core';
import {App} from 'ionic-angular';
import {Observable} from 'rxjs/Observable';
import {LoginPage} from '../pages/login/login';

import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/empty';
import 'rxjs/add/observable/throw';

import {TokenService} from './token-service';

const HTTP_401_UNAUTHORIZED = 401;

@Injectable()
export class RequestsInterceptor implements HttpInterceptor {

    private translateService: TranslateService = null;
    private tokenService: TokenService = null;
    private app: App = null;

    constructor(private injector: Injector) {}

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
      if (!this.app) {
        this.app = this.injector.get(App);
      }
      if (!this.tokenService) {
        this.tokenService = this.injector.get(TokenService);
      }
      if (!this.translateService) {
        this.translateService = this.injector.get(TranslateService);
      }

      // Get the auth header from the service.
      if (this.tokenService.token) {
        req = req.clone({ headers: req.headers.set("Authorization", `Token ${this.tokenService.token}`) });
      }

      const languageCode = this.translateService.currentLang;
      if (languageCode || null) {
        req = req.clone({ headers: req.headers.set("Accept-Language", languageCode) });
      }

      return next.handle(req).catch(response => {
           if (response instanceof HttpErrorResponse && response.status == HTTP_401_UNAUTHORIZED) {
              this.tokenService.setToken(null);
              this.app.getRootNav().push(LoginPage);
          }
          try {
              return Observable.throw(JSON.parse(response.error));
          } catch (e) {
              return Observable.throw(response);
          }
      });
    }

}
