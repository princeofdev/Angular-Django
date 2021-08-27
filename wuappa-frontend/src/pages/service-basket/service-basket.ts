import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { ServicesService } from '../../providers/services-service';
import { UIComponent } from '../../classes/component';
import { UserCalendarPage } from '../user-calendar/user-calendar';
import { HireService } from '../../providers/hire-service';
import { TranslateService } from '@ngx-translate/core';
import { HomePage } from '../home/home';

@IonicPage()
@Component({
  selector: 'page-service-basket',
  templateUrl: 'service-basket.html',
})
export class ServiceBasketPage extends UIComponent {

  private basketList: any;
  public translations: any        
  public title: string;
  public registerMode: boolean = false;


  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private servicesService: ServicesService,
    private hireService: HireService,
    private translateService: TranslateService) {
    super();
    this.listBasket();
    this.setUIIdeal();
    
    this.translateService.get(['SERVICES' ]).subscribe(values => {
      this.translations = values;
      this.title = values['SERVICES'];
    });
    this.registerMode = true;
  }

  listBasket(){
    this.basketList = this.servicesService.getBasketList();
  }

  incrementService(id){
    this.servicesService.incrementService(id);
  }

  decrementService(id){
    this.servicesService.decrementService(id);
    this.setUIState();
  }

  addOtherServices(){
    this.navCtrl.pop();
    this.navCtrl.popTo(HomePage);

  }

  addBasketToResume(){
    let basket = this.servicesService.getBasketList();
    this.hireService.setBasket(basket);
  }

  goToUserCalendar(){
    this.addBasketToResume();
    this.navCtrl.push(UserCalendarPage);
  }

  setUIState(){
    if (this.servicesService.isBasketEmpty()) {
      this.setUIBlank();
    } else {
      this.setUIIdeal();
    }
  }

}
