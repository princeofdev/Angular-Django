import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, ModalController, LoadingController, AlertController} from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { PaymentMethodPage } from '../payment-method/payment-method';
import { FinishOrderPage } from '../finish-order/finish-order';
import { HireService } from '../../providers/hire-service';
import { OnInit } from '@angular/core/src/metadata/lifecycle_hooks';
import { TranslateService } from '@ngx-translate/core';
import { SignupService } from '../../providers/signup-service';
import { ServicesService } from '../../providers/services-service';

@IonicPage()
@Component({
  selector: 'page-resume',
  templateUrl: 'resume-page.html',
})
export class ResumePage extends UIComponent implements OnInit {
  public type;

  private card = null;
  private date: any = null;
  private services: string = "";
  private address: string = "";
  private comment: string = "";
  private price: number = 0;
  private currency: string = "";
  public title: string;
  public translations: any;
  public registerMode: boolean = false;
  public coupon_code: any = null;
  public couponValid: any = null;
  private coupon: any = null;
  private special_price: number = 0;

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private hireService: HireService,
    private modalCtrl: ModalController,
    private loadingCtrl: LoadingController,
    private translate: TranslateService,
    private signupService: SignupService,
    private alertCtrl: AlertController,
    private servicesService: ServicesService

  ) {
    super();
    this.type = navParams.get('type');
    this.type = 'resume';
    this.card = navParams.get('card');
    this.translate.get(['Resume',"Credit card is mandatory", "OK"]).subscribe(values => {
      this.translations = values;
      this.title = values['Resume'];
    });
    this.registerMode = true;
  }

  ngOnInit(){
    this.date = this.hireService.getFullDate();
    this.price = this.hireService.getTotalPrice();
    this.currency = this.hireService.getCurrency();
    this.services = this.hireService.getListOfServices();
    this.address = this.hireService.getFullAddress();
  }

  goToPaymentsPage(){
    let modal = this.modalCtrl.create(PaymentMethodPage, {selectCardMode: true});
    modal.onDidDismiss(data => {
      this.card = data.card;
    });
    modal.present();
  }

  goToFinishOrder(){
    if(this.card){
      if(this.couponValid){
          this.hireService.setSpecialPrice(this.special_price);
      }else{
        this.hireService.setSpecialPrice(this.price);
      }
      this.hireService.setCard(this.card);
      this.hireService.setComment(this.comment);
      let loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
      loader.present();
      if(this.coupon && this.couponValid){
        this.hireService.setCouponCode(this.coupon_code);
      }
      this.hireService.sendData().subscribe(results =>{
        loader.dismiss();
        this.hireService.cleanService();
        this.servicesService.cleanData();
        this.navCtrl.push(FinishOrderPage);

      }, error => {
        loader.dismiss();
        this.showErrorAlert(error);
      });
    }else{
      this.alertCtrl.create({
        message: this.translations['Credit card is mandatory'],
        buttons: [this.translations['OK']]
      }).present();
    }
  }

  checkCoupon() {

    if (this.coupon_code && this.coupon_code !== '') {
      let loader = this.loadingCtrl.create();
      loader.present();
      this.hireService.checkCoupon(this.coupon_code).subscribe(results => {
        loader.dismiss();
        this.couponValid = true;
        this.coupon = results;
        this.setSpecialPrice(results);

      }, error => {
        loader.dismiss();
        this.couponValid = false;
        this.coupon = null;
        this.showErrorAlert(error);
      });
    }else{
      this.couponValid = null;
      this.coupon = null;
    }
  }

  setSpecialPrice(coupon){

    let amount_off = coupon.amount_off;

    let type = coupon.type;

    let special_price = 0;
    if(type === 'MON'){
      special_price = this.price - parseInt(amount_off);
    }else{
      let discount = (this.price * parseInt(amount_off)) / 100;
      special_price = this.price - discount;
    }
    this.special_price = special_price;
  }


  showErrorAlert(error) {
    this.alertCtrl.create({
      message: this.signupService.errorToString(error),
      buttons: [this.translations['OK']]
    }).present();
  }

  cuponStyle() {
    let styles = {
      'coupon-valid': this.couponValid,
      'coupon-invalid': this.couponValid == false
    }
    return styles;
  }






}
