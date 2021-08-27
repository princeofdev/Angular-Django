import { Component, ViewChild } from '@angular/core';
import { IonicPage, NavController, NavParams, LoadingController, AlertController } from 'ionic-angular';
import { ServicesService } from '../../providers/services-service';
import { ServiceBasketPage } from '../service-basket/service-basket';

import { Slides } from 'ionic-angular';
import { OnInit } from '@angular/core/src/metadata/lifecycle_hooks';
import { TranslateService } from '@ngx-translate/core';
import { UIComponent } from '../../classes/component';


@IonicPage()
@Component({
  selector: 'page-user-services',
  templateUrl: 'user-services.html',
})
export class UserServicesPage extends UIComponent implements OnInit {

  @ViewChild(Slides) slides: Slides;
  private categoryId: any = null;
  private postal_code: any = null;
  private servicesList = null;
  private activeIndex = null;
  public translations: any        
  public title: string;
  public registerMode: boolean = false;


  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private translateService: TranslateService,
    private servicesService: ServicesService,
    private loadingCtrl: LoadingController,
    private alertCtrl: AlertController) {
      super();
      this.translateService.get(['SERVICES', 'OK']).subscribe(values => {
        this.translations = values;
      });
      this.registerMode = true;
  }

  ngOnInit(){
    this.categoryId = this.navParams.get('categoryId');
    this.postal_code = this.navParams.get('postal_code');
    this.title = this.navParams.get('title');

    if(typeof(this.categoryId) !== 'undefined' && typeof(this.postal_code) !=='undefined'){
      this.getServicesByCategoryAndZip(this.categoryId,this.postal_code);
    }

  }

  ngAfterViewInit() {
    setTimeout(() => {
      this.activeIndex = this.slides._activeIndex;
    }, 100);

  }

  getServicesByCategoryAndZip(category,postal_code){
    let loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
    loader.present();
    this.servicesService.getServicesByCategoryAndZip(category,postal_code).subscribe(results =>{
      loader.dismiss();
      this.servicesList = results;
      if(this.servicesList.length === 0){
        this.setUIBlank();
      }else{
        this.setUIIdeal();
      }
    }, error => {
      loader.dismiss();
      this.showErrorAlert(error);
    });
  }

  goToBasket(){
    this.servicesService.addItemToBasket(this.servicesList[this.activeIndex]);
    this.navCtrl.push(ServiceBasketPage);
  }

  slideChanged() {
    let currentIndex = this.slides.getActiveIndex();
    this.activeIndex = currentIndex;
  }


  showErrorAlert(error) {
    this.alertCtrl.create({
      message: this.servicesService.errorToString(error),
      buttons: [this.translations["OK"]]
    }).present();
  }

}
