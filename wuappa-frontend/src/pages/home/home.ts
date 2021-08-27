import { Component } from '@angular/core';
import { UIComponent } from '../../classes/component';
import { IonicPage, NavController, NavParams, LoadingController, AlertController} from 'ionic-angular';
import { ServicesService } from '../../providers/services-service';
import { HireService } from '../../providers/hire-service';
import { TranslateService } from '@ngx-translate/core';
import { ServiceDetailPage } from '../service-detail/service-detail'

@IonicPage()
@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage extends UIComponent {
  public postal_code: string;
  public categories: any = [];
  public title: any;
  private translations: any = [];
  public registerMode: boolean = false;
  public itemActive:any = undefined;
  public selectedCategory = {};

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    public servicesService: ServicesService,
    public hireService: HireService,
    public translateService: TranslateService,
    private loadingCtrl: LoadingController,
    private alertCtrl: AlertController
  ) {
    super();
    this.postal_code = this.navParams.get('postal_code');
    this.translateService.get(['Loading','Categories','OK']).subscribe(results =>{
      this.translations = results;
      this.title = results['Categories'];
    });
    this.registerMode = true;
    this.setParams();

    if(this.postal_code || false){
      this.getCategories(this.postal_code);
    }
  }


  setParams(){
    this.hireService.setAddress(this.navParams.get('address'));
    this.hireService.setPostalCode(this.navParams.get('postal_code'));
    this.hireService.setCity(this.navParams.get('city'));
    this.hireService.setCountry(this.navParams.get('country'));
    this.hireService.setState(this.navParams.get('state'));
    this.hireService.setAddressDetails(this.navParams.get('address_details'));
  }

  getCategories(postal_code) {
    let loader = this.loadingCtrl.create({content: this.translations['Loading']});
    loader.present();
    this.servicesService.getCategoriesByZip(postal_code).subscribe(data => {
      this.categories = data;
      if(this.categories.length !== 0 ){
        this.setUIIdeal();
        loader.dismiss();
      }else{
        this.setUIBlank();
        loader.dismiss();
      }
    }, error => {
      this.setUIError();
      loader.dismiss();
    }
    )
  }

  public getServicesByCategoryAndZip(category, postal_code){
    let loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
    loader.present();
    this.servicesService.getServicesByCategoryAndZip(category.id,postal_code).subscribe(results =>{
      loader.dismiss();
      category.services = results;
      this.selectedCategory = category;
    }, error => {
      loader.dismiss();
      this.showErrorAlert(error);
    });
  }

  showErrorAlert(error) {
    this.alertCtrl.create({
      message: this.servicesService.errorToString(error),
      buttons: [this.translations['OK']]
    }).present();
  }

  public goToServiceDetail(service, relatedServices){
    relatedServices = relatedServices.filter((serviceFromList) => { return serviceFromList.id != service.id });
    this.navCtrl.push(ServiceDetailPage, { service, relatedServices });
  }


}
