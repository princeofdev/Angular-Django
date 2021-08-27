import { Injectable } from '@angular/core';
import { APIService } from './api-service';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class AppointmentService extends APIService {

    constructor(protected http: HttpClient){
        super(http);
    }

    getFinalUserList(){
        return this.http.get(this.getApiUrl('hireservices'));
    }

    updateAppointment(id,data){
        return this.http.patch(this.getApiUrl('hireservices') + id + '/', data);
    }

    cancelAppointment(id){
        return this.http.delete(this.getApiUrl('hireservices') + id + '/');
    }

    refuseAppointment(id){
        return this.http.delete(this.getApiUrl('hireservices') + id + '/');
    }

    acceptAppointment(id){
        let data = {
            accept: true,
            id: id
        }
        return this.http.put(this.getApiUrl('hireservices'), data);
    }

    completeAppointment(id){
        let data = {
            complete: true,
            id: id
        };
        return this.http.put(this.getApiUrl('hireservices'), data);
    }

    getAppointmentDetail(id){
        return this.http.get(this.getApiUrl('hireservices') + id + '/');
    }


    updateCreditCard(stripeId,id){
        let data = {
            credit_card: stripeId,
        };
        return this.http.patch(this.getApiUrl('hireservices')+ id + '/',data);
    }

    sendReview(data){
        let new_data = {
            id: data.id,
            rating: data.rating,
            review: data.review,
            review_date: data.review_date
        };

        return this.http.put(this.getApiUrl('hireservices'),new_data);
    }

    checkAppointmentCancelability(id){
        let url = this.getApiUrl('hireservices') + `${id}/cancelability/`;
        return this.http.get(url);
    }

    notifyCustomer(id){
      let url = this.getApiUrl('hireservices') + `${id}/notify-customer/`;
      return this.http.post(url, {});
  }




}
