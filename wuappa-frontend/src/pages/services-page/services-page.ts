import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { AlertController } from 'ionic-angular/components/alert/alert-controller';
import { LoadingController } from 'ionic-angular/components/loading/loading-controller';
import { TranslateService } from '@ngx-translate/core';

import { UIComponent } from '../../classes/component';
import { ServicesService } from '../../providers/services-service';
import { SignupService } from '../../providers/signup-service';
import { UserService } from '../../providers/user-service';
import { WorkDaysPage } from '../work-days/work-days';
import { Observable } from 'rxjs';

@IonicPage()
@Component({
    selector: 'page-services-page',
    templateUrl: 'services-page.html',
})
export class ServicesPage extends UIComponent {
    user: any;
    userServices: any = [];
    translations = {};
    services = [];
    selectedServices = [];
    postal_code: any = '';
    professionalServices: any = [];
    workZoneServices: any = [];
    public title: any;
    public registerMode: any;
    constructor(
        public navCtrl: NavController,
        public navParams: NavParams,
        public alertCtrl: AlertController,
        public loadingCtrl: LoadingController,
        public servicesService: ServicesService,
        public signupService: SignupService,
        public translate: TranslateService,
        private userService: UserService,
    ) {
        super();
        console.log('aqui estoy loco');

        this.translate.get(["SERVICES"]).subscribe(result => {
          this.title = result['SERVICES'];
        });
        let registerMode = this.navParams.get('register_mode');
        if(typeof registerMode !== 'undefined'){
          this.registerMode = true;
          this.translate.get(["Loading", "OK", "Your request has been sended"]).subscribe(result => {
          this.getServices();
          });
        }else{
          this.registerMode = false;
          this.userService.getUser().subscribe(user =>{
            this.user = user;
            this.translate.get(["Loading", "OK","Your request has been sended"]).subscribe(result => {
              this.translations = result;
                if (user['profile'].type == 'PRO'){
                  this.userServices = user['services'];
                  this.getServicesByWorkZone(user['services'],user['work_zones']);
                }else{
                  this.getServices();
                }

            });
          });
        }
    }

    isServiceSelected(service) {
      return this.selectedServices.indexOf(service.id) >= 0;
    }

    switchService(service) {
      if (this.isServiceSelected(service)) {
        this.selectedServices = this.selectedServices.filter(item => item != service.id);
      } else {
        this.selectedServices.push(service.id);
      }
    }

    serviceStyle(service) {
      if (this.isServiceSelected(service)) {
        return {"clicked": true};
      } else {
        return {};
      }
    }

    getServices() {
      const loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
      loader.present();
      console.log('city selected',this.signupService.citySelected);
      let citiesQuery = [];
      for(let i=0;i<this.signupService.citySelected.length;i++){
        citiesQuery.push(this.servicesService.getServicesByCity(this.signupService.citySelected[i].id));
      }
      console.log('cities query',citiesQuery);

      Observable.forkJoin(citiesQuery).subscribe(services => {
        console.log('services',services);

        loader.dismiss();
        services.forEach(item => {
          // console.log('city',city);
          let city = item as Array<any>;
          for(let service of city){
            this.services.push(service);
          }
        })
        // this.services = services as Array<any>;
        console.log('services after',this.services);

      }, error => {
        loader.dismiss();
        this.alertCtrl.create({
          message: this.servicesService.errorToString(error.errors),
          buttons: [this.translations["OK"]]
        }).present();
      });
    }

    getServicesByZip(postal_code){
      const loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
      loader.present();
      this.servicesService.getServicesByZip(postal_code).subscribe(services => {
        loader.dismiss();
        this.services = services as Array<any>;
        },error => {
          loader.dismiss();
          this.alertCtrl.create({
            message: this.servicesService.errorToString(error.errors),
            buttons: [this.translations["OK"]]
          }).present();
        }
      )
    }

    register() {
      this.signupService.setServices(this.selectedServices);
      this.navCtrl.push(WorkDaysPage, {
        editMode: false
      });
    }


    getServicesByWorkZone(services,work_zones){
      let loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
      loader.present();

        this.servicesService.getServicesByWorkZones(work_zones).subscribe(results => {
          this.workZoneServices = results;
          this.checkProfessionalServices(services);
          loader.dismiss();
      }, error =>{
         this.showErrorAlert(error);
      });


    }
    checkProfessionalServices(userServices){

      for(let i=0; i< userServices.length;i++){
        for(let j=0; j< this.workZoneServices.length;j++){

          if(userServices[i] == this.workZoneServices[j].id){
              this.selectedServices.push(userServices[i]);
              break;
          }
        }
      }

    }

    updateProfessionalServices(){
      if(this.user){
        let loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
        loader.present();
        let data = {
          profile: this.user['profile'],
          new_services: this.selectedServices
        }

        this.servicesService.updateProfessionalServices(data).subscribe(results =>{
          loader.dismiss();
            this.alertCtrl.create({
              subTitle: this.translations['Your request has been sended'],
              buttons: [this.translations['OK']]
            }).present();
        },error =>{
          loader.dismiss();
            this.showErrorAlert(error);
        })
      }
    }

  showErrorAlert(error) {
    this.alertCtrl.create({
      subTitle: this.servicesService.errorToString(error),
      buttons: [this.translations['OK']]
    }).present();
  }


}
