import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AppointmentDetailPage } from './appointment-detail';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [AppointmentDetailPage],
  exports: [AppointmentDetailPage],
  imports: [
    IonicPageModule.forChild(AppointmentDetailPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class AppointmentDetailPageModule {}
