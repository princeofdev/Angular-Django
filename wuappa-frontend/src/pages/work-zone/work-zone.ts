import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, AlertController, LoadingController, LoadingOptions } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { LocationService } from '../../providers/location-service';
import { WorkZoneDistrictPage } from '../work-zone-district/work-zone-district';
import { SignupService } from '../../providers/signup-service';
import { TranslateService } from '@ngx-translate/core'
import { UserService } from '../../providers/user-service';
import { Observable } from '../../../node_modules/rxjs';


@IonicPage()
@Component({
    selector: 'page-work-zone',
    templateUrl: 'work-zone.html',
})
export class WorkZonePage extends UIComponent {
    private passwordForm: FormGroup;
    public countries: any;
    public regions: any;
    public cities: any = [];
    public countrySelected: any;
    public regionSelected: any;
    public citySelected: any;
    public loading: string;
    public title: any;
    public registerMode: any;
    private editMode: boolean = false;
    private user: any = [];
    constructor(
        public navCtrl: NavController,
        public navParams: NavParams,
        private fb: FormBuilder,
        private translateService: TranslateService,
        private signupService: SignupService,
        private locationService: LocationService,
        private alertCtrl: AlertController,
        private loadingCtrl: LoadingController,
        private userService: UserService
      ) {
        super();
        this.passwordForm = this.fb.group({
            old_password: ["", Validators.required],
            new_password1: ["", Validators.required],
            new_password2: ["", Validators.required]
        });
          this.editMode = this.navParams.get('editMode');

          this.getAllData();
          this.translateService.get(['LOADING','WORKZONE']).subscribe( value => {
            this.loading = value['LOADING'];
            this.title = value['WORKZONE'];
          } );
          this.registerMode = true;

    }

    createLoader() {
      return this.loadingCtrl.create({ message: this.loading } as LoadingOptions);
    }

    showErrorAlert(error) {
      this.alertCtrl.create({ message: this.locationService.errorToString(error) }).present();
    }

    getAllData() {
      let loader = this.createLoader();
      loader.present();
      this.locationService.getCountries().subscribe(data => {
        this.countries = data;
        loader.dismiss();
      }, error => {
        loader.dismiss();
        this.showErrorAlert(error);
      });
    }

    onCountryChange(newValue) {
      let loader = this.createLoader();
      loader.present();
      this.locationService.getRegions(newValue).subscribe( data => {
        this.regions = data;
        loader.dismiss();
      }, error => {
        loader.dismiss();
        this.showErrorAlert(error);
      });
    }

    onRegionChange(newValue) {
      let citiesRequest = [];
      for(let citieId of newValue){
        citiesRequest.push(this.locationService.getCities(citieId));
      }

      let loader = this.createLoader();
      loader.present();
      Observable.forkJoin(citiesRequest).subscribe(data => {
        let cities = [];
        for(let cityGroup of data){
          let group = cityGroup as Array<any>;
          for(let city of group){
            cities.push(city);

          }

        }
        this.cities = cities;
        loader.dismiss();
      }, error => {
        loader.dismiss();
        this.showErrorAlert(error);
      });
    }

    goToNextPage() {

      this.signupService.setCity(this.citySelected);
      this.navCtrl.push(WorkZoneDistrictPage, {
          citySelected: this.citySelected,
          editMode: false,
          editCityMode: this.editMode
      });
    }

}
