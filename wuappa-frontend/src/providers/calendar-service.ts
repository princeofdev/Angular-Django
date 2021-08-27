import { Injectable } from '@angular/core';
import { APIService } from './api-service';
import { HttpClient } from '@angular/common/http';
import { UserService } from './user-service';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class CalendarService extends APIService {

    user: any = null;

    constructor(protected http: HttpClient,private userService: UserService){
        super(http);
        this.getUser().then(results => {

        });

    }

    getDaysOff(){
        if(this.user){
            return this.http.get(this.getApiUrl('daysoff'));
        }else{
            return Observable.empty<Response>();
        }
    }

    addDayOff(date){
        if(this.user){
            let data = {
                professional_email: this.user.email,
                date: date,
                professional: this.user.pk
            }
            return this.http.post(this.getApiUrl('daysoff'),data);
        }else{
            return Observable.empty<Response>();
        }
    }

    deleteDayOff(date){
        if(this.user){
            let url = this.getApiUrl('daysoff') + date + '/';
            return this.http.delete(url);
        }else{
           return Observable.empty<Response>();
        }
    }

    getUser(){
       return new Promise<any>((resolve,reject) => {
           this.userService.getUser().subscribe(results => {
               this.user = results;
               resolve(this.user);
           }, error => {
               reject(error);
           });
       });
    }

}
