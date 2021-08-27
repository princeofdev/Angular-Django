import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { SignupService } from '../../providers/signup-service';
import { SignupConfirmationPage } from '../signup-confirmation/signup-confirmation';
import { UserService } from '../../providers/user-service';
import { LoadingController } from 'ionic-angular/components/loading/loading-controller';
import { TranslateService } from '@ngx-translate/core';
import { AlertController } from 'ionic-angular/components/alert/alert-controller';
import { ServicesService } from '../../providers/services-service';


@IonicPage()
@Component({
  selector: 'page-work-days',
  templateUrl: 'work-days.html',
})
export class WorkDaysPage extends UIComponent {

  translations = {};
  public selectedHours = [];
  public selectedDays = [];
  user: any;
  public days = [{ key: 1, value: "Mon" }, { key: 2, value: "Tue" }, { key: 3, value: "Wed" }, { key: 4, value: "Thu" }, { key: 5, value: "Fri" }, { key: 6, value: "Sat" }, { key: 0, value: "Sun" }]
  public mornings = [{ key: 7, value: "07:00 - 08:00" }, { key: 8, value: "08:00 - 09:00" }, { key: 9, value: "09:00 - 10:00" }, { key: 10, value: "10:00 - 11:00" }, { key: 11, value: "11:00 - 12:00" }, { key: 12, value: "12:00 - 13:00" }, { key: 13, value: "13:00 - 14:00" }];
  public afternoons = [{ key: 14, value: "14:00 - 15:00" }, { key: 15, value: "15:00 - 16:00" }, { key: 16, value: "16:00 - 17:00" }, { key: 17, value: "17:00 - 18:00" }, { key: 18, value: "18:00 - 19:00" }, { key: 19, value: "19:00 - 20:00" }, { key: 20, value: "20:00" }];
  public editMode = true;
  private savedSuccesfully: string;
  public title: any;
  public registerMode: any;
  constructor(
    private signupService: SignupService,
    public navCtrl: NavController,
    public navParams: NavParams,
    public userService: UserService,
    public loadingCtrl: LoadingController,
    public translate: TranslateService,
    public alertCtrl: AlertController,
    public servicesService: ServicesService,

  ) {
    super();
    if (this.navParams.get("editMode") === false) {
      this.editMode = this.navParams.get("editMode");
    }
    this.registerMode = true;
    if (this.editMode) {
      this.registerMode = false;
      const loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
      loader.present();
      this.userService.getUser().subscribe(data => {
        this.user = data;
        this.selectedDays = this.user.profile.work_days || [];
        this.selectedHours = this.user.profile.work_hours || [];
        loader.dismiss();
      });
    }
    this.translate.get(["Loading", "OK","Workdays","Mon","Tue","Wed","Thu","Fri","Sat","Sun"]).subscribe(result => {
      this.translations = result;
      this.title = result['Workdays'];
      this.days = [
        { key: 1, value: this.translations["Mon"] },
        { key: 2, value: this.translations["Tue"]  },
        { key: 3, value: this.translations["Wed"] },
        { key: 4, value: this.translations["Thu"] },
        { key: 5, value: this.translations["Fri"] },
        { key: 6, value: this.translations["Sat"] },
        { key: 0, value: this.translations["Sun"] }
      ]
    });
    this.translate.get('Saved Successfully').subscribe(
      value => {
        this.savedSuccesfully = value;
      }
    );


  }
  isHourSelected(hour) {
    return this.selectedHours.indexOf(hour) >= 0;
  }

  switchHour(hour) {
    if (this.isHourSelected(hour)) {
      this.selectedHours = this.selectedHours.filter(item => item != hour);
    } else {
      this.selectedHours.push(hour);
    }
  }

  hourStyle(hour) {
    if (this.isHourSelected(hour)) {
      return { "clicked": true };
    } else {
      return {};
    }
  }
  isDaySelected(day) {
    return this.selectedDays.indexOf(day) >= 0;
  }

  switchDay(day) {
    if (this.isDaySelected(day)) {
      this.selectedDays = this.selectedDays.filter(item => item != day);
    } else {
      this.selectedDays.push(day);
    }
  }

  dayStyle(day) {
    if (this.isDaySelected(day)) {
      return { "clicked": true };
    } else {
      return {};
    }
  }

  save() {

    const loader = this.loadingCtrl.create({ content: this.translations["Loading"] });
    loader.present();
    this.signupService.setWorkHours(this.selectedHours);
    this.signupService.setWorkDays(this.selectedDays);
    if (!this.editMode) {
      this.signupService.registerUser().subscribe(result => {
        loader.dismiss();
        this.signupService.setValidRegister(true);
        this.navCtrl.push(SignupConfirmationPage);
      }, error => {
        loader.dismiss();
        this.alertCtrl.create({
          message: this.servicesService.errorToString(error.errors),
          buttons: [this.translations["OK"]]
        }).present();
      });
    } else {
      this.userService.updateWorkDays(this.selectedDays, this.selectedHours).subscribe(result => {
        loader.dismiss();
        this.alertCtrl.create({
          message:  this.savedSuccesfully,
          buttons: [{
            text: this.translations["OK"],
          }]
        }).present();
      }, error => {
        loader.dismiss();
        this.alertCtrl.create({
          message: this.servicesService.errorToString(error.errors),
          buttons: [{text: this.translations["OK"]}]
        }).present();
      });
    }
  }


}
