import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, Events, Platform, App } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { AppointmentDetailPage } from '../../pages/appointment-detail/appointment-detail';
import { AppointmentService } from '../../providers/appointment-service';
import { PENDING,COMPLETED,CONFIRMED } from '../../app/constants';
import { LoadingController } from 'ionic-angular/components/loading/loading-controller';
import { TranslateService } from '@ngx-translate/core';
import { SessionService } from '../../providers/session-service';
import { Subscription } from 'rxjs/Subscription';
import { MapsPage } from '../maps/maps';

@IonicPage()
@Component({
  selector: 'page-appointments',
  templateUrl: 'appointments.html',
})

export class AppointmentsPage extends UIComponent {
  public activeItem: string = 'confirmed';
  private pendingList: any = [];
  private confirmedList: any = [];
  private completedList: any = [];
  private user: any;
  public counter = '10';
  public translations: any
  public title: string;
  private onResumeSubscription: Subscription;

  constructor(
    public app: App,
    public platform: Platform,
    public navCtrl: NavController,
    public navParams: NavParams,
    private appointmentService: AppointmentService,
    private loadingCtrl: LoadingController,
    private translateService: TranslateService,
    private sessionService: SessionService,
    private events: Events
  ) {
    super();

    this.translateService.get(['My appointments' ]).subscribe(values => {
      this.translations = values;
      this.title = values['My appointments'];
    });

    this.sessionService.getUser().then(
      data => this.setUser(data)
    );

    this.onResumeSubscription = platform.resume.subscribe(() => {
      this.checkAppointmentsToLoad();
    }); 

    this.events.subscribe("service.update", () => { this.loadAppointments("confirmed"); });
    this.events.subscribe("service.pending", () => {  this.loadAppointments("pending"); });
  }

  checkAppointmentsToLoad() {
    if (this.navParams.get('activeItem') === 'pending'){
      this.loadAppointments('pending');
    }else{
      this.loadAppointments(this.activeItem);
    }
  }

  ionViewDidEnter(){
    this.checkAppointmentsToLoad();
  }

  ngOnDestroy() {
    this.onResumeSubscription.unsubscribe();
  }

  loadAppointments(activeItem){
    let loader = this.loadingCtrl.create();
    loader.present();
    this.appointmentService.getFinalUserList().subscribe(results => {
      this.pendingList = [];
      this.confirmedList = [];
      this.completedList = [];
      for (let i in results) {
        if (results[i].status === PENDING) {
          this.pendingList.push(results[i]);
        } else if (results[i].status === CONFIRMED) {
          this.confirmedList.push(results[i]);
        } else if (results[i].status === COMPLETED) {
          this.completedList.push(results[i]);
        }
      }
      this.setActiveItem(activeItem);
      loader.dismiss();
    });
  }

  goToDetail(event) {
    this.navCtrl.push(AppointmentDetailPage, {
      appointmentId: event.id
    });
  }

  goToHome() {
    this.app.getActiveNavs("menuRoot")[0].setRoot(MapsPage);
  }

  changeTab(item) {
    this.loadAppointments(item);
  }

  setActiveItem(item){
    this.activeItem = item;
    if((item === 'confirmed' && this.confirmedList.length === 0)
      || (item === 'completed' && this.completedList.length === 0)
      || (item === 'pending' && this.pendingList.length === 0)){
      this.setUIBlank();
    }else{
      this.setUIIdeal();
    }
  }

  setUser(user){
    this.user = user;
  }






}
