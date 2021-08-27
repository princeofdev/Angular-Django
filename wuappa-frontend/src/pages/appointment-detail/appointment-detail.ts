import { Component,  } from '@angular/core';
import { IonicPage, NavController, NavParams, App, AlertController, ToastController, LoadingController, ModalController } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { HomePage } from '../../pages/home/home';
import * as moment from 'moment';

import { AppointmentService } from '../../providers/appointment-service';
import { SignupService } from '../../providers/signup-service';
import { TranslateService } from '@ngx-translate/core';
import { SessionService } from '../../providers/session-service';
import { PaymentMethodPage } from '../payment-method/payment-method';

@IonicPage()
@Component({
  selector: 'page-appointment-detail',
  templateUrl: 'appointment-detail.html',
})
export class AppointmentDetailPage extends UIComponent{
  public item: any;
  private userId: any;
  private userType: any;
  public activeItem: string;
  public hour: any;
  public punctuation: number;
  public canceled = false;
  public translations: any
  public fullAddress: string = '';
  public formattedDate: string = '';
  private canceledMessage: string = '';
  private alertCancelMessage: string  = '';
  private alertCancelMessage50: string  = '';
  private alertCancelMessage100: string  = '';
  private alertCancelMessageCharged: string  = '';
  private cancelQuestion: string = '';

  public title: string;
  private price: any = '';
  private appointment_id: any;
  private card: any = null;
  public hasReview: boolean = null;
  private professional_avatar: any = null;
  private rating: number = 0;
  private review_comment: any = '';

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private app: App,
    private appointmentService: AppointmentService,
    private signupService: SignupService,
    private alertCtrl: AlertController,
    private toastCtrl: ToastController,
    private translateService: TranslateService,
    private sessionService: SessionService,
    private loadingCtrl: LoadingController,
    private modalCtrl: ModalController
  ) {
    super();
    this.appointment_id = navParams.get('appointmentId');

    this.translateService.get([
      'Loading',
      'Appointment cancelled succesfully',
      'Are you sure that you want to cancel',
      'APPOINTMENT', "If you cancel this service you will be charged",
      "If you cancel this service you will be charged 100% of the total cost",
      "Are you sure that you want to cancel?",
      'Yes',
      'No',
      'Confirm cancel',
      'OK',
      'Cancel',
      "No",
      "Yes",
      "You have refused the service",
      "Your review has been sent",
      "Confirm refuse",
      "Are you sure you want to refuse this service?",
      "The service has been completed",
      "Notification sent",
      "Yes, delete it"
    ]).subscribe(values => {
      this.translations = values;
      this.title = values['APPOINTMENT'];
      this.canceledMessage = values['Appointment cancelled succesfully'];
      this.alertCancelMessage = values['Are you sure that you want to cancel'];
      this.alertCancelMessageCharged = values['If you cancel this service you will be charged'];
      this.alertCancelMessage100 = values['If you cancel this service you will be charged 100% of the total cost'];
      this.cancelQuestion = values["Are you sure that you want to cancel?"];
    });
    let loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
    loader.present();

    this.appointmentService.getAppointmentDetail(this.appointment_id).subscribe(value =>{

      this.item = value;
      console.log('item',this.item);

      this.sessionService.getUser().then(results => {
        if (typeof this.item !== 'undefined') {
          this.userType = results['type'];
          this.userId = results['user_id'];
          this.activeItem = this.item.status;
          this.fullAddress = this.getFullAddress();
          this.formattedDate = this.getFormattedDate();
          this.price = this.getFormattedPrice();
          this.hasReview = (this.item.review) ? true : false;
          if (this.item.professional && this.item.professional.profile && this.item.professional.profile.picture){
            this.professional_avatar = this.item.professional.profile.picture;
          }
          this.checkDateTime();
          this.setUIIdeal();
          loader.dismiss();
        }
      })

    },error =>{
      this.showErrorAlert(error);
    })
  }

  public goHome(){
    this.app.getActiveNavs("menuRoot")[0].setRoot(HomePage);
  }

  checkData(data){
    if(data){
      for(let i in data){
        if(typeof data[i] === 'undefined'){
          data[i] = '';
        }
      }

    } else {
      data = {};
    }
    return data;
  }

  getFullAddress(){
    return this.item.address + ", " + this.item.zip_code + ", " + this.item.city + ", " + this.item.region + ", " + this.item.country;
  }

  getFormattedDate(){
    let date = moment(this.item.date).format("DD/MM/YYYY");
    let hour = moment(this.item.time,"hh:mm:ss").format('HH:mm');
    return date + " " + hour;
  }

  getFormattedPrice(){
    let price = this.item.total;
    let currency = this.item.total_currency;
    return price + " " + currency;
  }

  showToast(message) {
    this.toastCtrl.create({
      message: message,
      duration: 3000,
      position: 'bottom'
    }).present();
  }

  showCancelAlert(cost = false,data = null){
    if(this.userType === 'FIN'){
      if (!cost) {
        this.alertCtrl.create({
          title: this.translations['Confirm Cancel'],
          message: this.alertCancelMessage,
          buttons: [
            {
              text: this.translations['Yes'],
              role: 'OK',
              handler: () => {
                this.cancelAppointment();
              }
            },
            {
              text: this.translations['No'],
              role: 'Cancel',
              handler: () => {}
            }
          ]
        }).present();
      }else{
        this.showAlertWithCost(data);
      }

    }else{
      this.alertCtrl.create({
        title: this.translations['Confirm Cancel'],
        message: this.alertCancelMessage,
        buttons: [
          {
            text: this.translations['Yes'],
            role: 'OK',
            handler: () => {
              this.cancelAppointment();
            }
          },
          {
            text: this.translations['No'],
            role: 'Cancel',
            handler: () => {}
          }
        ]
      }).present();
    }
  }

  showAlertWithCost(data){
    let alertMessage = `${this.alertCancelMessageCharged} ${data['amount']} ${data['currency']}. ${this.cancelQuestion}`;
    this.alertCtrl.create({
      title: this.translations['Confirm Cancel'],
      message: alertMessage,
      buttons: [
        {
          text: this.translations['Yes'],
          role: 'OK',
          handler: () => {
            this.cancelAppointment();
          }
        },
        {
          text: this.translations['No'],
          role: 'Cancel',
          handler:() =>{}
        }
      ]
    }).present();
  }

  alertFiftyPerfect(){

    this.alertCtrl.create({
      title: this.translations['Confirm Cancel'],
      message: this.alertCancelMessage50,
      buttons: [
        {
          text: this.translations['Yes'],
          role: 'OK',
          handler: () => {
            this.cancelAppointment();
          }
        },
        {
          text: this.translations['No'],
          role: 'Cancel',
          handler: () => {}
        }
      ]
    }).present();
  }
  alertHundredPerfect(){
    this.alertCtrl.create({
      title: this.translations['Confirm Cancel'],
      message: this.alertCancelMessage100,
      buttons: [
        {
          text: this.translations['Yes'],
          role: 'OK',
          handler: () => {
            this.cancelAppointment();
          }
        },
        {
          text: this.translations['No'],
          role: 'Cancel',
          handler: () => {}
        }
      ]
    }).present();
  }

  cancelAppointment(){
    this.appointmentService.cancelAppointment(this.item.id).subscribe(results =>{
       this.toastCtrl.create({
        message: this.canceledMessage,
        duration: 3000,
        position: 'bottom'
      }).present();
      this.navCtrl.pop();

    }, error => {
        this.showErrorAlert(error);
    })
  }

  showErrorAlert(error) {
    this.alertCtrl.create({
      message: this.signupService.errorToString(error),
      buttons: [this.translations['OK']]
    }).present();
  }

  acceptService(){
    if(this.userType === 'PRO'){
      let loader = this.loadingCtrl.create();
      loader.present();
      this.appointmentService.acceptAppointment(this.item.id).subscribe(results =>{
        loader.dismiss();
        this.showToast(this.translations["You have accepted the service"]);
        this.navCtrl.pop();
      },error => {
        loader.dismiss();
        this.showErrorAlert(error);
      });
    }
  }

  refuseService(){
    if(this.userType === 'PRO'){
      this.alertCtrl.create({
        title: this.translations['Confirm refuse'],
        message: this.translations['Are you sure you want to refuse this service?'],
        buttons: [{
          text: this.translations['Yes'],
          role: 'OK',
          handler: () => {
            let loader = this.loadingCtrl.create();
            loader.present();
            this.appointmentService.refuseAppointment(this.item.id).subscribe(results =>{
              loader.dismiss();
              this.showToast(this.translations["You have refused the service"]);
              this.navCtrl.pop();
            }, error => {
              loader.dismiss();
              this.showErrorAlert(error);
            });
          }
        }, {
          text: this.translations['No'],
          role: 'Cancel'
        }]
      }).present();
    }
  }

  checkDateTime(){
    let appointmentDate = moment(this.item.date+ " "+ this.item.time).format();
    let dateAfterNow = moment().isAfter(appointmentDate);
    return dateAfterNow;

  }

  goToPaymentsPage() {
    let modal = this.modalCtrl.create(PaymentMethodPage, { selectCardMode: true });
    modal.onDidDismiss(data => {
      this.card = data.card;
      let loader = this.loadingCtrl.create();
      loader.present();
      if(this.card){
        this.appointmentService.updateCreditCard(this.card.stripe_id,this.item.id).subscribe(results =>{
          let message = this.translations['Updated credit card correctly'];
          loader.dismiss();
          this.showToast(message);
        },error =>{
          loader.dismiss();
          this.showErrorAlert(error);
        });
      }else{
        loader.dismiss();
      }
    });
    modal.present();
  }

  sendReview(){
    let loader = this.loadingCtrl.create();
    loader.present();
    let data = {
      id: this.item.id,
      rating: this.rating,
      review: this.review_comment
    }
    this.appointmentService.sendReview(data).subscribe(results =>{
      loader.dismiss();
      this.showToast(this.translations["Your review has been sent"]);
      this.navCtrl.pop();
    }, error => {
      loader.dismiss();
      this.showErrorAlert(error);
    })
  }

  updateRatingStars(event) {
    this.rating = event;
  }



  finishService() {
    let loader = this.loadingCtrl.create();
    loader.present();
    this.appointmentService.completeAppointment(this.item.id).subscribe(results =>{
      loader.dismiss();
      this.showToast(this.translations["The service has been completed"]);
      this.navCtrl.pop();
    },error =>{
      loader.dismiss();
      this.showErrorAlert(error);
    });
  }

  notifyCustomer(){
    let loader = this.loadingCtrl.create();
    loader.present();
    this.appointmentService.notifyCustomer(this.item.id).subscribe(results =>{
      loader.dismiss();
      this.showToast(this.translations["Notification sent"]);
    },error =>{
      loader.dismiss();8
      this.showErrorAlert(error);
    });
  }

  checkCancelability(){
    this.appointmentService.checkAppointmentCancelability(this.appointment_id).subscribe(results =>{
      this.showCancelAlert();

    }, error =>{
      this.showCancelAlert(true,error);

    });
  }

}
