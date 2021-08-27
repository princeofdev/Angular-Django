import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { WorkCalendarPage } from './work-calendar';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    WorkCalendarPage
  ],
  exports: [
    WorkCalendarPage
  ],
  imports: [
    IonicPageModule.forChild(WorkCalendarPage),
    TranslateModule,
    ComponentsModule
  ],
})
export class WorkCalendarPageModule {}
