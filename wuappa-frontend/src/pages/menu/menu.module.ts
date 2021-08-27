import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { MenuPage } from './menu';
import { ComponentsModule } from '../../components/components.module';
import { TranslateModule } from '@ngx-translate/core';

import { Push } from '@ionic-native/push';
import { HomePageModule } from '../home/home.module';
import { ListPageModule } from '../list/list.module';
import { AppointmentsPageModule } from '../appointments/appointments.module';

@NgModule({
  declarations: [
    MenuPage
  ],
  exports: [
    MenuPage
  ],
  imports: [
    IonicPageModule.forChild(MenuPage),
    TranslateModule,
    ComponentsModule,
    HomePageModule,
    ListPageModule,
    AppointmentsPageModule
  ],
  providers: [
    Push
  ]
})
export class MenuPageModule {}
