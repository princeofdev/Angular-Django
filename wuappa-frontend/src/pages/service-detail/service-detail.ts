import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { ServicesService } from '../../providers/services-service';
import { ServiceBasketPage } from '../service-basket/service-basket';

/**
 * Generated class for the ServiceDetailPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-service-detail',
  templateUrl: 'service-detail.html',
})
export class ServiceDetailPage {
  public service = [];
  public relatedServices = [];
  public itemRelated = undefined;

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    public servicesService: ServicesService
  ) {
    if(this.navParams.get("service")){
      this.service = this.navParams.get("service");
    }
    if(this.navParams.get("relatedServices")){
      this.relatedServices = this.navParams.get("relatedServices");

    }
  }

  public goToServiceDetail(service){
    let relatedServices = this.relatedServices.filter((serviceFromList) => { return serviceFromList.id != service.id });
    this.navCtrl.push(ServiceDetailPage, { service, relatedServices });
  }

  public goToBasket(){
    this.servicesService.addItemToBasket(this.service);
    this.navCtrl.push(ServiceBasketPage);
  }

}
