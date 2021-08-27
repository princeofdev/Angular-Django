import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, ModalController,AlertController } from 'ionic-angular';
import { ConfirmAddressPage } from '../confirm-address/confirm-address';
import { HireService } from '../../providers/hire-service';
import { AppointmentDetailPage } from '../appointment-detail/appointment-detail';
import { TranslateService } from '@ngx-translate/core';
import { ServicesService } from '../../providers/services-service';


@IonicPage()
@Component({
  selector: 'page-maps',
  templateUrl: 'maps.html',
})
export class MapsPage {

 notPostalCode: boolean = false;
 public registerMode: boolean;
 translations = {};

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private hireService: HireService,
    private modalCtrl: ModalController,
    private alertCtrl: AlertController,
    translateService: TranslateService,
    private servicesService: ServicesService) {
    this.registerMode = false;
    this.hireService.getUser();
    this.getHireServicesWithoutReview();
    translateService.get(['OK']).subscribe(results =>{
      this.translations = results;
    });
  }

  locationChange(location){
    this.navCtrl.push(ConfirmAddressPage, location);
  }

  showErrorAlert(error) {
    this.alertCtrl.create({
      message: this.hireService.errorToString(error),
      buttons: [this.translations['OK']]
    }).present();
  }

  getHireServicesWithoutReview(){
    this.hireService.getHireServicesWithoutReview().subscribe(results =>{
      let services_list = results as Array<any>;

      if(services_list.length > 0){
        let modal = this.modalCtrl.create(AppointmentDetailPage, { appointmentId: services_list[0].id });
        modal.onDidDismiss(data => {
          this.getHireServicesWithoutReview();
        });
        modal.present();
      }
    }, error => {
        this.showErrorAlert(error);
    });
  }

  ionViewDidEnter(){
    this.hireService.cleanService();
    this.servicesService.cleanData();
  }

}
