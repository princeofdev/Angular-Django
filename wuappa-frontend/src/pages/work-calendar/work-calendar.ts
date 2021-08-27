import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, ToastController, AlertController,LoadingController } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { CalendarComponentOptions } from "ion2-calendar";
import { CalendarService } from '../../providers/calendar-service';
import * as moment from 'moment';
import { TranslateService } from '@ngx-translate/core';

@IonicPage()
@Component({
    selector: 'page-work-calendar',
    templateUrl: 'work-calendar.html',
})
export class WorkCalendarPage extends UIComponent {

    translations = {};
    selectedHours = [];


    layout: string = 'calendar'
    public date: any = [];
    public month: any = moment().month('MMM');
    toastMsg: any = '';
    public type: any;
    public title: any;
    options: CalendarComponentOptions = {
        pickMode: 'multi',
        weekStart: 1,
        weekdays: ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'],
        from: new Date()
    }

    constructor(
        public navCtrl: NavController,
        public navParams: NavParams,
        private calendarService: CalendarService,
        private toastCtrl: ToastController,
        private translateService: TranslateService,
        private alertCtrl: AlertController,
        private loadingCtrl: LoadingController) {
        super();
        this.month = moment().month('MMM');
        this.translateService.get(['Day added correctly', 'Loading', 'Day deleted correctly', 'HOLYDAYS', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRY', 'SAT',
                                    'JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC', 'OK']).subscribe(value =>{
            this.translations = value;
            this.title = value['HOLYDAYS'];
            this.options = {
                pickMode: 'multi',
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
                from: new Date(),
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
                monthFormat: "MMM YY"
            }

        });

    }

    ngOnInit(){
       this.calendarService.getUser().then(results =>{
           this.getDays();
       }).catch(error => {
            console.log('error usuario',error);
       })
    }
    onChange($event) {

        if($event.length < this.date.length){
            let dayToDelete = '';

            for (var i = 0; i < this.date.length; i++) {
                var found = false;
                for (var j = 0; j < $event.length; j++) { // j < is missed;
                    if (this.date[i]._i == $event[j]._i) {
                        found = true;
                        break;
                    }
                }
                if (found == false) {
                    dayToDelete = this.date[i];
                }

            }
            this.deleteDay(dayToDelete);
        }else{
           let dayToAdd =  $event[$event.length-1];
            this.saveDay(dayToAdd);
        }
        this.date = $event;
    }

    showToast(message){
        let toast = this.toastCtrl.create({
            message: message,
            duration: 1000,
            position: 'bottom'
        });
        toast.present();
    }

    saveDay(date){
        let loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
        loader.present();
        let formatted_date = moment(date._i).format('YYYY-MM-DD');
        this.calendarService.addDayOff(formatted_date).subscribe(results => {
            loader.dismiss();
            this.showToast(this.translations['Day added correctly']);
        }, error => {
            this.showErrorAlert(error);
        });
    }

    deleteDay(date){
        let loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
        loader.present();
        let formatted_date = moment(date._i).format('YYYY-MM-DD');
        this.calendarService.deleteDayOff(formatted_date).subscribe(results => {
            loader.dismiss();
            this.showToast(this.translations['Day deleted correctly']);
        }, error => {
            loader.dismiss();
            this.showErrorAlert(error);
        })
    }



    getDays(){
        let professionalDates = [];
        let loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
        loader.present();
        this.calendarService.getDaysOff().subscribe(results =>{
            for(let i in results){
                let momentObj = moment(results[i].date);
                //posible fix
                let yesterday = moment().subtract(1,'days');
                if(moment(momentObj).isSameOrAfter(yesterday)){
                    professionalDates.push(momentObj);
                }
            }
            this.date = professionalDates;
            loader.dismiss();

        }, error => {
            loader.dismiss();
            this.showErrorAlert(error);
        })
    }

    showErrorAlert(error) {
        this.alertCtrl.create({
            subTitle: this.calendarService.errorToString(error),
            buttons: [this.translations["OK"]]
        }).present();
    }


}
