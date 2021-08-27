import { Injectable } from '@angular/core';
import { APIService } from './api-service';

@Injectable()
export class ServicesService extends APIService {

    private basket: any = [];

    getServicesByCity(cityId) {
        return this.http.get(this.getApiUrl('services', {cities: cityId}));
    }

    getCategoriesByZip(postal_code) {
        return this.http.get(this.getApiUrl('categories', {zip: postal_code}));
    }

    getServicesByZip(postal_code){
        return this.http.get(this.getApiUrl('services',{postal_code: postal_code}));
    }

    getServicesByCategoryAndZip(category,postal_code){
        return this.http.get(this.getApiUrl('services',{category: category,zip: postal_code}));
    }

    getServicesByWorkZones(work_zones){
        let data = '';
        for (let i = 0; i < work_zones.length; i++) {
            data += (i == work_zones.length - 1) ? work_zones[i] : work_zones[i] + ",";
        }
        return this.http.get(this.getApiUrl('services', data));        
    }

    addItemToBasket(item){
        let indexItem = this.checkItemIsInBasket(item.id);
        if(indexItem !== -1){
            this.basket[indexItem].count += 1;
            let price = parseFloat(this.basket[indexItem].price) + parseFloat(this.basket[indexItem].default_price);
            this.basket[indexItem].price = price;
        }else{
            let service = {
                id: item.id,
                count: 1,
                service: item,
                price: 0,
                price_currency: '',
                default_price: 0
            };
            if(item.cities.length > 0){
                service.price = item.cities[0].price;
                service.default_price = item.cities[0].price;
                service.price_currency = item.cities[0].price_currency;
            }else{
                service.price = 0;
                service.price_currency = '';
            }
            this.basket.push(service);
        }
    }

    getBasketList(){
        return this.basket;
    }

    checkItemIsInBasket(id){
        return this.basket.findIndex(item => item.id === id);
    }



    incrementService(id){
        let index = this.basket.findIndex(item => item.id === id);
        this.basket[index].count += 1;
        let price = parseFloat(this.basket[index].price) + parseFloat(this.basket[index].default_price);
        this.basket[index].price = price;
    }


    decrementService(id){
        let index = this.basket.findIndex(item => item.id === id);
        this.basket[index].count -= 1;
        let price = parseFloat(this.basket[index].price) - parseFloat(this.basket[index].default_price);
        if(price > 0){
            this.basket[index].price = price;
        }

        if(this.basket[index].count === 0){
            this.removeService(index);
        }
    }

    removeService(index){
        if(index > -1){
            this.basket.splice(index,1);
        }
    }

    isBasketEmpty(){
        return this.basket.length === 0;
    }

    cleanData(){
        this.basket = [];
    }

    getProfessionalServices(services){
        let data = '';
        for(let i=0; i< services.length;i++){
            data += (i == services.length - 1) ? services[i] : services[i] + ",";
        }
        return this.http.get(this.getApiUrl('services',data));        
    }

    updateProfessionalServices(data){
        return this.http.patch(this.getApiUrl('user'),data);
    }

}
