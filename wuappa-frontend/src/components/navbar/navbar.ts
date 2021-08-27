import { Component, Input } from '@angular/core';
import { MenuController, App } from 'ionic-angular';
import { AppointmentsPage } from '../../pages/appointments/appointments';


@Component({
  selector: 'navbar',
  templateUrl: 'navbar.html'
})

export class NavbarComponent {

  @Input() title: string = null;
  @Input() registerMode: any = false;

  constructor(public appCtrl: App, public menuCtrl: MenuController) { }

  goToAppointments(){
    this.appCtrl.getActiveNavs("menuRoot")[0].setRoot(AppointmentsPage);
  }

  toogleMenu() {
    this.menuCtrl.enable(true);
    this.menuCtrl.toggle();
  }

}
