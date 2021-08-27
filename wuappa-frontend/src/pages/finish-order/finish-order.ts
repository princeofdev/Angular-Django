import { Component } from '@angular/core';
import { IonicPage, App } from 'ionic-angular';
import { UIComponent } from '../../classes/component';
import { AppointmentsPage } from '../appointments/appointments';


@IonicPage()
@Component({
    selector: 'page-finish-order',
    templateUrl: 'finish-order.html',
})
export class FinishOrderPage extends UIComponent {


    constructor(
        private app: App
    ) {
      super();
        this.setUIIdeal();
    }

    goToAppointments() {
        this.app.getActiveNavs("menuRoot")[0].setRoot(AppointmentsPage, {
            activeItem: 'pending'
        });
    }

}
