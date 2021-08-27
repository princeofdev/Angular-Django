import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, LoadingController,AlertController } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { CalendarComponentOptions } from "ion2-calendar";
import { HireService } from '../../providers/hire-service';
import { ResumePage } from '../resume-page/resume-page';
import { TranslateService } from '@ngx-translate/core';
import * as moment from 'moment';


/**
 * Generated class for the UserCalendarPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-user-calendar',
  templateUrl: 'user-calendar.html',
})
export class UserCalendarPage extends UIComponent {

  selectedHours = [];

  options: CalendarComponentOptions = null;

  layout: string = 'calendar';

  public date: any = null;

  public hour: any = null;

  public dateAvailable: boolean = false;

  public today:any = moment()
  public currentHour:any = moment().format('HH:mm')
  public timeOut:any = '21:00'
  public currentDay:any;

  format: string = 'YYYY-MM-DD';
  public translations: any;
  public title: string;
  public registerMode: boolean = false;
  public timePickerTitle: any;
  public hourValues = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];
  public minuteValues = [0, 15, 30, 45];

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    private hireService: HireService,
    private translateService: TranslateService,
    private loadingCtrl: LoadingController,
    private alertCtrl: AlertController) {
    super();
    this.setUIIdeal();
    if(this.today){
      let date = new Date()
      if(this.currentHour > this.timeOut){
        this.currentDay = date.setDate(date.getDate() + 1)
      }else{
        this.currentDay = date
      }
    }else{
      this.currentDay = new Date()
    }
    this.translateService.get(['forbidden hour to hire', 'Calendar', 'Loading', 'SELECTADATE', 'Hour complete', 'Select an hour', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRY', 'SAT','JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'OK']).subscribe(values => {
      this.translations = values;
      this.title = values['SELECTADATE'];
      this.timePickerTitle = values['Select an hour'];
      this.options = {
        pickMode: 'single',
        weekStart: 1,
        weekdays: [
          this.translations['SUN'],
          this.translations['MON'],
          this.translations['TUE'],
          this.translations['WED'],
          this.translations['THU'],
          this.translations['FRY'],
          this.translations['SAT']
        ],
        monthPickerFormat: [
          this.translations['JAN'],
          this.translations['FEB'],
          this.translations['MAR'],
          this.translations['APR'],
          this.translations['MAY'],
          this.translations['JUN'],
          this.translations['JUL'],
          this.translations['AUG'],
          this.translations['SEP'],
          this.translations['OCT'],
          this.translations['NOV'],
          this.translations['DEC'],
        ],
        from: this.currentDay
      }
    });
    this.registerMode = true;
  }

  onChange(event){
    this.date = event;
    if(this.hour && this.date){
      this.checkAvailability(this.hour)
    }

  }

  saveDateAndHour(){
    this.hireService.setDate(this.date);
    this.hireService.setHour(this.hour);
  }



  checkAvailability(event){
    let loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
    loader.present();
    if(this.hour && this.date){
      let data = {
        date: this.date,
        time: this.hour
      };
        if(data.time != '20:15' && data.time != '20:30' && data.time != '20:45'){
          this.hireService.checkAvailability(data).subscribe(results =>{
              let pro_list = results as Array<any>;
              loader.dismiss();
              if (pro_list.length === 0) {
                this.dateAvailable = false;
                this.alertCtrl.create({
                  message: this.translations['Hour complete'],
                  buttons: [this.translations["OK"]]
                }).present();
              }else{
                this.dateAvailable = true;
                this.setUIIdeal();
              }
          }, error =>{
                loader.dismiss();
                this.dateAvailable = false;
                this.showErrorAlert(error);
          });
        } else {
          this.dateAvailable = false;
          this.hour = '20:00';
          loader.dismiss();
          this.alertCtrl.create({
            message: this.translations['forbidden hour to hire'],
            buttons: [this.translations["OK"]]
          }).present();
        }
    }
  }

  goToResume(){
    this.saveDateAndHour();
    this.navCtrl.push(ResumePage);
  }


  showErrorAlert(error) {
    this.alertCtrl.create({
      message: this.hireService.errorToString(error),
      buttons: [this.translations["OK"]]
    }).present();
  }



}
