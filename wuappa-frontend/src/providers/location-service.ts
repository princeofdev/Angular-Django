import { Injectable } from '@angular/core';
import { APIService } from './api-service';

@Injectable()
export class LocationService extends APIService {

    getCountries(){
        return this.http.get(this.getApiUrl('countries'));
    }

    getRegions(country){
        return this.http.get(this.getApiUrl('regions', { country }));
    }

    getCities(region){
        return this.http.get(this.getApiUrl('cities', { region }));
    }

    getZones(city){
        return this.http.get(this.getApiUrl('zones', { city }));
    }

    getAllZones(){
        return this.http.get(this.getApiUrl('zones'));
    }

    updateUserZones(zones){
        return this.http.patch(this.getApiUrl('user'),zones);
    }

    getCityDetail(id){
        return this.http.get(`${this.getApiUrl('cities')}${id}/`);
    }

}
