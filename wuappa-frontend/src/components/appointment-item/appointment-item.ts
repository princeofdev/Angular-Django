import { Component, Input,Output,EventEmitter } from '@angular/core';
import { OnInit } from '@angular/core/src/metadata/lifecycle_hooks';
import * as moment from 'moment';
import { SessionService } from '../../providers/session-service';

/**
 * Generated class for the AppointmentItemComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'appointment-item',
  templateUrl: 'appointment-item.html'
})
export class AppointmentItemComponent implements OnInit {

  userType: any;
  @Input() appointment: any;
  @Output() goDetail: EventEmitter<any> = new EventEmitter<any>();
  date: any;
  time: any;
  picture: any;

  constructor(private sessionService: SessionService) {

  }

  ngOnInit(){
    this.sessionService.getUser().then(result => {
      let user: any = result;
      this.userType = user.type;
      for (let key of this.appointment) {
        if (typeof this.appointment[key] === 'undefined') {
          this.appointment[key] = '';
        }
      }
      this.date = this.getFormattedDate(this.appointment.date);
      this.time = this.getFormattedHour(this.appointment.time);
      this.picture = this.getPicture(user);
    })
  }

  goToDetail() {
   this.goDetail.emit(this.appointment);
  }

  getFormattedDate(date) {
    let formatted_date = moment(date).format("DD/MM/YYYY");
    return formatted_date;
  }

  getFormattedHour(hour){
    return moment(hour,"hh:mm:ss").format('HH:mm');
  }

  getPicture(user) {
    if (user.type == "FIN") {
      let hasPicture = this.appointment.professional && this.appointment.professional.profile.picture;

      if (hasPicture) {
        return this.appointment.professional.profile.picture;
      }else{
        return "assets/imgs/profile-default-image.png";

      }
    } else {
      let hasPicture = this.appointment.client && this.appointment.client.profile.picture;      
      if (hasPicture) {
        return this.appointment.client.profile.picture;
      }else{
        return "/assets/imgs/profile-default-image.png";

      }

    }
  }


}
