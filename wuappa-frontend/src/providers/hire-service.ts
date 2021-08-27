import { Injectable } from '@angular/core';
import { APIService } from './api-service';
import { DatePipe } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import * as moment from 'moment';
import { SessionService } from './session-service';
@Injectable()
export class HireService extends APIService {
    private date: any = null;
    private hour: any = null;
    private basket: any = null;
    private address: any = null;
    private city: any = null;
    private postal_code: any = null;
    private country: any = null;
    private state: any = null;
    private address_details: any = null;
    private comment: any = null;
    private user: any = null;
    private address_data: any = null;
    private card: any = null;
    private coupon_code: any = null;
    private specialPrice: any = null;
    constructor(
        protected http: HttpClient,
        protected datePipe: DatePipe,
        private sessionService: SessionService
    ) {
        super(http);
        this.getUser();
    }

    getUser(){
        this.sessionService.getUser().then(data => {
            this.user = data;
        });
    }

    setDate(date){
        this.date = date;
    }

    setCouponCode(coupon_code){
        this.coupon_code = coupon_code;
    }

    getDate(){
        return this.date;
    }

    setHour(hour){
        this.hour = hour;
    }

    getHour(){
        return this.hour;
    }

    getFormattedDate(){
        return this.datePipe.transform(this.date,'dd/MM/yyyy');
    }

    getFormattedHour(){
        return this.hour + ":00";
    }

    getFullDate(){
        let fullDate = this.getFormattedDate() + " - " + this.hour;
        return fullDate;
    }

    setBasket(basket){
        this.basket = basket;
    }

    getTotalPrice(){
        let totalPrice = 0;
        if(this.basket){
            for(var i= 0; i < this.basket.length;i++){
                    totalPrice += parseFloat(this.basket[i].price);
            }
        }
        return totalPrice;
    }

    setSpecialPrice(special_sprice){
        this.specialPrice = special_sprice;
    }

    getCurrency(){
        let currency = '';
        if(this.basket.length > 0){
            currency = this.basket[0].price_currency;

        }

        return currency;
    }

    getListOfServices(){
        let serviceList = '';
        for (let item of this.basket) {
            serviceList += `${item.count}x ${item.service.name}. `
        }
        return serviceList;
    }

    getServicesIdList(){
        let idList = [];
        if(this.basket.length > 0){
            for(var i=0;i<this.basket.length;i++){
                for(var j=0;j<this.basket[i].count;j++){
                    idList.push(this.basket[i].id);
                }
            }
        }
        return idList;
    }

    setAddress(address){
        this.address = address;
    }

    setCity(city){
        this.city = city;
    }

    setPostalCode(postal_code){
        this.postal_code = postal_code;
    }

    setCountry(country){
        this.country = country;
    }

    setState(state){
        this.state = state;
    }

    setAddressDetails(address_detail){
        this.address_details = address_detail;
    }

    setComment(comment){
        if(comment){
            this.comment = comment;
        }else{
            this.comment = "";
        }
    }

    getFullAddress(){
        if(this.address && this.postal_code && this.city && this.state && this.country && this.address_details){
            return this.address +", " + this.address_details + ", " + this.postal_code + ", " + this.city + ", " + this.state + ", " + this.country + ".";
        }else{
            return "";
        }
    }

    setAddressData(data){
        this.address_data = data;
    }

    setCard(card){
        this.card = card;
    }

    checkAvailability(dateData){
        let formatted_date = moment(dateData.date).format('YYYY-MM-DD');
        let data = {
            services: this.getServicesIdList(),
            zip: this.postal_code,
            date: formatted_date,
            time: dateData.time
        };
        return this.http.post(this.getApiUrl('professionalsavailability'),data);
    }

    sendData(){
        console.log("SEND DATA", JSON.stringify(this.user));
        let data = {
            date: this.datePipe.transform(this.date, 'yyyy-MM-dd'),
            time: this.getFormattedHour(),
            address: `${this.address} ${this.address_details}`,
            city: this.city,
            zip_code: this.postal_code,
            region: this.state,
            country: this.country,
            comments: this.comment,
            services: this.getServicesIdList(),
            client: this.user.pk || null,
            total: this.specialPrice,
            total_currency: this.getCurrency(),
            credit_card: this.card.stripe_id,
            coupon: this.coupon_code
        };
        return this.http.post(this.getApiUrl('hireservices'),data);
    }

    getHireServicesWithoutReview(){
        return this.http.get(this.getApiUrl('hireservices', { review: true }))
    }

    cleanService() {
        this.date = null;
        this.hour = null;
        this.basket = null;
        this.address = null;
        this.city = null;
        this.postal_code = null;
        this.country = null;
        this.state = null;
        this.comment = null;
        this.address_data = null;
        this.address_details = null;
    }

    public checkCoupon(coupon) {
        return this.http.get(this.getApiUrl('coupon') + coupon + "/");
    }

    public setCouponToUsed(coupon){
        let date = moment().toISOString();
        let data = {
            redemption: date,
            code: coupon,
            valid: false
        };
        return this.http.patch(this.getApiUrl('coupon') + coupon + "/",data);
    }

}
