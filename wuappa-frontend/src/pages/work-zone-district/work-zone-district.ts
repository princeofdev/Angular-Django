import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, LoadingController, LoadingOptions, AlertController,ToastController } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { LocationService } from '../../providers/location-service';
import { SignupService } from '../../providers/signup-service';
import { AccountPage } from '../account-page/account-page';
import { TranslateService } from '@ngx-translate/core';
import { UserService } from '../../providers/user-service';
import { Observable } from 'rxjs/Rx';
import { WorkZonePage } from '../work-zone/work-zone';
import { AppointmentsPage } from '../appointments/appointments';
import { App } from 'ionic-angular/components/app/app';


@IonicPage()
@Component({
    selector: 'page-work-zone-district',
    templateUrl: 'work-zone-district.html',
})
export class WorkZoneDistrictPage extends UIComponent {

    public zones: any = [];
    public workZones:any;
    private citySelected: any = [];
    private citySelectedByUser: any = [];
    private city: any = [];
    private zonesAdded: any = [];
    private professionalZones: any = [];
    private editMode: boolean = false;
    private userWorkZones: any = [];
    private user;
    private translations: any;
    public title: any;
    public registerMode: any;
    public editCityMode: boolean = false;

    constructor(
      public navCtrl: NavController,
      public navParams: NavParams,
      private locationService: LocationService,
      private signupService: SignupService,
      private loadingCtrl: LoadingController,
      private alertCtrl: AlertController,
      private translateService: TranslateService,
      private userService: UserService,
      private toastCtrl: ToastController,
      private app: App

    ) {
      super();
      this.editMode = this.navParams.get('editMode');
      if(typeof this.editMode === 'undefined'){
        this.editMode = true;
      }else{
        this.editMode = false;
      }
      this.editCityMode = this.navParams.get('editCityMode');
      if (typeof this.editCityMode === 'undefined') {
        this.editCityMode = false;
      } else {
        this.editCityMode = true;
      }


      if(!this.editMode){
        this.registerMode = true;
        this.citySelected = this.navParams.get('citySelected');
        this.translateService.get(['LOADING', 'Zones updated correctly', 'WORKZONE', 'OK','Cancel',
            'If you change the cities, you need to fill the work zones again. Are you sure that you want to edit the cities?'
          ]).subscribe(value => {
              this.translations = value;
              this.title = this.translations['WORKZONE'];
        });
        this.getAllData();
        if(this.editCityMode){
          this.userService.getUser().subscribe(user => {
            this.user = user;
          })
        }
      }else{
        this.userService.getUser().subscribe(user =>{

          this.translateService.get(['LOADING','Zones updated correctly', 'WORKZONE','OK','Cancel',
          'If you change the cities, you need to fill the work zones again. Are you sure that you want to edit the cities?']).subscribe(value =>{
             this.translations = value;
             this.title = this.translations['WORKZONE'];
          });

          this.user = user;
          this.userWorkZones = user['work_zones'];
          let city = user['profile'].city;

          this.getProfessionalZones(city);
        })
      }

    }

    createLoader() {
      return this.loadingCtrl.create({ message: this.translations['LOADING'] } as LoadingOptions);
    }

    showErrorAlert(error) {
      this.alertCtrl.create({
        message: this.locationService.errorToString(error),
        buttons: [this.translations["OK"]]
      }).present();
    }

    getAllData() {
      let loader = this.createLoader();
      loader.present();
      let cities = [];
      let ids = this.citySelected.map(i => i.id);
      for(let id in ids){
       cities.push(this.locationService.getZones(ids[id]))
      }
      Observable.forkJoin(cities).subscribe(data => {
          this.zones = data;
          for(let zoneGroup of data){
            let group = zoneGroup as Array<any>;
            for(let zone of group){
              this.addZone(zone.id);
            }


          }
          loader.dismiss();
        }, error => {
          loader.dismiss();
          this.showErrorAlert(error);
        });

    }

    getProfessionalZones(cities = null, cityId = null){
      let loader = this.createLoader();
      loader.present();
      if(cities){
        let query = []
        let queryCities = []

        for(let city in cities){
          query.push(this.locationService.getZones(cities[city]))
          queryCities.push(this.locationService.getCityDetail(cities[city]))
        }

        Observable.forkJoin(query).subscribe(data =>{
          this.professionalZones = data;

          this.checkWorkZones();
          Observable.forkJoin(queryCities).subscribe(cities => {
            this.citySelectedByUser = cities

          }, error => {
            console.log(error);
          })
          loader.dismiss();
        },error =>{
          loader.dismiss();
          this.showErrorAlert(error);
        });
      }else{
        this.locationService.getAllZones().subscribe(data =>{
          this.professionalZones = data;
          this.checkWorkZones();
          loader.dismiss();
        });
      }

    }

    checkWorkZones(){
      for(let i = 0; i < this.userWorkZones.length;i++){
        this.professionalZones.forEach(element => {
          for(let j=0; j < element.length;j++){
            if(this.userWorkZones[i] == element[j].id){
              this.addZone(this.userWorkZones[i]);
            }
          }
        });
      }
    }

    addZone(zone) {
      if (!this.zoneIsSelected(zone)) {
        this.zonesAdded.push(zone);
      }
    }

    zoneIsSelected(zone){
      return this.zonesAdded.indexOf(zone) != -1;
    }

    deleteZone(zone){
       let zoneIndex = this.zonesAdded.findIndex(obj => obj == zone);
      if(zoneIndex >= 0){
        this.zonesAdded.splice(zoneIndex, 1)
      }
    }

    goToAccountPage(){
      this.signupService.setWorkZones(this.zonesAdded);
      this.navCtrl.push(AccountPage, {
        edit: false
      });
    }

    updateUserZones(editCity = false){
      let profile = [];
      //if the user is also editing the cities, is needed to update the profile with the city list
      if(editCity){
        //convert the city selected to an array of city ids
        let city = this.signupService.getCity();
        let cityList = city.map(item => item.id);
        profile = this.user['profile'];
        profile['city'] = cityList;
      }else{
        //city is not edited
        profile = this.user['profile'];
      }

      let data = {
        profile: profile,
        new_zones: this.zonesAdded
      }
      let loader = this.createLoader();
      loader.present();

      this.locationService.updateUserZones(data).subscribe(results => {
        loader.dismiss();
        let toast = this.toastCtrl.create({
          message: this.translations['Zones updated correctly'],
          duration: 3000,
          position: 'bottom'
        });
        toast.present();
        if(editCity){
          //if the city is edited, then the user is redirected to Appointments page
          this.app.getActiveNavs("menuRoot")[0].setRoot(AppointmentsPage);
        }

      }, error => {
        loader.dismiss();
        this.showErrorAlert(error);
      })
    }

    //Show an alert to confirm to go to update cities and go to update cities
    goToUpdateCities(){
      this.alertCtrl.create({
        message: this.translations['If you change the cities, you need to fill the work zones again. Are you sure that you want to edit the cities?'],
        buttons: [{
          text: this.translations["OK"],
          role: this.translations["OK"],
          handler: () => {
            this.navCtrl.push(WorkZonePage,{
              editMode: true
            })
          }
        },
        {
          text: this.translations['Cancel'],
          role: 'Cancel'
        }
      ]

      }).present();
    }

    //Update user work zones and cities
    updateUserCitiesAndZones(){
        this.updateUserZones(true);
    }

}
