import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AppointmentsPage } from './appointments';
import { ComponentsModule } from '../../components/components.module';
import { TranslateModule } from '@ngx-translate/core';

@NgModule({
  declarations: [AppointmentsPage],
  exports: [AppointmentsPage],
  imports: [
    IonicPageModule.forChild(AppointmentsPage),
    ComponentsModule,
    TranslateModule
    ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]

})
export class AppointmentsPageModule {}
