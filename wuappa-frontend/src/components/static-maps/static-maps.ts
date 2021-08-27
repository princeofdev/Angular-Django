import { Component, Output, EventEmitter } from '@angular/core';
import { LoadingController, AlertController, Platform } from 'ionic-angular';
import { Geolocation } from '@ionic-native/geolocation';
import { NativeGeocoder, NativeGeocoderReverseResult } from '@ionic-native/native-geocoder';
import { TranslateService } from '@ngx-translate/core';
import { LOCATION_TIMEOUT, STATIC_MAPS_API_KEY } from '../../app/constants';

@Component({
  selector: 'static-maps',
  templateUrl: 'static-maps.html'
})
export class StaticMapsComponent {
  private url_api_maps = '';
  coords = { lat: null, lng: null };
  @Output() onChange: EventEmitter<any> = new EventEmitter<any>();
  translations: any;

  constructor(
    private loadingCtrl: LoadingController,
    private geolocation: Geolocation,
    private nativeGeocoder: NativeGeocoder,
    private alertCtrl: AlertController,
    private translate: TranslateService,
    private platform: Platform
  ) {
    this.translate.get([
      "OK", "Loading",
      "We're sorry. We're unable to retrieve your current address."
    ]).subscribe(values => this.translations = values);
    this.setMap();
    this.loadLocation();
  }

  public changeLocation(event) {
    this.onChange.emit(event);
  }

  loadLocation() {
    this.geolocation.getCurrentPosition({ timeout: LOCATION_TIMEOUT }).then(resp => {
      this.setMap(resp.coords.latitude, resp.coords.longitude);
     }).catch((error) => {
       console.error('Error getting location', error);
       this.setMap();
     });
  }

  setMap(lat = null, lng = null) {
    if (lat && lng) {
      let maps_size = this.platform.width() + "x" + this.platform.height();
      this.coords = {
        lat: lat,
        lng: lng
      };
      let map_key = STATIC_MAPS_API_KEY;
      let maps_coords = `${this.coords.lat},${this.coords.lng}`;
      this.url_api_maps = `https://maps.googleapis.com/maps/api/staticmap?center=${maps_coords}&zoom=12&scale=2&size=${maps_size}&key=${map_key}&markers=color:red%7C${maps_coords}`;
    }
  }

  getBackgroundImage(){
    if (this.coords.lat == null || this.coords.lng == null) {
      return {};
    } else {
      return { 'background-image': `url("${this.url_api_maps}")`, 'opacity': 1 };
    }
  }

  useCurrentAddress() {
    if (this.coords) {
      let loader = this.loadingCtrl.create({ content: this.translate["Loading"] });
      loader.present();
      this.nativeGeocoder.reverseGeocode(this.coords.lat, this.coords.lng).then((result: NativeGeocoderReverseResult) => {
        loader.dismiss();
        this.onChange.emit({
          address: result.thoroughfare,
          address_details: result.subThoroughfare,
          city: `${result.locality} ${result.subLocality}`,
          state: `${result.administrativeArea} ${result.subAdministrativeArea}`,
          country: result.countryName,
          postal_code: result.postalCode
        });
      }).catch((error: any) => {
        loader.dismiss();
        console.error(error);
        this.alertCtrl.create({
          message: this.translations["We're sorry. We're unable to retrieve your current address."],
          buttons: [this.translations["OK"]]
        }).present();
      });
    } else {
      this.alertCtrl.create({
        message: this.translations["We're sorry. We're unable to retrieve your current address."],
        buttons: [this.translations["OK"]]
      }).present();
    }
  }

}
