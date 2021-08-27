import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { UserCalendarPage } from './user-calendar';
import { TranslateModule } from '@ngx-translate/core';
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  declarations: [
    UserCalendarPage,
  ],
  exports: [
    UserCalendarPage
  ],
  imports: [
    IonicPageModule.forChild(UserCalendarPage),
    TranslateModule,
    ComponentsModule,
    ]
})
export class UserCalendarPageModule {}
